"""
ReliefLink AI — LangGraph Workflow Pipeline

Graph:  fetch_news → analyze → classify_urgency → extract_needs → embed_store → generate_output → END

Each node is a pure function that receives and returns the full CrisisState TypedDict.
The compiled graph is exposed as `crisis_workflow` and `run_crisis_pipeline()`.
"""
import json
import logging
import requests as http_requests
from datetime import datetime
from typing import TypedDict, List, Optional

from langgraph.graph import StateGraph, END
from langchain.schema import Document
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from backend.config import OPENAI_API_KEY, NEWS_API_KEY, OPENAI_CHAT_MODEL
from backend.data import sample_data
from backend.data import faiss_store as faiss_module
from backend.metrics import (
    crisis_pipeline_runs_total,
    crisis_pipeline_duration_seconds,
    llm_calls_total,
    llm_call_duration_seconds,
    faiss_document_count,
)

logger = logging.getLogger(__name__)

# Pipeline constants
MAX_ARTICLES_PER_RUN = 6
MAX_CHAT_HISTORY = 4

# ─────────────────────────────────────────────────────────────────────────────
# State Definition
# ─────────────────────────────────────────────────────────────────────────────
class CrisisState(TypedDict):
    region: str
    raw_articles: List[dict]
    analyzed_crises: List[dict]
    crisis_feed: List[dict]        # ← was missing from TypedDict (Bug #2 fix)
    error: Optional[str]


# ── In-memory live feed (populated after each pipeline run) ──
_current_crisis_feed: List[dict] = []


def get_current_feed() -> List[dict]:
    return _current_crisis_feed


# ─────────────────────────────────────────────────────────────────────────────
# Node 1 — Fetch News
# ─────────────────────────────────────────────────────────────────────────────
def fetch_news_node(state: CrisisState) -> CrisisState:
    """Fetch crisis articles from NewsAPI or fall back to sample data."""
    region = state.get("region", "global")
    articles: List[dict] = []

    if NEWS_API_KEY:
        try:
            query = (
                "humanitarian crisis disaster flood earthquake famine conflict"
                if region.lower() == "global"
                else f"humanitarian crisis {region} disaster aid"
            )
            url = (
                f"https://newsapi.org/v2/everything"
                f"?q={query}&language=en&sortBy=publishedAt"
                f"&pageSize=10&apiKey={NEWS_API_KEY}"
            )
            resp = http_requests.get(url, timeout=10)
            resp.raise_for_status()
            articles = resp.json().get("articles", [])[:8]
            logger.info("Fetched %d articles from NewsAPI for region=%s.", len(articles), region)
        except http_requests.exceptions.HTTPError as exc:
            logger.warning("NewsAPI HTTP error: %s — using sample data.", exc)
        except http_requests.exceptions.RequestException as exc:
            logger.warning("NewsAPI request failed: %s — using sample data.", exc)

    if not articles:
        articles = sample_data.get_sample_articles(region)
        logger.info(
            "Using %d sample articles for region=%s (source=sample_data).",
            len(articles), region,
        )

    return {**state, "raw_articles": articles}


# ─────────────────────────────────────────────────────────────────────────────
# Node 2 — Analyze Crisis  (now uses LangChain ChatOpenAI → traced by LangSmith)
# ─────────────────────────────────────────────────────────────────────────────
CRISIS_SYSTEM_PROMPT = """You are a humanitarian crisis analyst. Given a news article extract:
1. crisis_type: e.g. "Armed Conflict", "Natural Disaster", "Famine", "Disease Outbreak"
2. region: country or region name
3. people_affected: number as string (e.g. "5 million")
4. needs: JSON array of strings (max 5), e.g. ["food", "water", "medical aid", "shelter"]
5. urgency: "High", "Medium", or "Low"
6. summary: 2–3 sentence factual summary

Respond with ONLY valid JSON matching these keys exactly. No markdown, no extra text."""


def _build_fallback_crisis(state: CrisisState, title: str, desc: str) -> dict:
    """Return a safe default crisis dict when the LLM response cannot be parsed."""
    return {
        "crisis_type": "Humanitarian Crisis",
        "region": state.get("region", "Unknown"),
        "people_affected": "Unknown",
        "needs": ["food", "water", "medical aid"],
        "urgency": "High",
        "summary": desc[:250] if desc else title,
    }


def _strip_code_fences(text: str) -> str:
    """Remove markdown ```json ... ``` fences from LLM output."""
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return text.strip()


