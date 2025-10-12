import os
from typing import List
from ..core.config import settings

# OpenAI python >=1.0
from openai import OpenAI
_client = OpenAI(api_key=settings.openai_api_key)

# choose a stable embeddings model
_EMBED_MODEL = os.getenv("EMBED_MODEL", "text-embedding-3-small")

async def embed_text(text: str) -> List[float]:
    # sync API; fine to call directly (FastAPI route is async)
    resp = _client.embeddings.create(model=_EMBED_MODEL, input=text)
    return resp.data[0].embedding
