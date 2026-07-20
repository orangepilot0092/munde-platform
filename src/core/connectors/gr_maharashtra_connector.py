"""
GR Maharashtra Connector — Government Resolution Scraper
Source: https://gr.maharashtra.gov.in
Verified Endpoints (2026-07-09):
  - /Site/SearchGR.aspx (ASP.NET WebForms, may require CAPTCHA)
  - /1035/शासन-निर्णय → redirects to /1145/Government-Resolutions (HAS CAPTCHA)
Domain: Policy / RAG Corpus
Access: Public (no authentication required, but CAPTCHA present)
AI Readiness: NLP, RAG, Summarization, Classification
Note: Full automation deferred to Sprint 34 (OCR + headless browser pipeline).
      This connector attempts server-rendered table parsing and falls back
      gracefully when CAPTCHA blocks automated access.
"""

from typing import Any, Optional
import re
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel
from src.core.connectors.live_base import LiveConnectorBase
from src.core.logging_config import get_logger

logger = get_logger(__name__)


class GRRecord(BaseModel):
    """Schema for a single Government Resolution entry."""

    title: str
    date: str
    department: str
    pdf_url: Optional[str] = None
    gr_number: Optional[str] = None


class GRMaharashtraConnector(LiveConnectorBase):
    BASE_URL = "https://gr.maharashtra.gov.in"
    SEARCH_URL = f"{BASE_URL}/Site/SearchGR.aspx"
    LISTING_URL = f"{BASE_URL}/1145/Government-Resolutions"

    # Verified table selectors from live HTML inspection (2026-07-09)
    TABLE_SELECTORS = [
        "table#SitePH_dgvDocuments",
        "table.tblFlexi.gr",
        "table#GridView1",
        "table.grid-view",
        "table[id*='GridView']",
        "table",
    ]

    # ASP.NET form field names verified from live HTML
    FORM_FIELDS = {
        "department": "ctl00$SitePH$ddlDepartmentType",
        "from_date": "ctl00$SitePH$txtFromDate",
        "to_date": "ctl00$SitePH$txtToDate",
        "captcha": "ctl00$SitePH$txtimgcode",
        "date_filter": "ctl00$SitePH$rblDateFilter",
    }

    def __init__(self):
        super().__init__("gr_maharashtra", "GR Maharashtra Portal")
        self.is_live = True
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "ProjectSahyadri/1.0 (DPI Research Bot; contact@sahyadri.ai)",
                "Accept-Language": "mr,en;q=0.9",
            }
        )

    def _get_aspnet_tokens(self, url: str) -> dict[str, str]:
        """Extract __VIEWSTATE and __EVENTVALIDATION from an ASP.NET page."""
        resp = self.session.get(url, timeout=30)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        tokens = {}
        for field in ["__VIEWSTATE", "__VIEWSTATEGENERATOR", "__EVENTVALIDATION"]:
            tag = soup.find("input", {"name": field})
            if tag and tag.get("value"):
                tokens[field] = tag["value"]
        logger.debug(f"Extracted {len(tokens)} ASP.NET tokens from {url}")
        return tokens

    def _has_captcha(self, html: str) -> bool:
        """Check if the response contains a CAPTCHA challenge."""
        return "txtimgcode" in html or "captcha" in html.lower()

    def _parse_gr_table(self, html: str) -> list[dict]:
        """Parse GR entries from the verified table structure."""
        soup = BeautifulSoup(html, "html.parser")
        table = None
        for selector in self.TABLE_SELECTORS:
            table = soup.select_one(selector)
            if table:
                logger.info(f"Found GR table using selector: {selector}")
                break

        if not table:
            logger.warning("No GR table found in response HTML")
            return []

        rows = table.select("tr")[1:]  # Skip header row
        grs: list[dict] = []

        for row in rows:
            cols = row.select("td")
            if len(cols) < 3:
                continue

            # Find PDF link (verified pattern: ../Site/Upload/Government%20Resolutions/...)
            link_tag = None
            for col in cols:
                a_tag = col.select_one("a[href*='.pdf']")
                if a_tag:
                    link_tag = a_tag
                    break

            title = link_tag.get_text(strip=True) if link_tag else ""
            pdf_href = link_tag.get("href") if link_tag else None

            if pdf_href and not pdf_href.startswith("http"):
                pdf_href = f"{self.BASE_URL}/{pdf_href.lstrip('../')}"

            # Extract date and department from remaining columns
            text_cols = [
                c.get_text(strip=True)
                for c in cols
                if not c.select_one("a[href*='.pdf']")
            ]
            date_str = text_cols[0] if len(text_cols) > 0 else ""
            dept_str = text_cols[1] if len(text_cols) > 1 else ""

            # Extract GR number pattern (e.g., "JSA-2024/CR-123/WCD")
            gr_number = None
            match = re.search(r"[A-Z]+-\d{4}/[A-Z]+-\d+/[A-Z]+", title)
            if match:
                gr_number = match.group(0)

            if title or pdf_href:
                record = GRRecord(
                    title=title,
                    date=date_str,
                    department=dept_str,
                    pdf_url=pdf_href,
                    gr_number=gr_number,
                )
                grs.append(record.model_dump())

        return grs

    def fetch_live(
        self, department: Optional[str] = None, limit: int = 10, **kwargs
    ) -> dict[str, Any]:
        """
        Fetch GRs via ASP.NET WebForms POST.
        Falls back to GET-based listing page parsing.
        Gracefully handles CAPTCHA by returning empty results with warning.
        """
        limit = min(limit, 50)
        source_url = self.SEARCH_URL

        try:
            # Attempt 1: POST to SearchGR.aspx with ASP.NET tokens
            tokens = self._get_aspnet_tokens(self.SEARCH_URL)
            post_data = {
                **tokens,
                self.FORM_FIELDS["date_filter"]: "1",  # देवाण दिनांक
            }
            if department:
                post_data[self.FORM_FIELDS["department"]] = department

            logger.info(
                f"POSTing to {self.SEARCH_URL} (dept={department}, limit={limit})"
            )
            resp = self.session.post(self.SEARCH_URL, data=post_data, timeout=30)
            resp.raise_for_status()
            resp.encoding = "utf-8"

            if self._has_captcha(resp.text):
                logger.warning(
                    "CAPTCHA detected on SearchGR.aspx. Automated scraping blocked."
                )
                raise ValueError("CAPTCHA challenge detected")

            grs = self._parse_gr_table(resp.text)
            if grs:
                return {
                    "grs": grs[:limit],
                    "count": len(grs[:limit]),
                    "source_url": source_url,
                    "method": "POST",
                }

        except Exception as e:
            logger.warning(f"SearchGR.aspx failed ({e}), trying listing page...")

        try:
            # Attempt 2: GET the listing page directly
            source_url = self.LISTING_URL
            logger.info(f"GETting listing page: {self.LISTING_URL}")
            resp = self.session.get(self.LISTING_URL, timeout=30)
            resp.raise_for_status()
            resp.encoding = "utf-8"

            if self._has_captcha(resp.text):
                logger.warning(
                    "CAPTCHA detected on listing page. Automated scraping blocked."
                )
                raise ValueError("CAPTCHA challenge detected")

            grs = self._parse_gr_table(resp.text)
            return {
                "grs": grs[:limit],
                "count": len(grs[:limit]),
                "source_url": source_url,
                "method": "GET",
            }

        except Exception as e:
            logger.error(
                f"All GR scraping attempts failed: {e}. Returning sample data."
            )
            sample = self.get_sample_data()
            sample["warning"] = (
                "Live scraping blocked by CAPTCHA. "
                "Full automation requires Sprint 34 OCR + headless browser pipeline. "
                "Using sample data for development."
            )
            return sample

    def get_sample_data(self, **kwargs) -> dict[str, Any]:
        """Return realistic sample data for dry-run/testing."""
        samples = [
            GRRecord(
                title="Jalyukt Shivar Abhiyan 2.0 Implementation Guidelines",
                date="2024-06-15",
                department="जलसंपदा",
                pdf_url="https://gr.maharashtra.gov.in/Site/Upload/Government%20Resolutions/Marathi/JSA2024.pdf",
                gr_number="JSA-2024/CR-123/WCD",
            ),
            GRRecord(
                title="PM-KISAN Integration with KrishiSetu Platform",
                date="2024-07-01",
                department="कृषी",
                pdf_url="https://gr.maharashtra.gov.in/Site/Upload/Government%20Resolutions/Marathi/PMKISAN2024.pdf",
                gr_number="AGRI-2024/CR-456/Farmers",
            ),
            GRRecord(
                title="Dynamic Water Rationing for Municipal Corporations",
                date="2024-07-05",
                department="नगर विकास",
                pdf_url="https://gr.maharashtra.gov.in/Site/Upload/Government%20Resolutions/Marathi/NagarSetu2024.pdf",
                gr_number="UD-2024/CR-789/NagarSetu",
            ),
        ]
        return {
            "grs": [s.model_dump() for s in samples],
            "count": len(samples),
            "source_url": self.LISTING_URL,
            "status": "sample_data",
            "note": "SAMPLE DATA — Live scraping requires CAPTCHA bypass (Sprint 34)",
        }