def analyze_crisis_node(state: CrisisState) -> CrisisState:
    """
    Use LangChain ChatOpenAI to extract structured crisis metadata from raw articles.
    Using ChatOpenAI (vs raw OpenAI SDK) ensures all calls appear in LangSmith traces.
    """
    articles = state.get("raw_articles", [])
    if not articles:
        return {**state, "analyzed_crises": []}

    if not OPENAI_API_KEY:
        logger.warning("No OpenAI key — returning sample crises.")
        return {
            **state,
            "analyzed_crises": sample_data.get_sample_crises(state.get("region", "global")),
        }

    llm = ChatOpenAI(
        model=OPENAI_CHAT_MODEL,
        api_key=OPENAI_API_KEY,
        max_tokens=350,
        temperature=0.2,
    )
    analyzed: List[dict] = []

    for article in articles[:MAX_ARTICLES_PER_RUN]:
        title = article.get("title", "")
        desc = article.get("description") or ""
        content = f"{title}. {desc}"

        import time as _time
        t0 = _time.perf_counter()
        try:
            response = llm.invoke(
                [
                    SystemMessage(content=CRISIS_SYSTEM_PROMPT),
                    HumanMessage(content=f"Analyze: {content}"),
                ]
            )
            duration = _time.perf_counter() - t0
            llm_calls_total.labels(
                model=OPENAI_CHAT_MODEL, operation="analyze_crisis", success="true"
            ).inc()
            llm_call_duration_seconds.labels(
                model=OPENAI_CHAT_MODEL, operation="analyze_crisis"
            ).observe(duration)

            text = _strip_code_fences(response.content.strip())
            result = json.loads(text)

        except json.JSONDecodeError as exc:
            logger.warning(
                "LLM returned invalid JSON for article '%s': %s",
                title[:40], exc,
            )
            llm_calls_total.labels(
                model=OPENAI_CHAT_MODEL, operation="analyze_crisis", success="parse_error"
            ).inc()
            result = _build_fallback_crisis(state, title, desc)

        except Exception as exc:
            duration = _time.perf_counter() - t0
            logger.error(
                "LLM API error for article '%s': %s (%.2fs)",
                title[:40], exc, duration,
            )
            llm_calls_total.labels(
                model=OPENAI_CHAT_MODEL, operation="analyze_crisis", success="false"
            ).inc()
            result = _build_fallback_crisis(state, title, desc)

        result["title"] = title
        result["source"] = (article.get("source") or {}).get("name", "News Source")
        result["url"] = article.get("url", "#")
        result["published_at"] = article.get("publishedAt", datetime.now().isoformat())
        analyzed.append(result)

    if not analyzed:
        analyzed = sample_data.get_sample_crises(state.get("region", "global"))

    return {**state, "analyzed_crises": analyzed}


# ─────────────────────────────────────────────────────────────────────────────
# Node 3 — Classify Urgency
# ─────────────────────────────────────────────────────────────────────────────
def classify_urgency_node(state: CrisisState) -> CrisisState:
    """Normalise urgency field and add colour coding."""
    urgency_colors = {"High": "#ef4444", "Medium": "#f59e0b", "Low": "#22c55e"}
    crises = state.get("analyzed_crises", [])

    for crisis in crises:
        raw_urgency = str(crisis.get("urgency", "Medium")).strip().capitalize()
        if raw_urgency not in urgency_colors:
            n = len(crisis.get("needs", []))
            raw_urgency = "High" if n >= 4 else ("Medium" if n >= 2 else "Low")
        crisis["urgency"] = raw_urgency
        crisis["urgency_color"] = urgency_colors[raw_urgency]

    return {**state, "analyzed_crises": crises}


# ─────────────────────────────────────────────────────────────────────────────
# Node 4 — Extract & Normalise Needs
# ─────────────────────────────────────────────────────────────────────────────
_NEED_KEYWORDS = {
    "food":      ["food", "nutrition", "hunger", "famine", "meal", "starvation"],
    "water":     ["water", "sanitation", "hygiene", "clean water", "sewage"],
    "medical":   ["medical", "medicine", "healthcare", "hospital", "doctor", "wounded", "injury", "health"],
    "shelter":   ["shelter", "housing", "refugee", "camp", "displacement", "tent"],   # ← removed duplicate "housing"
    "clothing":  ["clothing", "clothes", "warm", "blankets", "winter"],
    "financial": ["funding", "financial", "money", "donation", "aid", "cash"],
    "education": ["school", "education", "children", "learning", "teachers"],
}


def extract_needs_node(state: CrisisState) -> CrisisState:
    """Normalise the needs field to a controlled vocabulary list."""
    crises = state.get("analyzed_crises", [])
    for crisis in crises:
        raw_needs = crisis.get("needs", [])
        if isinstance(raw_needs, str):
            raw_needs = [n.strip() for n in raw_needs.split(",")]
        normalised: List[str] = []
        for need in raw_needs:
            need_lower = need.lower()
            matched = False
            for cat, keywords in _NEED_KEYWORDS.items():
                if any(kw in need_lower for kw in keywords):
                    if cat not in normalised:
                        normalised.append(cat)
                    matched = True
                    break
            if not matched and need not in normalised:
                normalised.append(need.lower().strip())
        crisis["needs"] = normalised[:5]
    return {**state, "analyzed_crises": crises}


