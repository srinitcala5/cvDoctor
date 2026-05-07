from app.models.resume import DimensionScore, ResumeScoreResponse


def placeholder_resume_score() -> ResumeScoreResponse:
    return ResumeScoreResponse(
        overall_score=0,
        dimensions={
            "formatting": DimensionScore(score=0, feedback="Scoring prompt implementation is assigned to Claude."),
            "bullet_impact": DimensionScore(score=0, feedback="Scoring prompt implementation is assigned to Claude."),
            "keyword_relevance": DimensionScore(score=0, feedback="Scoring prompt implementation is assigned to Claude."),
            "section_completeness": DimensionScore(score=0, feedback="Scoring prompt implementation is assigned to Claude."),
            "career_progression": DimensionScore(score=0, feedback="Scoring prompt implementation is assigned to Claude."),
        },
        top_issues=[],
        quick_wins=[],
    )
