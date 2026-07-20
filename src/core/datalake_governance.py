import boto3
from botocore.client import Config
from src.core.config import settings
from src.core.logging_config import get_logger

logger = get_logger(__name__)


class DataLakeGovernance:
    def __init__(self):
        # MinIO is S3-compatible, so we use boto3 for advanced lifecycle/versioning APIs
        self.s3 = boto3.client(
            "s3",
            endpoint_url=f"http://{settings.MINIO_ENDPOINT}",
            aws_access_key_id=settings.MINIO_ACCESS_KEY,
            aws_secret_access_key=settings.MINIO_SECRET_KEY,
            config=Config(signature_version="s3v4"),
            region_name="us-east-1",
        )

    def setup_bucket_governance(self, bucket_name: str):
        """Enable versioning and apply lifecycle rules to a bucket."""
        try:
            self.s3.head_bucket(Bucket=bucket_name)
        except Exception:
            logger.info(f"Creating bucket {bucket_name}")
            self.s3.create_bucket(Bucket=bucket_name)

        # 1. Enable Versioning (Protects against accidental deletions/overwrites)
        self.s3.put_bucket_versioning(
            Bucket=bucket_name, VersioningConfiguration={"Status": "Enabled"}
        )

        # 2. Apply Lifecycle Rules
        lifecycle_config = {
            "Rules": [
                {
                    "ID": "ExpireTempIngestionFiles",
                    "Status": "Enabled",
                    "Filter": {"Prefix": "temp/"},
                    "Expiration": {"Days": 7},
                },
                {
                    "ID": "CleanupOldVersions",
                    "Status": "Enabled",
                    "Filter": {"Prefix": ""},
                    "NoncurrentVersionExpiration": {"NoncurrentDays": 90},
                },
            ]
        }
        self.s3.put_bucket_lifecycle_configuration(
            Bucket=bucket_name, LifecycleConfiguration=lifecycle_config
        )
        logger.info(f"Governance policies applied to {bucket_name}")
        return True

    def get_storage_metrics(self):
        """Calculate storage metrics across all buckets."""
        metrics = []
        buckets = self.s3.list_buckets().get("Buckets", [])

        for bucket in buckets:
            name = bucket["Name"]
            paginator = self.s3.get_paginator("list_objects_v2")
            total_size = 0
            total_objects = 0

            for page in paginator.paginate(Bucket=name):
                for obj in page.get("Contents", []):
                    total_size += obj["Size"]
                    total_objects += 1

            metrics.append(
                {
                    "bucket": name,
                    "total_objects": total_objects,
                    "total_size_mb": round(total_size / (1024 * 1024), 2),
                }
            )

        return metrics
