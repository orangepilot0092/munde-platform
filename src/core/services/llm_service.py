"""
Multi-Model LLM Service for Sprint 34 Evaluation Framework
DB-backed model registry for enterprise auditability & governance.
Per 02_ARCHITECTURE_AND_INFRA.md Layer 8: Supports llama3.1:8b, qwen2.5:14b, mumbai-vikram:latest
"""

import os
import requests
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor
import psycopg2
from src.core.logging_config import get_logger

logger = get_logger(__name__)

AI_NODE_IP = os.environ.get("AI_NODE_IP", "192.168.29.96")
OLLAMA_BASE_URL = f"http://{AI_NODE_IP}:11434"
DATABASE_URL = os.environ.get("DATABASE_URL")


class LLMRequest(BaseModel):
    model: str = "llama3.1:8b"
    system_prompt: str
    user_message: str
    temperature: float = 0.1
    max_tokens: int = 2048


class LLMResponse(BaseModel):
    model: str
    response: str
    total_duration_ms: float
    eval_count: int
    prompt_eval_count: int


class LLMService:
    """Unified interface for multi-model LLM inference via Ollama with DB-backed registry."""

    @staticmethod
    def list_models() -> dict:
        """Fetch active models from registry."""
        if not DATABASE_URL:
            logger.warning("DATABASE_URL not set; returning empty model list")
            return {}
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            "SELECT model_id, display_name, provider, context_window, best_for, metadata "
            "FROM model_registry WHERE is_active = TRUE"
        )
        models = {row["model_id"]: dict(row) for row in cur.fetchall()}
        cur.close()
        conn.close()
        return models

    @staticmethod
    def generate(request: LLMRequest) -> LLMResponse:
        """Generate completion using specified model on AI Node."""
        available = LLMService.list_models()
        if request.model not in available:
            raise ValueError(
                f"Unsupported model '{request.model}'. "
                f"Available: {list(available.keys())}"
            )

        payload = {
            "model": request.model,
            "messages": [
                {"role": "system", "content": request.system_prompt},
                {"role": "user", "content": request.user_message},
            ],
            "stream": False,
            "options": {
                "temperature": request.temperature,
                "num_predict": request.max_tokens,
            },
        }

        logger.info(f"LLM generate: model={request.model}, temp={request.temperature}")

        resp = requests.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json=payload,
            timeout=120,
        )
        resp.raise_for_status()
        data = resp.json()

        message = data.get("message", {})
        return LLMResponse(
            model=request.model,
            response=message.get("content", ""),
            total_duration_ms=data.get("total_duration", 0) / 1e6,
            eval_count=data.get("eval_count", 0),
            prompt_eval_count=data.get("prompt_eval_count", 0),
        )

    @staticmethod
    def health_check() -> dict:
        """Verify AI Node connectivity and registry status."""
        result = {"ai_node": AI_NODE_IP}

        try:
            resp = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=10)
            resp.raise_for_status()
            ollama_models = [m["name"] for m in resp.json().get("models", [])]
            result["ollama_status"] = "healthy"
            result["ollama_models"] = ollama_models
        except Exception as e:
            result["ollama_status"] = "unhealthy"
            result["ollama_error"] = str(e)

        try:
            registry_models = LLMService.list_models()
            result["registry_status"] = "healthy"
            result["registry_models"] = list(registry_models.keys())
        except Exception as e:
            result["registry_status"] = "unhealthy"
            result["registry_error"] = str(e)

        if (
            result.get("ollama_status") == "healthy"
            and result.get("registry_status") == "healthy"
        ):
            result["status"] = "healthy"
        else:
            result["status"] = "degraded"

        return result
