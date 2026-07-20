FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for OCR (Tesseract/Poppler)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy and install dependencies using uv (Lightning fast!)
COPY requirements.txt ./
RUN uv pip install --system --no-cache -r requirements.txt

# Copy application code
COPY src ./src
COPY alembic ./alembic
COPY alembic.ini .
COPY scripts ./scripts
COPY etl ./etl

CMD ["uvicorn", "src.core.main:app", "--host", "0.0.0.0", "--port", "8000"]
