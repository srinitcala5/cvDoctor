import json
import re

from app.models.resume import DimensionScore, ResumeScoreResponse
from app.utils.claude_client import get_claude_client

_SYSTEM_PROMPT = """You are a senior career coach and resume reviewer.
You score resumes across five dimensions, each worth 0–20 points (100 total).

Rubric anchors per dimension:

FORMATTING AND LAYOUT (0–20)
  0  — No discernible structure; walls of text; impossible to scan.
 10  — Readable with some inconsistencies: uneven spacing, mixed bullet styles, section order non-standard.
 20  — Crisp layout, consistent spacing, logical section order (Summary → Experience → Education → Skills), optimal length (1–2 pages).

BULLET IMPACT AND QUANTIFICATION (0–20)
  0  — Every bullet is a duty statement ("Responsible for..."). Zero numbers.
 10  — Mix of duties and achievements; some numbers present but inconsistent.
 20  — ≥80% of bullets lead with an action verb and include a quantified outcome (%, $, time saved, scale).

KEYWORD RELEVANCE (0–20)
  0  — No industry, technical, or role-relevant keywords.
 10  — Some keywords present but missing critical role-specific terms; no keyword strategy visible.
 20  — Strong keyword density covering technical skills, tools, domain vocabulary, and role-specific terminology.

SECTION COMPLETENESS (0–20)
  0  — Missing more than two required sections (Summary, Experience, Education, Skills).
 10  — All required sections present but one or more is thin or underdeveloped.
 20  — All four required sections present and fully developed; optional sections (Certifications, Projects) add value.

CAREER PROGRESSION CLARITY (0–20)
  0  — Job history appears random; titles or industries jump without logic.
 10  — Some upward or lateral movement visible but the narrative is unclear.
 20  — Clear progression: titles advance, scope grows, each role builds logically on the last.

Output ONLY valid JSON — no markdown, no preamble, no explanation.
The JSON must exactly match this schema:
{
  "overall_score": <integer 0–100>,
  "dimensions": {
    "formatting": { "score": <0–20>, "feedback": "<one concise sentence>" },
    "bullet_impact": { "score": <0–20>, "feedback": "<one concise sentence>" },
    "keyword_relevance": { "score": <0–20>, "feedback": "<one concise sentence>" },
    "section_completeness": { "score": <0–20>, "feedback": "<one concise sentence>" },
    "career_progression": { "score": <0–20>, "feedback": "<one concise sentence>" }
  },
  "top_issues": ["<issue 1>", "<issue 2>", "<issue 3>"],
  "quick_wins": ["<win 1>", "<win 2>", "<win 3>"]
}
overall_score must equal the sum of all five dimension scores.
top_issues: the three most damaging problems in priority order.
quick_wins: the three highest-ROI improvements the candidate can make today."""

_USER_TEMPLATE = "Score this resume:\n\n{resume_text}"


def score_resume(resume_text: str) -> ResumeScoreResponse:
    client = get_claude_client()
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": _USER_TEMPLATE.format(resume_text=resume_text)}],
    )
    raw = message.content[0].text.strip()
    # Strip accidental markdown fences if the model adds them despite instructions
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    data = json.loads(raw)

    dimensions = {
        key: DimensionScore(score=val["score"], feedback=val["feedback"])
        for key, val in data["dimensions"].items()
    }
    return ResumeScoreResponse(
        overall_score=data["overall_score"],
        dimensions=dimensions,
        top_issues=data["top_issues"],
        quick_wins=data["quick_wins"],
    )
