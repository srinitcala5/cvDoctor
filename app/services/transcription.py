import os
from tempfile import NamedTemporaryFile

from fastapi import HTTPException, UploadFile, status
from openai import OpenAI


async def transcribe_audio(file: UploadFile, duration_seconds: float) -> dict[str, int | float | str]:
    if duration_seconds <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Duration must be greater than zero.")

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="OPENAI_API_KEY is not configured.")

    suffix = f".{(file.filename or 'audio.webm').split('.')[-1]}"
    contents = await file.read()
    with NamedTemporaryFile(suffix=suffix) as audio_file:
        audio_file.write(contents)
        audio_file.flush()
        with open(audio_file.name, "rb") as stream:
            transcript = OpenAI(api_key=api_key).audio.transcriptions.create(model="whisper-1", file=stream)

    text = transcript.text.strip()
    word_count = len([word for word in text.split() if word])
    wpm = round(word_count / (duration_seconds / 60))
    return {
        "transcript": text,
        "duration_seconds": duration_seconds,
        "word_count": word_count,
        "wpm": wpm,
    }
