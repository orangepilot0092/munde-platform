import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/ai", tags=["AI Services"])

class SummarizeRequest(BaseModel):
    text: str
    model: str = "qwen2.5:14b"

class SummarizeResponse(BaseModel):
    summary: str
    model_used: str

@router.post("/summarize", response_model=SummarizeResponse)
async def summarize_text(request: SummarizeRequest):
    ai_node_url = "http://192.168.29.96:11434/api/generate"
    payload = {
        "model": request.model,
        "prompt": f"Summarize the following text concisely in 2-3 sentences:\n\n{request.text}",
        "stream": False
    }
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(ai_node_url, json=payload)
            response.raise_for_status()
            result = response.json()
            return SummarizeResponse(summary=result.get("response", "No summary generated"), model_used=request.model)
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"AI Node unreachable: {str(e)}")
