#!/bin/bash
set -e

BACKUP_DIR="/tmp/backups/postgres"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
FILENAME="sahyadri_db_${TIMESTAMP}.sql.gz"

# Ensure backup directory exists
mkdir -p $BACKUP_DIR

echo "Starting PostgreSQL backup..."

# Perform dump and compress
pg_dump -U ${DB_USER:-sahyadri} -h postgres -d ${DB_NAME:-sahyadri_db} | gzip > $BACKUP_DIR/$FILENAME

echo "Backup completed: $BACKUP_DIR/$FILENAME"

# Optional: Upload to MinIO if mc is available
if command -v mc &> /dev/null; then
    echo "Uploading to MinIO..."
    mc alias set myminio http://minio:9000 ${MINIO_ROOT_USER:-minioadmin} ${MINIO_ROOT_PASSWORD:-minio_secret}
    mc mb -p myminio/backups/postgres
    mc cp $BACKUP_DIR/$FILENAME myminio/backups/postgres/
    echo "Upload to MinIO completed."
fi
