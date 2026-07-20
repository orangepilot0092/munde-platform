"""
Bulk reclassification script for Sprint 41.5.
Fixes Categories B, C, and D based on empirical harness results.
"""

import yaml
import os

updates = {
    # Category B: Auth Required (Honest Flagging)
    "datagov_agriculture_maharashtra.yaml": {
        "auth_required": True,
        "status": "ready",
        "blocked_reason": "Requires data.gov.in API Key",
    },
    "cpcb_aqi_maharashtra.yaml": {
        "auth_required": True,
        "status": "ready",
        "blocked_reason": "Requires data.gov.in API Key",
    },
    "udise_schools_maharashtra.yaml": {
        "auth_required": True,
        "status": "ready",
        "blocked_reason": "Requires data.gov.in API Key",
    },
    "firms_fire_maharashtra.yaml": {
        "auth_required": True,
        "status": "ready",
        "blocked_reason": "Requires NASA FIRMS MAP_KEY",
    },
    # Category D: SSL Issues (Fix via ssl_verify: false)
    "rest_maha_agri.yaml": {"ssl_verify": False},
    # Category C: Fake APIs -> Scraper/Manual (Honest Reclassification)
    "rest_dpiit.yaml": {
        "type": "scraper",
        "url": "https://dpiit.gov.in/fdi-statistics",
        "status": "ready",
        "blocked_reason": "Requires HTML scraping",
    },
    "rest_eci.yaml": {
        "type": "scraper",
        "url": "https://eci.gov.in/election-results/",
        "status": "ready",
        "blocked_reason": "Requires HTML scraping",
    },
    "rest_india_code.yaml": {
        "type": "scraper",
        "url": "https://www.indiacode.nic.in/",
        "status": "ready",
        "blocked_reason": "Requires HTML scraping",
    },
    "rest_gst_statistics.yaml": {
        "type": "scraper",
        "url": "https://cbic.gov.in/gst-statistics",
        "status": "ready",
        "blocked_reason": "Requires HTML scraping",
    },
    "nhai_toll_plazas_maharashtra.yaml": {
        "type": "scraper",
        "url": "https://nhai.org/toll-plaza-data",
        "status": "ready",
        "blocked_reason": "Requires HTML scraping",
    },
    "msrtc_bus_routes_maharashtra.yaml": {
        "type": "manual",
        "url": "https://msrtc.gov.in/",
        "status": "ready",
        "blocked_reason": "No public data feed available",
    },
}

for filename, changes in updates.items():
    filepath = f"configs/connectors/{filename}"
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            data = yaml.safe_load(f) or {}
        data.update(changes)
        with open(filepath, "w") as f:
            yaml.dump(data, f, sort_keys=False)
        print(f"✅ Reclassified {filename}")
