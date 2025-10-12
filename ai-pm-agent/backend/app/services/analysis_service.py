from __future__ import annotations

import os
from typing import Any, Dict, List, TypedDict

import httpx
from pydantic import BaseModel
from .embeddings import embed_text
from ..core.config import settings
from typing import Any, Sequence

# Optional: use official supabase-py v2
from supabase import create_client, Client # type: ignore


class LiveResult(TypedDict, total=False):
    title: str
    url: str
    content: str


class RetrievedChunk(TypedDict, total=False):
    id: str
    source: str
    url: str | None
    content: str
    similarity: float


class OrchestratorPayload(BaseModel):
    transcript: str
    context: Dict[str, Any]


def _supabase() -> Client:
    if not settings.supabase_url or not settings.supabase_key:
        raise RuntimeError("Supabase credentials are missing")
    return create_client(settings.supabase_url, settings.supabase_key)


async def _retrieve_from_pgvector(transcript: str, k: int = 6, threshold: float = 0.72) -> List[RetrievedChunk]:
    """
    Calls a Postgres RPC (e.g., match_tavily) that performs cosine similarity
    against an embeddings column in your 'tavily_context' table.
    """
    embedding = await embed_text(transcript)

    sb = _supabase()
    # RPC signature assumed below; see SQL in section 5.
    resp = sb.rpc(
        settings.rag_match_rpc,
        {
            "query_embedding": embedding,
            "match_count": k,
            "similarity_threshold": threshold,
        },
    ).execute()

    rows = resp.data or []
    out: List[RetrievedChunk] = []
    for r in rows: # type: ignore
        out.append(
            {
                "id": str(r.get("id")),
                "source": r.get("source", "tavily_cached"),
                "url": r.get("url"),
                "content": r.get("content") or r.get("text") or "",
                "similarity": float(r.get("similarity", 0)),
            }
        )
    return out


async def _tavily_live_search(query: str, k: int = 5) -> List[LiveResult]:
    """Query Tavily API live, then cache the results in Supabase for future RAG retrieval."""
    if not settings.tavily_api_key:
        return []

    tavily_url = "https://api.tavily.com/search"
    payload = {
        "api_key": settings.tavily_api_key,
        "query": query,
        "search_depth": "advanced",
        "max_results": k,
        "include_answer": True,
        "include_raw_content": True,
    }

    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(tavily_url, json=payload)
        r.raise_for_status()
        data = r.json()
        results = data.get("results", [])

        out: List[LiveResult] = [
            {
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "content": item.get("raw_content") or item.get("content") or "",
            }
            for item in results
        ]

    try:
        await store_tavily_result(out)
        print(f"✅ Cached {len(out)} Tavily results to Supabase.")
    except Exception as e:
        print(f"⚠️ Failed to cache Tavily results: {e}")

    return out


async def store_tavily_result(results: Sequence[LiveResult]):
    """Compute embeddings for Tavily results and insert them into Supabase."""
    sb = _supabase()
    rows = []

    for r in results:
        text = (r.get("content") or "").strip()
        if not text:
            continue

        embedding = await embed_text(text)
        rows.append({
            "source": "tavily_live",
            "url": r.get("url"),
            "content": text[:5000],
            "embedding": embedding,
        })

    if rows:
        sb.table(settings.rag_table).insert(rows).execute()
        print(f"✅ Inserted {len(rows)} Tavily records into Supabase.")


async def call_mastra(transcript: str, context: Dict[str, Any]) -> Dict[str, Any]:
    base = settings.mastra_base_url.rstrip("/")
    url = f"{base}/run"  # adjust if your orchestrator exposes a different path
    headers = {}
    if settings.mastra_api_key:
        headers["Authorization"] = f"Bearer {settings.mastra_api_key}"

    payload = OrchestratorPayload(transcript=transcript, context=context).model_dump()
    async with httpx.AsyncClient(timeout=120) as client:
        r = await client.post(url, headers=headers, json=payload)
        r.raise_for_status()
        return r.json()


async def analyze_with_rag(transcript: str) -> Dict[str, Any]:
    """
    Full pipeline:
      - PgVector retrieval (cached Tavily / prior knowledge)
      - Live Tavily for freshness
      - Call Mastra with consolidated context
    """
    history_chunks, live_results = await _retrieve_from_pgvector(transcript), await _tavily_live_search(transcript)

    context = {
        "retrieval": {
            "pgvector": history_chunks,
            "tavily_live": live_results,
        }
    }
    return await call_mastra(transcript, context)
