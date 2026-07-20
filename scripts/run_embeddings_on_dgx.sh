#!/usr/bin/env bash
# Run generate_metadata_embeddings Dagster asset on DGX Spark AI Node
# Usage: ./scripts/run_embeddings_on_dgx.sh [--dry-run]
set -euo pipefail

DGX_HOST="${DGX_HOST:-advait_sanap@edgexpert-c0d5}"
PROJECT_DIR="${DGX_PROJECT_DIR:-/home/advait_sanap/projects/sahyadri-platform}"
LOCAL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DRY_RUN="${1:-}"

echo "🚀 Deploying embedding pipeline to DGX Spark: ${DGX_HOST}"

# Step 1: Sync code to DGX Spark
echo "📦 Syncing code..."
if [ "$DRY_RUN" = "--dry-run" ]; then
    echo "[DRY-RUN] rsync -avz --exclude='.venv' --exclude='__pycache__' ${LOCAL_DIR}/ ${DGX_HOST}:${PROJECT_DIR}/"
else
    rsync -avz --exclude='.venv' --exclude='__pycache__' --exclude='.git' \
        "${LOCAL_DIR}/" "${DGX_HOST}:${PROJECT_DIR}/"
fi

# Step 2: Execute Dagster asset on DGX Spark
echo "⚙️  Executing generate_metadata_embeddings asset..."
REMOTE_CMD="cd ${PROJECT_DIR} && poetry run dagster asset materialize --select generate_metadata_embeddings"

if [ "$DRY_RUN" = "--dry-run" ]; then
    echo "[DRY-RUN] ssh ${DGX_HOST} '${REMOTE_CMD}'"
else
    ssh "${DGX_HOST}" "${REMOTE_CMD}"
fi

echo "✅ Embedding pipeline execution complete"
