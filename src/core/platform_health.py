import os
import redis
import boto3
from botocore.client import Config
from opensearchpy import OpenSearch
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.core.logging_config import get_logger

logger = get_logger(__name__)


class PlatformHealthService:
    def __init__(self, db: Session):
        self.db = db

    def check_postgres(self):
        try:
            self.db.execute(text("SELECT 1"))
            return {"status": "healthy", "message": "PostgreSQL connection successful"}
        except Exception as e:
            return {"status": "unhealthy", "message": str(e)}

    def check_redis(self):
        try:
            r = redis.Redis(
                host=os.getenv("REDIS_HOST", "redis"),
                port=int(os.getenv("REDIS_PORT", 6379)),
                socket_timeout=2,
            )
            r.ping()
            return {"status": "healthy", "message": "Redis ping successful"}
        except Exception as e:
            return {"status": "unhealthy", "message": str(e)}

    def check_minio(self):
        try:
            s3 = boto3.client(
                "s3",
                endpoint_url=f"http://{os.getenv('MINIO_ENDPOINT', 'minio:9000')}",
                aws_access_key_id=os.getenv("MINIO_ACCESS_KEY", "minioadmin"),
                aws_secret_access_key=os.getenv("MINIO_SECRET_KEY", "minioadmin"),
                config=Config(signature_version="s3v4", connect_timeout=2),
            )
            s3.list_buckets()
            return {"status": "healthy", "message": "MinIO S3 API responsive"}
        except Exception as e:
            return {"status": "unhealthy", "message": str(e)}

    def check_opensearch(self):
        try:
            client = OpenSearch(
                hosts=[
                    {
                        "host": os.getenv("OPENSEARCH_HOST", "opensearch"),
                        "port": 9200,
                        "scheme": "http",
                    }
                ],
                use_ssl=False,
                verify_certs=False,
                timeout=2,
            )
            client.info()
            return {"status": "healthy", "message": "OpenSearch cluster responsive"}
        except Exception as e:
            return {"status": "unhealthy", "message": str(e)}

    def get_health_report(self):
        return {
            "postgres": self.check_postgres(),
            "redis": self.check_redis(),
            "minio": self.check_minio(),
            "opensearch": self.check_opensearch(),
        }

    def get_platform_metrics(self):
        # Atlas stats
        atlas_datasets = (
            self.db.execute(text("SELECT COUNT(*) FROM metadata_registry")).scalar()
            or 0
        )

        # Knowledge Graph stats
        kg_entities = (
            self.db.execute(text("SELECT COUNT(*) FROM graph_entities")).scalar() or 0
        )
        kg_relationships = (
            self.db.execute(text("SELECT COUNT(*) FROM graph_relationships")).scalar()
            or 0
        )

        # Data Lake stats (MinIO)
        minio_buckets = 0
        try:
            s3 = boto3.client(
                "s3",
                endpoint_url=f"http://{os.getenv('MINIO_ENDPOINT', 'minio:9000')}",
                aws_access_key_id=os.getenv("MINIO_ACCESS_KEY", "minioadmin"),
                aws_secret_access_key=os.getenv("MINIO_SECRET_KEY", "minioadmin"),
                config=Config(signature_version="s3v4"),
            )
            minio_buckets = len(s3.list_buckets().get("Buckets", []))
        except Exception:
            pass

        return {
            "data_atlas": {"total_datasets": atlas_datasets},
            "knowledge_graph": {
                "total_entities": kg_entities,
                "total_relationships": kg_relationships,
            },
            "data_lake": {"total_buckets": minio_buckets},
            "platform_status": "Phase 3 Core Data Platform Operational",
        }
