import pytesseract
from pdf2image import convert_from_path
from src.core.logging import get_logger

logger = get_logger(__name__)


class OCRService:
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from a PDF file using OCR."""
        logger.info(f"Starting OCR for {pdf_path}")
        try:
            images = convert_from_path(pdf_path)
            full_text = ""
            for i, image in enumerate(images):
                text = pytesseract.image_to_string(image, lang="eng")
                full_text += f"\n--- Page {i + 1} ---\n{text}"
            logger.info(f"OCR complete. Extracted {len(full_text)} characters.")
            return full_text
        except Exception as e:
            logger.error(f"OCR failed for {pdf_path}: {e}")
            return ""
