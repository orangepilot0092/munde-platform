import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import requests
import tempfile
import hashlib
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from src.core.config import settings
from src.core.storage import MinIOService
from src.core.ocr import OCRService
from src.core.chunking import chunk_text
from src.core.embeddings import EmbeddingService
from src.core.logging import get_logger

logger = get_logger(__name__)


def run_ocr_pipeline():
    print("=== Starting OCR Pipeline Test ===")
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    storage = MinIOService()
    ocr = OCRService()
    es = EmbeddingService()

    try:
        # 1. Download Sample PDF (Using a reliable public test PDF)
        url = "https://raw.githubusercontent.com/mozilla/pdf.js-sample-files/master/helloworld.pdf"
        print(f"Downloading {url}...")
        response = requests.get(url)
        response.raise_for_status()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(response.content)
            pdf_path = tmp.name

        # 2. Calculate Hash
        with open(pdf_path, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()

        # 3. Upload to MinIO
        bucket = "documents"
        object_name = "sample_reports/helloworld.pdf"
        print("Uploading to MinIO...")
        storage.ensure_bucket(bucket)
        storage.upload_file(bucket, object_name, pdf_path)
        minio_path = f"s3://{bucket}/{object_name}"

        # 4. Perform OCR
        print("Performing OCR (this may take a few seconds)...")
        extracted_text = ocr.extract_text_from_pdf(pdf_path)
        if not extracted_text.strip():
            raise Exception(
                "OCR failed to extract any text. Ensure tesseract-ocr and poppler-utils are installed on your host machine."
            )

        # 5. Chunk Text
        chunks = chunk_text(extracted_text)
        print(f"Generated {len(chunks)} text chunks.")

        # 6. Store in DB
        print("Saving to PostgreSQL...")
        doc_query = text("""
            INSERT INTO document_registry (title, source_url, minio_path, file_hash, total_chunks)
            VALUES (:title, :url, :path, :hash, :chunks) RETURNING id
        """)
        doc_id = db.execute(
            doc_query,
            {
                "title": "Sample Government Report",
                "url": url,
                "path": minio_path,
                "hash": file_hash,
                "chunks": len(chunks),
            },
        ).scalar()

        for i, chunk_content in enumerate(chunks):
            embedding = es.generate_embedding(chunk_content)
            chunk_query = text("""
                INSERT INTO document_chunks (document_id, chunk_index, content, embedding)
                VALUES (:doc_id, :index, :content, :embedding)
            """)
            db.execute(
                chunk_query,
                {
                    "doc_id": doc_id,
                    "index": i,
                    "content": chunk_content,
                    "embedding": embedding,
                },
            )

        db.commit()
        print(f"✅ Successfully processed document {doc_id} with {len(chunks)} chunks.")

    except Exception as e:
        print(f"❌ Pipeline failed: {e}")
        import traceback

        traceback.print_exc()
    finally:
        db.close()
        if "pdf_path" in locals() and os.path.exists(pdf_path):
            os.remove(pdf_path)


if __name__ == "__main__":
    run_ocr_pipeline()
