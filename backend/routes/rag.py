"""RAG API — query the knowledge base, analyse regions, generate blog posts."""
import logging
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address

from backend.workflow.rag_pipeline import (
    rag_query,
    generate_region_analysis,
    generate_awareness_blog,
)
from backend.data.sample_data import get_donation_info

router = APIRouter()
logger = logging.getLogger(__name__)
limiter = Limiter(key_func=get_remote_address)


class QueryRequest(BaseModel):
    query: str


class RegionRequest(BaseModel):
    region: str


@router.post("/query")
@limiter.limit("20/minute")
async def query_knowledge_base(request: Request, body: QueryRequest):
    """RAG query against FAISS-indexed crisis knowledge base."""
    try:
        response = rag_query(body.query)
        return {"response": response, "source": "rag"}
    except Exception as exc:
        logger.error("RAG query error: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/analyze")
@limiter.limit("10/minute")
async def analyze_region(request: Request, body: RegionRequest):
    """Return AI analysis + donation info for a specific region."""
    try:
        donation_data = get_donation_info(body.region)
        analysis = generate_region_analysis(body.region, donation_data)
        return {
            "region":        body.region,
            "analysis":      analysis,
            "donation_info": donation_data,
        }
    except Exception as exc:
        logger.error("Region analysis error: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/blog")
@limiter.limit("5/minute")
async def generate_blog(request: Request, body: RegionRequest):
    """Generate an AI-powered awareness blog post for a crisis region."""
    try:
        blog = generate_awareness_blog(body.region)
        return {"region": body.region, "blog": blog}
    except Exception as exc:
        logger.error("Blog generation error: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc))
