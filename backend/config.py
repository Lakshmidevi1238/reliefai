"""
ReliefLink AI — Backend Configuration
Loads environment variables and exposes typed config constants.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ── Core API Keys ────────────────────────────────────────────
OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
NEWS_API_KEY: str = os.getenv("NEWS_API_KEY", "")
LANGCHAIN_API_KEY: str = os.getenv("LANGCHAIN_API_KEY", "")

# ── LangSmith Observability ──────────────────────────────────
LANGCHAIN_TRACING_V2: str = os.getenv("LANGCHAIN_TRACING_V2", "false")
LANGCHAIN_PROJECT: str = os.getenv("LANGCHAIN_PROJECT", "relieflink-ai")

# ── Service URLs ─────────────────────────────────────────────
BACKEND_URL: str = os.getenv("BACKEND_URL", "http://localhost:8000")

# ── OpenAI Model Settings ────────────────────────────────────
OPENAI_CHAT_MODEL: str = "gpt-3.5-turbo"
OPENAI_EMBEDDING_MODEL: str = "text-embedding-ada-002"

# ── Apply LangSmith Env Vars if key is present ───────────────
if LANGCHAIN_API_KEY:
    os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY
    os.environ["LANGCHAIN_TRACING_V2"] = LANGCHAIN_TRACING_V2
    os.environ["LANGCHAIN_PROJECT"] = LANGCHAIN_PROJECT
