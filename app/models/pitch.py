from pydantic import BaseModel


class PitchTranscriptionResponse(BaseModel):
    transcript: str
    duration_seconds: float
    word_count: int
    wpm: int


class PitchScoreBar(BaseModel):
    label: str
    score: int


class PitchFeedbackResponse(BaseModel):
    transcript: str
    highlighted_phrases: list[str]
    scores: list[PitchScoreBar]
    suggestions: list[str]
