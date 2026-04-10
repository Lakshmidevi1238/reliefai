"""Chat API — AI assistant powered by RAG + OpenAI."""
import logging
from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.workflow.rag_pipeline import rag_query, direct_llm_response

router = APIRouter()
logger = logging.getLogger(__name__)


class ChatMessage(BaseModel):
    message: str
    history: Optional[List[dict]] = []


@router.post("/message")
async def chat_message(request: ChatMessage):
    """Process a chat message and return an AI assistant response."""
    try:
        # Build a compact conversation context from recent history
        history_ctx = ""
        if request.history:
            for msg in request.history[-4:]:
                role = "User" if msg.get("role") == "user" else "Assistant"
                history_ctx += f"{role}: {msg.get('content', '')}\n"

        full_query = (
            f"Conversation so far:\n{history_ctx}\nUser: {request.message}"
            if history_ctx
            else request.message
        )

        response = rag_query(full_query)
        return {"response": response, "success": True}

    except Exception as exc:
        logger.error("Chat error: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/suggestions")
async def get_suggestions():
    """Return quick-start chat suggestion prompts."""
    return {
        "suggestions": [
            "How can I help people in Sudan?",
            "What is most urgently needed in Gaza?",
            "Which organizations are most trustworthy for Ukraine donations?",
            "What can I donate physically?",
            "How does my donation actually reach people?",
        ]
    }
