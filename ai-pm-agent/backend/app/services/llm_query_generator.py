from __future__ import annotations

import json
import re
from typing import Dict, List

from ..core.config import settings

try:
    from openai import OpenAI  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    OpenAI = None  # type: ignore


TARGET_COUNT = 5

SYSTEM_INSTRUCTIONS = (
    "You are a helpful product research assistant for a PM."
)


def _build_prompt(transcript: str) -> str:
    return (
        "Given this interview transcript, list the 5 most relevant search queries "
        "that would help a product manager at Tavily (a search API company that provides AI optimized search solutions for AI agents) research solutions or validation for the problems mentioned. "
        "For each query, also create 1 competitor-oriented variant (e.g., 'competitors dealing with ___').\n"
        "Return JSON [{user_query, competitor_query}] with exactly 5 items, no extra commentary.\n\n"
        f"Transcript:\n{transcript.strip()}"
    )


def _parse_json_response(text: str) -> List[Dict[str, str]]:
    # Try direct JSON
    try:
        data = json.loads(text)
        if isinstance(data, list):
            return _normalize_items(data)
    except Exception:
        pass

    # Try to extract from fenced code block
    match = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if match:
        try:
            data = json.loads(match.group(1))
            if isinstance(data, list):
                return _normalize_items(data)
        except Exception:
            pass

    # Last resort: try to find JSON-like array
    match = re.search(r"\[(?:.|\n)*\]", text)
    if match:
        try:
            data = json.loads(match.group(0))
            if isinstance(data, list):
                return _normalize_items(data)
        except Exception:
            pass

    return []


def _normalize_items(items: List[dict]) -> List[Dict[str, str]]:
    normalized: List[Dict[str, str]] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        uq = str(item.get("user_query", "")).strip()
        cq = str(item.get("competitor_query", "")).strip()
        if uq and cq:
            normalized.append({"user_query": uq, "competitor_query": cq})
        if len(normalized) >= TARGET_COUNT:
            break
    return normalized


def _openai_generate(transcript: str) -> List[Dict[str, str]]:
    if not (settings.openai_api_key and OpenAI):
        return []
    try:
        client = OpenAI(api_key=settings.openai_api_key)
        prompt = _build_prompt(transcript)
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_INSTRUCTIONS},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )
        text = resp.choices[0].message.content or ""
        parsed = _parse_json_response(text)
        return parsed[:TARGET_COUNT]
    except Exception:
        return []


def generate_queries(transcript: str) -> List[Dict[str, str]]:
    """Generate 5 pairs of search prompts from a transcript via OpenAI.

    Returns a list of dicts: [{"user_query": str, "competitor_query": str}].
    No heuristic fallback; requires a valid OpenAI setup.
    """
    if not transcript or not transcript.strip():
        return []

    return _openai_generate(transcript)
