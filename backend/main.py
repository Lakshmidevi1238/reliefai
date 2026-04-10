"""
ReliefLink AI — FastAPI Application Entry Point

Run with:
  uvicorn backend.main:app --reload --port 8000
"""
import os
import time
import logging
import uvicorn
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from prometheus_fastapi_instrumentator import Instrumentator

from backend.logging_config import configure_logging
from backend.routes import crisis, rag, help, chat
from backend.config import OPENAI_API_KEY, NEWS_API_KEY, LANGCHAIN_API_KEY

# ── Configure structured logging (must run before any logger.xxx call) ───────
configure_logging()
logger = logging.getLogger(__name__)

# ── Rate Limiter ──────────────────────────────────────────────────────────────
limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])


# ── Lifespan (replaces deprecated @app.on_event) ─────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── Startup ──
    logger.info("=" * 60)
    logger.info("ReliefLink AI Backend — Starting Up")
    logger.info("OpenAI:    %s", "Configured" if OPENAI_API_KEY else "Not set — using fallbacks")
    logger.info("NewsAPI:   %s", "Configured" if NEWS_API_KEY else "Not set — using sample data")
    logger.info("LangSmith: %s", "Configured" if LANGCHAIN_API_KEY else "Disabled")
    logger.info("Docs:      http://localhost:8000/docs")
    logger.info("Metrics:   http://localhost:8000/metrics")
    logger.info("=" * 60)
    yield
    # ── Shutdown ──
    logger.info("ReliefLink AI Backend — Shutting Down")


# ── FastAPI App ───────────────────────────────────────────────────────────────
app = FastAPI(
    title="ReliefLink AI API",
    description=(
        "AI-powered crisis awareness and trusted donation platform. "
        "Backed by LangGraph workflows, LangChain RAG, and FAISS vector search."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# ── Attach rate-limiter state and error handler ───────────────────────────────
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ── CORS — restrict to known origins only ────────────────────────────────────
_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:8501,http://127.0.0.1:8501",
    ).split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

# ── Prometheus — auto-instrument all HTTP routes ──────────────────────────────
Instrumentator(
    should_group_status_codes=True,
    excluded_handlers=["/metrics", "/health", "/docs", "/redoc", "/openapi.json"],
).instrument(app).expose(app, endpoint="/metrics", tags=["Observability"])

# ── HTTP Request Logging Middleware ───────────────────────────────────────────
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000
    logger.info(
        "HTTP request completed",
        extra={
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": round(duration_ms, 2),
            "client_ip": request.client.host if request.client else "unknown",
        },
    )
    return response


# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(crisis.router, prefix="/api/crisis", tags=["Crisis Feed"])
app.include_router(rag.router,    prefix="/api/rag",    tags=["RAG / AI Analysis"])
app.include_router(help.router,   prefix="/api/help",   tags=["Help Requests"])
app.include_router(chat.router,   prefix="/api/chat",   tags=["AI Chat"])


# ── Root — no sensitive info exposed ─────────────────────────────────────────
@app.get("/", tags=["System"])
async def root():
    """Public root endpoint — returns basic app identity only."""
    return {
        "app": "ReliefLink AI",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "crisis_feed":       "/api/crisis/feed",
            "process_pipeline":  "/api/crisis/process",
            "rag_query":         "/api/rag/query",
            "region_analyze":    "/api/rag/analyze",
            "blog_generate":     "/api/rag/blog",
            "help_submit":       "/api/help/submit",
            "help_feed":         "/api/help/feed",
            "chat":              "/api/chat/message",
            "docs":              "/docs",
            "metrics":           "/metrics",
            "health":            "/health",
        },
    }


# ── Health — reflects true system state ──────────────────────────────────────
@app.get("/health", tags=["System"])
async def health():
    """
    Deep health check. Returns 200 + status=healthy when all subsystems are OK,
    or 200 + status=degraded (with per-subsystem detail) when something is wrong.
    """
    from backend.data.faiss_store import is_initialized, document_count

    checks: dict = {}
    overall = "healthy"

    # ── FAISS ──
    faiss_ok = is_initialized()
    faiss_docs = document_count()
    checks["faiss"] = {
        "status": "ok" if faiss_ok else "degraded",
        "documents": faiss_docs,
    }
    if not faiss_ok:
        overall = "degraded"

    # ── Config checks (no external calls) ──
    checks["openai"] = {
        "status": "ok" if OPENAI_API_KEY else "degraded",
        "configured": bool(OPENAI_API_KEY),
    }
    checks["newsapi"] = {
        "status": "ok" if NEWS_API_KEY else "degraded — using sample data",
        "configured": bool(NEWS_API_KEY),
    }
    checks["langsmith"] = {
        "status": "ok" if LANGCHAIN_API_KEY else "disabled",
        "configured": bool(LANGCHAIN_API_KEY),
    }
    if not OPENAI_API_KEY:
        overall = "degraded"

    return {
        "status": overall,
        "version": "1.0.0",
        "checks": checks,
    }


if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
