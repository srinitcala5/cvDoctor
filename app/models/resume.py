from pydantic import BaseModel


class ResumeUploadResponse(BaseModel):
    text: str
    page_count: int


class DimensionScore(BaseModel):
    score: int
    feedback: str


class ResumeScoreResponse(BaseModel):
    overall_score: int
    dimensions: dict[str, DimensionScore]
    top_issues: list[str]
    quick_wins: list[str]
