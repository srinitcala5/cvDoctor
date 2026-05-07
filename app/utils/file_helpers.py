import re
from tempfile import SpooledTemporaryFile

from fastapi import HTTPException, UploadFile, status


PDF_MIME_TYPES = {"application/pdf", "application/x-pdf"}
MAX_UPLOAD_BYTES = 5 * 1024 * 1024


def normalize_whitespace(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


async def read_limited_upload(file: UploadFile, max_bytes: int = MAX_UPLOAD_BYTES) -> bytes:
    contents = await file.read()
    if len(contents) > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File exceeds the 5MB limit.",
        )
    return contents


def assert_pdf_upload(file: UploadFile) -> None:
    if file.content_type not in PDF_MIME_TYPES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only PDF files are supported.")


def bytes_to_spooled_file(contents: bytes) -> SpooledTemporaryFile[bytes]:
    temp_file: SpooledTemporaryFile[bytes] = SpooledTemporaryFile(max_size=MAX_UPLOAD_BYTES)
    temp_file.write(contents)
    temp_file.seek(0)
    return temp_file
