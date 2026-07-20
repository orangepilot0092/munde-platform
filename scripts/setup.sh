#!/bin/bash
set -e

echo "🚀 Setting up Project Sahyadri Local Environment..."

# Check for Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker Desktop or Docker Engine."
    exit 1
fi

# Check for Docker Compose
if ! command -v docker compose &> /dev/null; then
    echo "❌ Docker Compose V2 is not installed."
    exit 1
fi

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env from .env.example..."
    cp .env.example .env
    echo "⚠️  Please update .env with secure passwords before starting services."
fi

# Start Services
echo "🐳 Starting infrastructure services..."
docker compose -f docker/dev.yml up -d

echo "✅ Setup complete!"
echo "🔹 Database: localhost:5432"
echo "🔹 MinIO API: localhost:9000"
echo "🔹 MinIO Console: localhost:9001"
echo "🔹 Redis: localhost:6379"