# ─────────────────────────────────────────────────────────────────────────────
# Node 5 — Embed and Store in FAISS
# ─────────────────────────────────────────────────────────────────────────────
def embed_store_node(state: CrisisState) -> CrisisState:
    """Convert crisis data to LangChain Documents and add to FAISS."""
    crises = state.get("analyzed_crises", [])
    if not OPENAI_API_KEY or not crises:
        return state

    documents: List[Document] = [
        Document(
            page_content=(
                f"Crisis Title: {c.get('title', '')}\n"
                f"Region: {c.get('region', '')}\n"
                f"Type: {c.get('crisis_type', '')}\n"
                f"Summary: {c.get('summary', '')}\n"
                f"Urgent Needs: {', '.join(c.get('needs', []))}\n"
                f"Urgency Level: {c.get('urgency', '')}\n"
                f"People Affected: {c.get('people_affected', '')}\n"
            ),
            metadata={
                "region": c.get("region", ""),
                "urgency": c.get("urgency", ""),
                "crisis_type": c.get("crisis_type", ""),
            },
        )
        for c in crises
    ]

    success = faiss_module.add_documents(documents)
    if success:
        doc_count = faiss_module.document_count()
        faiss_document_count.set(doc_count)
        logger.info(
            "Stored %d crisis documents in FAISS (total=%d).",
            len(documents), doc_count,
        )
    return state


# ─────────────────────────────────────────────────────────────────────────────
# Node 6 — Generate Formatted Output
# ─────────────────────────────────────────────────────────────────────────────
def generate_output_node(state: CrisisState) -> CrisisState:
    """Format the final crisis feed and persist to module-level cache."""
    global _current_crisis_feed
    crises = state.get("analyzed_crises", [])

    feed: List[dict] = [
        {
            "title":           c.get("title", "Crisis Alert"),
            "region":          c.get("region", "Unknown"),
            "crisis_type":     c.get("crisis_type", "Humanitarian Crisis"),
            "summary":         c.get("summary", ""),
            "needs":           c.get("needs", []),
            "urgency":         c.get("urgency", "Medium"),
            "urgency_color":   c.get("urgency_color", "#f59e0b"),
            "people_affected": c.get("people_affected", "Unknown"),
            "source":          c.get("source", ""),
            "url":             c.get("url", "#"),
            "published_at":    c.get("published_at", ""),
        }
        for c in crises
    ]

    _current_crisis_feed = feed
    logger.info("Generated crisis feed with %d entries.", len(feed))
    return {**state, "crisis_feed": feed}


# ─────────────────────────────────────────────────────────────────────────────
# Build & Compile the LangGraph Workflow
# ─────────────────────────────────────────────────────────────────────────────
def _build_workflow() -> StateGraph:
    wf = StateGraph(CrisisState)
    wf.add_node("fetch_news",       fetch_news_node)
    wf.add_node("analyze",          analyze_crisis_node)
    wf.add_node("classify_urgency", classify_urgency_node)
    wf.add_node("extract_needs",    extract_needs_node)
    wf.add_node("embed_store",      embed_store_node)
    wf.add_node("generate_output",  generate_output_node)

    wf.set_entry_point("fetch_news")
    wf.add_edge("fetch_news",       "analyze")
    wf.add_edge("analyze",          "classify_urgency")
    wf.add_edge("classify_urgency", "extract_needs")
    wf.add_edge("extract_needs",    "embed_store")
    wf.add_edge("embed_store",      "generate_output")
    wf.add_edge("generate_output",  END)
    return wf


crisis_workflow = _build_workflow().compile()


async def run_crisis_pipeline(region: str = "global") -> dict:
    """Invoke the full LangGraph crisis processing pipeline asynchronously."""
    import time as _time
    t0 = _time.perf_counter()
    try:
        initial_state: CrisisState = {
            "region": region,
            "raw_articles": [],
            "analyzed_crises": [],
            "crisis_feed": [],
            "error": None,
        }
        with crisis_pipeline_duration_seconds.time():
            result = await crisis_workflow.ainvoke(initial_state)

        feed = result.get("crisis_feed", [])
        crisis_pipeline_runs_total.labels(region=region, success="true").inc()
        logger.info(
            "Crisis pipeline completed",
            extra={"region": region, "crisis_count": len(feed), "duration_s": round(_time.perf_counter() - t0, 2)},
        )
        return {"success": True, "region": region, "crisis_count": len(feed), "feed": feed}

    except Exception as exc:
        crisis_pipeline_runs_total.labels(region=region, success="false").inc()
        logger.error(
            "Crisis pipeline failed",
            extra={"region": region, "error": str(exc), "duration_s": round(_time.perf_counter() - t0, 2)},
        )
        return {"success": False, "error": str(exc), "feed": [], "crisis_count": 0}
