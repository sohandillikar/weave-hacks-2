from __future__ import annotations

from typing import Any, Dict, Iterable, Optional

import httpx

from ..core.config import settings


TAVILY_BASE_URL = "https://api.tavily.com"


class TavilyError(Exception):
    pass


def _require_api_key() -> str:
    key = (settings.tavily_api_key or "").strip()
    if not key:
        raise TavilyError("TAVILY_API_KEY is not configured")
    return key


def _post(path: str, payload: dict, timeout: float = 30.0) -> Dict[str, Any]:
    url = f"{TAVILY_BASE_URL}{path}"
    with httpx.Client(timeout=timeout) as client:
        resp = client.post(url, json=payload, headers={"Content-Type": "application/json"})
    if resp.status_code >= 400:
        raise TavilyError(f"Tavily API error {resp.status_code}: {resp.text}")
    try:
        return resp.json()
    except Exception as e:
        raise TavilyError(f"Invalid JSON from Tavily: {e}")


def search(
    query: str,
    *,
    search_depth: str = "basic",  # "basic" or "advanced"
    include_domains: Optional[Iterable[str]] = None,
    exclude_domains: Optional[Iterable[str]] = None,
    max_results: int = 5,
    include_answer: bool = True,
    include_images: bool = False,
    include_raw_content: bool = False,
    timeout: float = 30.0,
) -> Dict[str, Any]:
    """Call Tavily Search API.

    Parameters mirror Tavily docs. Returns the JSON response as a dict.
    https://docs.tavily.com/documentation/api-reference/endpoint/search
    """
    if not query or not query.strip():
        raise ValueError("query must be a non-empty string")

    api_key = _require_api_key()
    payload: Dict[str, Any] = {
        "api_key": api_key,
        "query": query.strip(),
        "search_depth": search_depth,
        "max_results": max(1, int(max_results)),
        "include_answer": bool(include_answer),
        "include_images": bool(include_images),
        "include_raw_content": bool(include_raw_content),
    }
    if include_domains is not None:
        payload["include_domains"] = list(include_domains)
    if exclude_domains is not None:
        payload["exclude_domains"] = list(exclude_domains)

    return _post("/search", payload, timeout=timeout)
