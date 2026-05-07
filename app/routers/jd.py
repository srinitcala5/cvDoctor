from fastapi import APIRouter

from app.models.jd import JdGapAnalysisResponse

router = APIRouter(prefix="/jd", tags=["job-description"])


@router.get("/health")
async def health_check():
    return {"status": "jd-ready"}
