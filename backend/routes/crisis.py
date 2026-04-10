"""Crisis API — fetch, process, and serve the live crisis feed."""
import logging
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address

from backend.workflow.langgraph_pipeline import run_crisis_pipeline, get_current_feed
from backend.data.sample_data import get_sample_crises

router = APIRouter()
logger = logging.getLogger(__name__)
limiter = Limiter(key_func=get_remote_address)


class ProcessRequest(BaseModel):
    region: str = "global"


@router.post("/process")
@limiter.limit("5/minute")           # ← rate limit: prevent OpenAI budget exhaustion
async def process_crisis(request: Request, body: ProcessRequest):
    """Trigger LangGraph pipeline: fetch → analyze → embed → output."""
    try:
        result = await run_crisis_pipeline(region=body.region)
        return result
    except Exception as exc:
        logger.error("Crisis process error: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/feed")
@limiter.limit("30/minute")
async def get_crisis_feed(request: Request):
    """Return the current in-memory crisis feed (with sample data fallback)."""
    feed = get_current_feed()
    if not feed:
        feed = get_sample_crises()
    return {"feed": feed, "count": len(feed)}


@router.get("/regions")
async def get_regions():
    """Return a list of known crisis regions."""
    regions = [
        "Global", "Sudan", "Gaza", "Ukraine", "Haiti",
        "Syria", "Yemen", "Ethiopia", "Somalia", "Pakistan",
        "Turkey", "Libya", "Afghanistan", "Myanmar", "DRC",
    ]
    return {"regions": regions}
