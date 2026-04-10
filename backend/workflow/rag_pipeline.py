"""
ReliefLink AI — RAG Pipeline (LangChain + FAISS + OpenAI)

Provides:
- rag_query()              — FAISS-grounded Q&A (LCEL chain)
- direct_llm_response()    — Fallback LLM call without retrieval
- generate_region_analysis() — Structured donor-hub analysis
- generate_awareness_blog()  — Full awareness blog post
- generate_trust_score()     — Simulated trust scoring
"""
import logging
import time
from typing import Optional

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.messages import SystemMessage, HumanMessage

from backend.config import OPENAI_API_KEY, OPENAI_CHAT_MODEL
from backend.data import faiss_store
from backend.metrics import (
    llm_calls_total,
    llm_call_duration_seconds,
    rag_queries_total,
    rag_query_duration_seconds,
)

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────
def _format_docs(docs) -> str:
    return "\n\n---\n\n".join(doc.page_content for doc in docs)


def _get_llm(temperature: float = 0.3, max_tokens: int = 450) -> Optional[ChatOpenAI]:
    """Return a ChatOpenAI instance if the API key is configured, else None."""
    if not OPENAI_API_KEY:
        return None
    return ChatOpenAI(
        model=OPENAI_CHAT_MODEL,
        api_key=OPENAI_API_KEY,
        temperature=temperature,
        max_tokens=max_tokens,
    )


# ─────────────────────────────────────────────────────────────────────────────
# RAG Query — LCEL Chain (LangSmith-traced)
# ─────────────────────────────────────────────────────────────────────────────
_RAG_PROMPT = ChatPromptTemplate.from_template(
    """You are ReliefLink AI, an expert humanitarian crisis response assistant.
Use the following real-time crisis context to answer the question accurately and helpfully.

CRISIS CONTEXT:
{context}

USER QUESTION:
{question}

INSTRUCTIONS:
- Be specific and actionable
- Mention trusted organizations when relevant
- Provide concrete steps users can take
- Be empathetic, clear, and concise (3–5 sentences)

RESPONSE:"""
)


def rag_query(query: str) -> str:
    """Perform a RAG query: retrieve from FAISS then generate with OpenAI."""
    if not OPENAI_API_KEY:
        return (
            "⚠️ OpenAI API key not configured. "
            "Add OPENAI_API_KEY to your .env file to enable AI responses."
        )

    retriever = faiss_store.get_retriever(k=4)
    if retriever is None:
        logger.info("FAISS not initialised — falling back to direct LLM.")
        return direct_llm_response(query)

    t0 = time.perf_counter()
    try:
        llm = _get_llm(temperature=0.3)
        chain = (
            {"context": retriever | _format_docs, "question": RunnablePassthrough()}
            | _RAG_PROMPT
            | llm
            | StrOutputParser()
        )
        result = chain.invoke(query)
        duration = time.perf_counter() - t0
        rag_queries_total.labels(source="faiss", success="true").inc()
        rag_query_duration_seconds.observe(duration)
        llm_calls_total.labels(
            model=OPENAI_CHAT_MODEL, operation="rag_query", success="true"
        ).inc()
        llm_call_duration_seconds.labels(
            model=OPENAI_CHAT_MODEL, operation="rag_query"
        ).observe(duration)
        return result

    except Exception as exc:
        duration = time.perf_counter() - t0
        logger.error("RAG chain error (%.2fs): %s — falling back to direct LLM.", duration, exc)
        rag_queries_total.labels(source="faiss", success="false").inc()
        llm_calls_total.labels(
            model=OPENAI_CHAT_MODEL, operation="rag_query", success="false"
        ).inc()
        return direct_llm_response(query)


# ─────────────────────────────────────────────────────────────────────────────
# Direct LLM Fallback
# ─────────────────────────────────────────────────────────────────────────────
_SYSTEM_PROMPT = (
    "You are ReliefLink AI, a compassionate and knowledgeable humanitarian crisis assistant. "
    "Help users understand crisis situations, find donation opportunities, and take meaningful action. "
    "Be specific, empathetic, and actionable."
)


def direct_llm_response(query: str, context: str = "") -> str:
    """Call OpenAI directly without RAG retrieval."""
    llm = _get_llm(temperature=0.5, max_tokens=450)
    if llm is None:
        return "⚠️ OpenAI API key not configured."

    user_content = f"Context:\n{context}\n\nQuestion: {query}" if context else query
    messages = [SystemMessage(content=_SYSTEM_PROMPT), HumanMessage(content=user_content)]

    t0 = time.perf_counter()
    try:
        response = llm.invoke(messages)
        duration = time.perf_counter() - t0
        llm_calls_total.labels(
            model=OPENAI_CHAT_MODEL, operation="direct_llm", success="true"
        ).inc()
        llm_call_duration_seconds.labels(
            model=OPENAI_CHAT_MODEL, operation="direct_llm"
        ).observe(duration)
        rag_queries_total.labels(source="direct_llm", success="true").inc()
        return response.content

    except Exception as exc:
        duration = time.perf_counter() - t0
        logger.error("Direct LLM error (%.2fs): %s", duration, exc)
        llm_calls_total.labels(
            model=OPENAI_CHAT_MODEL, operation="direct_llm", success="false"
        ).inc()
        rag_queries_total.labels(source="direct_llm", success="false").inc()
        return f"⚠️ AI response error: {exc}. Please check your API key and try again."


