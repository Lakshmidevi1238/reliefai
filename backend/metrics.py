"""
ReliefLink AI — Prometheus Business Metrics

Defines application-level counters, histograms, and gauges.
Imported by route handlers and pipeline nodes to emit telemetry.
The /metrics endpoint is exposed by prometheus-fastapi-instrumentator in main.py.
"""
from prometheus_client import Counter, Histogram, Gauge

# ── Pipeline Metrics ─────────────────────────────────────────────────────────
crisis_pipeline_runs_total = Counter(
    "crisis_pipeline_runs_total",
    "Total number of crisis pipeline invocations",
    ["region", "success"],
)

crisis_pipeline_duration_seconds = Histogram(
    "crisis_pipeline_duration_seconds",
    "End-to-end duration of the LangGraph crisis pipeline",
    buckets=[1, 5, 10, 20, 30, 60, 90, 120],
)

# ── LLM Metrics ──────────────────────────────────────────────────────────────
llm_calls_total = Counter(
    "llm_calls_total",
    "Total number of LLM API calls made",
    ["model", "operation", "success"],
)

llm_call_duration_seconds = Histogram(
    "llm_call_duration_seconds",
    "Duration of individual LLM API calls",
    ["model", "operation"],
    buckets=[0.5, 1, 2, 5, 10, 20, 30],
)

# ── FAISS / Data Metrics ─────────────────────────────────────────────────────
faiss_document_count = Gauge(
    "faiss_document_count",
    "Current number of documents indexed in the FAISS vector store",
)

# ── Help Request Metrics ──────────────────────────────────────────────────────
help_requests_submitted_total = Counter(
    "help_requests_submitted_total",
    "Total number of help requests submitted via the platform",
    ["trust_level"],
)

# ── RAG Metrics ───────────────────────────────────────────────────────────────
rag_queries_total = Counter(
    "rag_queries_total",
    "Total RAG queries executed",
    ["source", "success"],          # source: "faiss" | "direct_llm"
)

rag_query_duration_seconds = Histogram(
    "rag_query_duration_seconds",
    "Duration of RAG query (retrieve + generate)",
    buckets=[0.5, 1, 2, 5, 10, 20],
)
