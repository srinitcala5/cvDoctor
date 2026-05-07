from fastapi import APIRouter, Depends

from app.models.coverletter import CoverLetterRequest, CoverLetterResponse
from app.services.coverletter import generate_and_score_cover_letter
from app.utils.auth import get_current_user

router = APIRouter(prefix="/cover-letter", tags=["cover-letter"])


@router.post("/generate", response_model=CoverLetterResponse)
def generate_cover_letter(
    body: CoverLetterRequest,
    _user: dict = Depends(get_current_user),
):
    return generate_and_score_cover_letter(body.resume_text, body.jd_text)
