from fastapi import APIRouter, Depends, File, Form, UploadFile

from app.models.pitch import PitchFeedbackResponse, PitchScoreRequest, PitchTranscriptionResponse
from app.services.pitch_scoring import score_pitch
from app.services.transcription import transcribe_audio
from app.utils.auth import get_current_user

router = APIRouter(prefix="/pitch", tags=["pitch"])


@router.post("/transcribe", response_model=PitchTranscriptionResponse)
async def transcribe_pitch(
    file: UploadFile = File(...),
    duration_seconds: float = Form(...),
):
    return await transcribe_audio(file, duration_seconds)


@router.post("/score", response_model=PitchFeedbackResponse)
def score_pitch_endpoint(
    body: PitchScoreRequest,
    _user: dict = Depends(get_current_user),
):
    return score_pitch(body.transcript, body.duration_seconds, body.wpm)
