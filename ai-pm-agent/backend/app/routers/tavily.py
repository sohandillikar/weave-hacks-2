from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..services.tavily_search import TavilyError, search as tavily_search


router = APIRouter()


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1)
    search_depth: str = Field("basic", pattern=r"^(basic|advanced)$")
    include_domains: Optional[List[str]] = None
    exclude_domains: Optional[List[str]] = None
    max_results: int = 5
    include_answer: bool = True
    include_images: bool = False
    include_raw_content: bool = False


class SearchResponse(BaseModel):
    data: dict


@router.post("/search", response_model=SearchResponse)
async def search(body: SearchRequest) -> SearchResponse:
    try:
        res = tavily_search(
            body.query,
            search_depth=body.search_depth,
            include_domains=body.include_domains,
            exclude_domains=body.exclude_domains,
            max_results=body.max_results,
            include_answer=body.include_answer,
            include_images=body.include_images,
            include_raw_content=body.include_raw_content,
        )
        return SearchResponse(data=res)
    except TavilyError as e:
        raise HTTPException(status_code=502, detail=str(e))

