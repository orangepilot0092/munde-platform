from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
import time

from sahyadri.core.logging import setup_logging, logger
from sahyadri.api.routes.assets import router as assets_router
from sahyadri.api.routes.ai import router as ai_router

setup_logging()

app = FastAPI(title="Project Sahyadri API", description="Sovereign Intelligence Platform for Maharashtra", version="0.1.0")

Instrumentator().instrument(app).expose(app, endpoint="/metrics")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info("http_request", method=request.method, path=request.url.path, status_code=response.status_code, duration_ms=round(process_time * 1000, 2))
    return response

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(assets_router, prefix="/api/v1")
app.include_router(ai_router, prefix="/api/v1")

@app.get("/health", tags=["System"])
async def health_check():
    logger.info("health_check_requested")
    return {"status": "healthy", "service": "sahyadri-api"}