# ─────────────────────────────────────────────────────────────────────────────
# Region Analysis (Donor Hub)
# ─────────────────────────────────────────────────────────────────────────────
def generate_region_analysis(region: str, donation_data: dict) -> str:
    """Generate a structured crisis analysis for the Donor Hub."""
    if not OPENAI_API_KEY:
        return "🔑 OpenAI API key required for AI analysis."

    context = ""
    if faiss_store.is_initialized():
        docs = faiss_store.similarity_search(f"humanitarian crisis in {region}", k=4)
        context = _format_docs(docs)
    if not context:
        context = f"Ongoing humanitarian crisis in {region} requiring urgent international aid."

    prompt = f"""Based on the following crisis context for {region}, provide a structured analysis for potential donors.

CRISIS CONTEXT:
{context}

Generate a clear, structured analysis with these exact sections:

## 🔴 Current Situation
2–3 sentences describing what is happening right now in {region}.

## ⚠️ Most Urgent Needs
List the 4–5 most critical needs currently facing people in {region}.

## 💡 How Your Donation Helps
2–3 specific ways that a monetary donation makes a difference, with impact numbers where possible.

## 🎯 Recommended Action Steps
3 concrete steps a donor can take right now to help the people in {region}.

Keep the tone urgent but hopeful. Be specific and factual."""

    return direct_llm_response(prompt, context)


# ─────────────────────────────────────────────────────────────────────────────
# Blog Generator
# ─────────────────────────────────────────────────────────────────────────────
def generate_awareness_blog(region: str) -> str:
    """Generate a comprehensive AI awareness blog post for a crisis region."""
    if not OPENAI_API_KEY:
        return "🔑 OpenAI API key required for blog generation."

    context = ""
    if faiss_store.is_initialized():
        docs = faiss_store.similarity_search(f"humanitarian crisis {region}", k=5)
        context = _format_docs(docs)
    if not context:
        context = f"The ongoing humanitarian crisis in {region} has affected millions of people."

    prompt = f"""Write a comprehensive, emotionally resonant, and factually accurate awareness blog post \
for ReliefLink AI about the humanitarian crisis in {region}.

REAL-TIME CONTEXT:
{context}

Structure the blog EXACTLY as follows (use markdown headings):

# [Write a compelling, specific headline about the {region} crisis]

## The Crisis at a Glance
[Key statistics in a compelling opening paragraph — who is affected, how many, since when]

## What Is Happening Right Now in {region}
[2–3 paragraphs describing the current humanitarian situation with specific details]

## Who Is Being Affected
[Describe the human face of the crisis — families, children, elderly, specific communities]

## What Is Urgently Needed
[Specific breakdown of the top 5 resources most needed right now]

## The Timeline: How This Crisis Developed
[Brief but informative historical context — what led to this crisis]

## How You Can Make a Real Difference Today
[4–5 specific, actionable steps a reader can take right now]

## Trusted Organizations on the Ground
[Name and describe 3–4 reputable organizations working in {region} with donation links]

---
*This article was generated by ReliefLink AI using real-time crisis data. All figures are sourced from UN agencies and humanitarian organisations.*

Write with urgency, empathy, and clarity. Use specific numbers and examples to make the impact tangible."""

    # Pass context separately so direct_llm_response can include it in the prompt
    return direct_llm_response(prompt, context)


# ─────────────────────────────────────────────────────────────────────────────
# Trust Scoring (Simulated)
# ─────────────────────────────────────────────────────────────────────────────
def generate_trust_score(request_data: dict) -> dict:
    """
    Compute a simulated trust score for a help request submission.
    Scoring is rule-based and transparent.

    Weights:
      - has_documents  : +30  (strongest signal of legitimacy)
      - contact_email  : +12  (valid email format required)
      - donation_link  : +8   (must start with http)
      - bank_details   : +5
      - description    : +5 if >300 chars, +2 if >150 chars
      - base           : 40
    """
    score = 40  # Base

    if request_data.get("has_documents"):
        score += 30
    if request_data.get("contact_email") and "@" in str(request_data.get("contact_email", "")):
        score += 12
    if request_data.get("donation_link", "").startswith("http"):
        score += 8
    if request_data.get("bank_details"):
        score += 5
    desc_len = len(request_data.get("description", ""))
    if desc_len > 300:
        score += 5
    elif desc_len > 150:
        score += 2

    score = min(score, 100)

    if score >= 80:
        level, badge, color = "High",   "✅ AI Verified",        "#22c55e"
    elif score >= 60:
        level, badge, color = "Medium", "⚠️ Partially Verified", "#f59e0b"
    else:
        level, badge, color = "Low",    "🔍 Under Review",       "#ef4444"

    return {
        "score":      score,
        "level":      level,
        "badge":      badge,
        "color":      color,
        "confidence": f"{score}%",
    }
