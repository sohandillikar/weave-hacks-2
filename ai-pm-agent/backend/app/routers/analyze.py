from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, List

from ..services.llm_query_generator import generate_queries
from ..services.analysis_service import analyze_with_rag

router = APIRouter()

# --- existing (kept) ---
class AnalyzeRequest(BaseModel):
    transcript: str

class QueryPair(BaseModel):
    user_query: str
    competitor_query: str

class AnalyzeResponse(BaseModel):
    queries: list[QueryPair]

@router.post("/", response_model=AnalyzeResponse)
async def analyze(body: AnalyzeRequest) -> AnalyzeResponse:
    transcript = (body.transcript or "").strip()
    if not transcript:
        raise HTTPException(status_code=400, detail="transcript must be a non-empty string")

    pairs = generate_queries(transcript)
    if not pairs:
        raise HTTPException(status_code=502, detail="failed to generate queries from LLM")
    return AnalyzeResponse(queries=[QueryPair(**p) for p in pairs])


# --- new orchestrated endpoint ---
class RunAnalyzeResponse(BaseModel):
    # flexible: pass through Mastra JSON (e.g., {"slow website": {"takes too long": "high"}, ...})
    result: Dict[str, Any]

@router.post("/run", response_model=RunAnalyzeResponse)
async def run(body: AnalyzeRequest) -> RunAnalyzeResponse:
    transcript = (body.transcript or "").strip()
    if not transcript:
        raise HTTPException(status_code=400, detail="transcript must be a non-empty string")

    try:
        result = await analyze_with_rag(transcript)
        if not isinstance(result, dict):
            raise ValueError("Mastra returned non-dict JSON")
        return RunAnalyzeResponse(result=result)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"analysis failed: {e}")
