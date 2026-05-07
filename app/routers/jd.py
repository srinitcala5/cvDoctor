from fastapi import APIRouter, Depends

from app.models.jd import JdGapAnalysisRequest, JdGapAnalysisResponse
from app.services.jd_analysis import analyse_jd_gap
from app.utils.auth import get_current_user

router = APIRouter(prefix="/jd", tags=["job-description"])


@router.post("/gap-analysis", response_model=JdGapAnalysisResponse)
def gap_analysis(
    body: JdGapAnalysisRequest,
    _user: dict = Depends(get_current_user),
):
    return analyse_jd_gap(body.jd_text, body.resume_text)
