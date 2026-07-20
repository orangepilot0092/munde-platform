import time
import uuid

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.api.v1 import router as v1_router
from src.core.health import router as health_router
from src.core.logging_config import get_logger, request_id_var

logger = get_logger(__name__)

app = FastAPI(
    title="Project Sahyadri",
    description="Open-source data and intelligence platform for Maharashtra.",
    version="0.1.0",
)

from fastapi.exceptions import RequestValidationError  # noqa: E402
from slowapi.errors import RateLimitExceeded  # noqa: E402
from starlette.middleware.base import BaseHTTPMiddleware  # noqa: E402

from src.core.exceptions import (  # noqa: E402
    generic_exception_handler,
    http_exception_handler,
    rate_limit_exceeded_handler,
    validation_exception_handler,
)

# 1. Initialize Rate Limiter
from src.core.limiter import limiter  # noqa: E402

app.state.limiter = limiter


# 2. Request ID Middleware for Distributed Tracing
class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


app.add_middleware(RequestIDMiddleware)

# 3. Register Global Exception Handlers
from fastapi import HTTPException  # noqa: E402

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)


# Initialize Rate Limiter
from src.core.limiter import limiter  # noqa: E402

app.state.limiter = limiter

# Include Routers
app.include_router(health_router)
app.include_router(v1_router)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error", "request_id": request_id_var.get()},
    )


@app.middleware("http")
async def add_metrics_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request_id_var.set(request_id)

    start_time = time.time()
    try:
        response = await call_next(request)
    except Exception as e:
        raise e
    finally:
        time.time() - start_time

    response.headers["X-Request-ID"] = request_id
    return response


from src.api.v1.search import router as search_router  # noqa: E402

app.include_router(search_router, prefix="/api/v1")


from src.api.v1.atlas import router as atlas_router  # noqa: E402

app.include_router(atlas_router, prefix="/api/v1")


from src.api.v1.catalog_search import router as catalog_router  # noqa: E402

app.include_router(catalog_router, prefix="/api/v1")


from src.api.v1.storage import router as storage_router  # noqa: E402

app.include_router(storage_router, prefix="/api/v1")


from src.api.v1.connectors import router as connectors_router  # noqa: E402
from src.api.v1.prompts import router as prompts_router  # noqa: E402

app.include_router(connectors_router, prefix="/api/v1")
app.include_router(prompts_router, prefix="/api/v1")


from src.api.v1.graph import router as graph_router  # noqa: E402

app.include_router(graph_router, prefix="/api/v1")


from src.api.v1.geospatial import router as geospatial_router  # noqa: E402

app.include_router(geospatial_router, prefix="/api/v1")


from src.api.v1.lineage import router as lineage_router  # noqa: E402

app.include_router(lineage_router, prefix="/api/v1")


from src.api.v1.platform import router as platform_router  # noqa: E402

app.include_router(platform_router, prefix="/api/v1")


from src.api.v1.rag import router as rag_router  # noqa: E402

app.include_router(rag_router, prefix="/api/v1")
from src.api.v1.api_status import router as api_status_router  # noqa: E402
from src.core.metrics import router as metrics_router  # noqa: E402

app.include_router(api_status_router, prefix="/api/v1")
app.include_router(metrics_router)

# Register Knowledge Graph Query Router
from src.api.v1.graph_query import router as graph_query_router

app.include_router(graph_query_router, prefix="/api/v1")

# Register Production RAG Query Router
from src.api.v1.rag_query import router as rag_query_router

app.include_router(rag_query_router, prefix="/api/v1")
