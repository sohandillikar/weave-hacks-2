from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..services.llm_query_generator import generate_queries


router = APIRouter()


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
        # Likely missing/invalid OpenAI setup
        raise HTTPException(status_code=502, detail="failed to generate queries from LLM")

    return AnalyzeResponse(queries=[QueryPair(**p) for p in pairs])
