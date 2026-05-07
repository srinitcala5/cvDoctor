from pydantic import BaseModel


class KeywordGap(BaseModel):
    keyword: str
    reason: str | None = None


class JdGapAnalysisResponse(BaseModel):
    match_percentage: int
    missing_must_haves: list[KeywordGap]
    missing_nice_to_haves: list[KeywordGap]
    present_keywords: list[str]


class JdGapAnalysisRequest(BaseModel):
    jd_text: str
    resume_text: str
