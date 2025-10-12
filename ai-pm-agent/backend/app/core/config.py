import os
from dataclasses import dataclass
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(usecwd=True))

@dataclass
class Settings:
    env: str = os.getenv("ENV", "development")

    # LLM + Search
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    tavily_api_key: str | None = os.getenv("TAVILY_API_KEY")

    # Mastra Orchestrator
    mastra_base_url: str = os.getenv("MASTRA_BASE_URL", "http://localhost:8787")
    mastra_api_key: str | None = os.getenv("MASTRA_API_KEY")

    # Supabase (PgVector)
    supabase_url: str | None = os.getenv("SUPABASE_URL")
    supabase_key: str | None = os.getenv("SUPABASE_ANON_KEY")
    # names used below; change if your schema differs
    rag_table: str = os.getenv("RAG_TABLE", "tavily_context")
    rag_match_rpc: str = os.getenv("RAG_MATCH_RPC", "match_tavily")

settings = Settings()
