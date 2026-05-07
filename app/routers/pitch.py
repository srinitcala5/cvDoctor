from fastapi import APIRouter, File, Form, UploadFile

from app.models.pitch import PitchTranscriptionResponse
from app.services.transcription import transcribe_audio

router = APIRouter(prefix="/pitch", tags=["pitch"])


@router.post("/transcribe", response_model=PitchTranscriptionResponse)
async def transcribe_pitch(file: UploadFile = File(...), duration_seconds: float = Form(...)):
    return await transcribe_audio(file, duration_seconds)
