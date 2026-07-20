"""
Prompt Registry Pydantic Models
Sprint 34 — LLM-as-Judge Evaluation Support
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class PromptCreate(BaseModel):
    prompt_id: str = Field(..., min_length=3, max_length=100)
    name: str = Field(..., min_length=3, max_length=255)
    domain: str
    category: str
    system_prompt: str = Field(..., min_length=10)
    user_template: str | None = None
    variables: dict[str, Any] | None = None
    expected_output_schema: dict[str, Any] | None = None
    tags: list[str] | None = None
    metadata: dict[str, Any] | None = None


class PromptUpdate(BaseModel):
    name: str | None = None
    system_prompt: str | None = None
    user_template: str | None = None
    variables: dict[str, Any] | None = None
    expected_output_schema: dict[str, Any] | None = None
    tags: list[str] | None = None
    metadata: dict[str, Any] | None = None


class PromptResponse(BaseModel):
    id: int
    prompt_id: str
    name: str
    version: int
    domain: str
    category: str
    system_prompt: str
    user_template: str | None
    variables: dict[str, Any] | None
    expected_output_schema: dict[str, Any] | None
    tags: list[str] | None
    metadata: dict[str, Any] | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EvalRequest(BaseModel):
    prompt_id: str
    model: str = Field(default="llama3.1:8b")
    test_inputs: list[dict[str, Any]] = Field(..., min_length=1)
    ground_truth: list[str] | None = None
    metrics: list[str] = Field(
        default=["faithfulness", "answer_relevancy", "context_precision"]
    )
    use_llm_judge: bool = Field(
        default=True, description="Use Mumbai-Vikram as LLM judge instead of heuristics"
    )
    async_mode: bool = Field(
        default=False,
        description="Submit to background queue instead of synchronous execution",
    )


class MetricResult(BaseModel):
    metric_name: str
    score: float
    method: str
    reasoning: str | None = None
    details: dict[str, Any] | None = None


class EvalResult(BaseModel):
    prompt_id: str
    model: str
    version: int
    metrics: list[MetricResult]
    num_samples: int
    timestamp: datetime
    avg_score: float
    judge_model: str | None = None
    llm_calls: list[dict[str, Any]] = []
