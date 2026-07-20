#!/bin/bash
echo "=== Project Sahyadri Performance Baseline ==="
echo "Target: http://localhost:8001"

# Test Health Endpoint
echo "1. Health Check (/health):"
curl -w "\nTime Total: %{time_total}s\n" -o /dev/null -s http://localhost:8001/health

# Test Metrics Endpoint
echo "2. Metrics (/metrics):"
curl -w "\nTime Total: %{time_total}s\n" -o /dev/null -s http://localhost:8001/metrics

# Test API Versioning
echo "3. API Root (/api/v1):"
curl -w "\nTime Total: %{time_total}s\n" -o /dev/null -s http://localhost:8001/api/v1/

echo "=== Baseline Complete ==="
