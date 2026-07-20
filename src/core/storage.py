import hashlib
from minio import Minio
from src.core.config import settings
from src.core.logging_config import get_logger

logger = get_logger(__name__)


class MinIOService:
    def __init__(self):
        # Ensure endpoint is handled correctly (e.g., "minio:9000" or "localhost:9000")
        self.client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=False,
        )

    def ensure_bucket(self, bucket_name: str):
        if not self.client.bucket_exists(bucket_name):
            self.client.make_bucket(bucket_name)
            logger.info(f"Created bucket: {bucket_name}")

    def upload_file(self, bucket_name: str, object_name: str, file_path: str):
        self.ensure_bucket(bucket_name)
        self.client.fput_object(bucket_name, object_name, file_path)
        logger.info(f"Uploaded {file_path} to {bucket_name}/{object_name}")

    def calculate_hash(self, file_path: str) -> str:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
