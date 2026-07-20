#!/bin/bash
set -e

echo "Starting MinIO backup/mirror..."

# Mirror local data to a backup bucket or external location
mc alias set myminio http://minio:9000 ${MINIO_ROOT_USER:-minioadmin} ${MINIO_ROOT_PASSWORD:-minio_secret}

# Create backup bucket if it doesn't exist
mc mb -p myminio/backups/minio_data

# Mirror all buckets to the backup location
mc mirror --overwrite myminio/data myminio/backups/minio_data

echo "MinIO backup/mirror completed."
