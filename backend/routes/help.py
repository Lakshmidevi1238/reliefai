"""Help Request API — submit, list, and upvote help requests."""
import uuid
import logging
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, field_validator, model_validator

from backend.workflow.rag_pipeline import generate_trust_score
from backend.data.sample_data import get_sample_help_requests
from backend.metrics import help_requests_submitted_total

router = APIRouter()
logger = logging.getLogger(__name__)

# In-memory store (user-submitted requests are prepended here)
_submitted_requests: List[dict] = []

# ── Request validation constants ──────────────────────────────────────────────
_MIN_DESC_LEN = 50
_MAX_DESC_LEN = 2000
_MAX_NAME_LEN = 120
_MAX_REGION_LEN = 100
_MAX_NEEDS = 10


class HelpRequest(BaseModel):
    name: str
    region: str
    description: str
    needs: List[str]
    contact_email: Optional[str] = None
    donation_link: Optional[str] = None
    bank_details: Optional[str] = None
    has_documents: bool = False

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Name cannot be empty.")
        if len(v) > _MAX_NAME_LEN:
            raise ValueError(f"Name must be at most {_MAX_NAME_LEN} characters.")
        return v

    @field_validator("region")
    @classmethod
    def validate_region(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Region cannot be empty.")
        if len(v) > _MAX_REGION_LEN:
            raise ValueError(f"Region must be at most {_MAX_REGION_LEN} characters.")
        return v

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: str) -> str:
        v = v.strip()
        if len(v) < _MIN_DESC_LEN:
            raise ValueError(
                f"Description must be at least {_MIN_DESC_LEN} characters "
                f"(currently {len(v)})."
            )
        if len(v) > _MAX_DESC_LEN:
            raise ValueError(
                f"Description must be at most {_MAX_DESC_LEN} characters."
            )
        return v

    @field_validator("needs")
    @classmethod
    def validate_needs(cls, v: List[str]) -> List[str]:
        if not v:
            raise ValueError("At least one need must be specified.")
        if len(v) > _MAX_NEEDS:
            raise ValueError(f"A maximum of {_MAX_NEEDS} needs can be specified.")
        return [n.strip() for n in v if n.strip()]

    @field_validator("donation_link")
    @classmethod
    def validate_donation_link(cls, v: Optional[str]) -> Optional[str]:
        if v and not v.startswith(("http://", "https://")):
            raise ValueError("Donation link must be a valid URL starting with http:// or https://.")
        return v

    @field_validator("contact_email")
    @classmethod
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        if v and "@" not in v:
            raise ValueError("Contact email must be a valid email address.")
        return v


@router.post("/submit")
async def submit_help_request(request: HelpRequest):
    """Submit a new help request. Returns an AI trust score."""
    try:
        trust = generate_trust_score(
            {
                "has_documents":  request.has_documents,
                "contact_email":  request.contact_email or "",
                "donation_link":  request.donation_link or "",
                "bank_details":   request.bank_details or "",
                "description":    request.description,
            }
        )

        # Track the submission by trust level for metrics
        help_requests_submitted_total.labels(trust_level=trust["level"]).inc()

        entry = {
            "id":            str(uuid.uuid4()),         # full UUID — no collision risk
            "name":          request.name,
            "region":        request.region,
            "description":   request.description,
            "needs":         request.needs,
            "contact_email": request.contact_email,
            "donation_link": request.donation_link,
            "bank_details":  request.bank_details,
            "has_documents": request.has_documents,
            "trust_score":   trust,
            "status":        "Active",
            "created_at":    datetime.now().isoformat(),
            "upvotes":       0,
        }
        _submitted_requests.insert(0, entry)
        logger.info(
            "Help request submitted",
            extra={"request_id": entry["id"], "region": request.region, "trust_level": trust["level"]},
        )
        return {"success": True, "id": entry["id"], "trust_score": trust}

    except Exception as exc:
        logger.error("Help request submission error: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/feed")
async def get_help_feed():
    """Return all help requests (user-submitted + sample data)."""
    all_requests = _submitted_requests + get_sample_help_requests()
    return {"requests": all_requests[:25], "count": len(all_requests)}


@router.post("/{request_id}/upvote")
async def upvote_request(request_id: str):
    """Increment upvote count on a user-submitted help request."""
    for req in _submitted_requests:
        if req["id"] == request_id:
            req["upvotes"] = req.get("upvotes", 0) + 1
            return {"success": True, "upvotes": req["upvotes"]}
    raise HTTPException(status_code=404, detail="Request not found.")
