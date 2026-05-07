from pydantic import BaseModel


class LinkedInSectionResult(BaseModel):
    score: int
    original: str
    suggested: str


class LinkedInOptimizeResponse(BaseModel):
    headline: LinkedInSectionResult
    about: LinkedInSectionResult
    experience: LinkedInSectionResult
