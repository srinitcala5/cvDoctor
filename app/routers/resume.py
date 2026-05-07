from fastapi import APIRouter, File, UploadFile

from app.models.resume import ResumeUploadResponse
from app.services.extraction import extract_pdf_text
from app.utils.file_helpers import assert_pdf_upload, read_limited_upload

router = APIRouter(prefix="/resume", tags=["resume"])


@router.post("/upload", response_model=ResumeUploadResponse)
async def upload_resume(file: UploadFile = File(...)):
    assert_pdf_upload(file)
    contents = await read_limited_upload(file)
    text, page_count = extract_pdf_text(contents)
    return ResumeUploadResponse(text=text, page_count=page_count)
