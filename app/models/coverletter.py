from pydantic import BaseModel


class CoverLetterScore(BaseModel):
    targeted_keywords: int
    opening_strength: int
    evidence_quality: int
    call_to_action: int


class CoverLetterResponse(BaseModel):
    text: str
    score: CoverLetterScore
    feedback: list[str]
