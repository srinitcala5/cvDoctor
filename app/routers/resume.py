from fastapi import APIRouter, Depends, File, UploadFile

from app.models.resume import ResumeScoreResponse, ResumeUploadResponse
from app.services.extraction import extract_pdf_text
from app.services.scoring import score_resume
from app.utils.auth import get_current_user
from app.utils.file_helpers import assert_pdf_upload, read_limited_upload

router = APIRouter(prefix="/resume", tags=["resume"])


@router.post("/upload", response_model=ResumeUploadResponse)
async def upload_resume(file: UploadFile = File(...)):
    assert_pdf_upload(file)
    contents = await read_limited_upload(file)
    text, page_count = extract_pdf_text(contents)
    return ResumeUploadResponse(text=text, page_count=page_count)


@router.post("/score", response_model=ResumeScoreResponse)
async def score_resume_endpoint(
    file: UploadFile = File(...),
    _user: dict = Depends(get_current_user),
):
    assert_pdf_upload(file)
    contents = await read_limited_upload(file)
    text, _ = extract_pdf_text(contents)
    return score_resume(text)
