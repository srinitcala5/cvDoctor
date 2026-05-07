import json
import re

from app.models.jd import JdGapAnalysisResponse, KeywordGap
from app.utils.claude_client import get_claude_client

# Stage 1: extract structured requirements from the JD
_EXTRACT_SYSTEM = """You are a technical recruiter extracting job requirements.
Given a job description, output ONLY valid JSON — no markdown, no preamble.
Schema:
{
  "must_haves": [{ "keyword": "<skill/tool/qualification>", "reason": "<why it is required>" }],
  "nice_to_haves": [{ "keyword": "<skill/tool/qualification>", "reason": "<why it is preferred>" }]
}
must_haves: skills/qualifications the JD marks as required, essential, or must-have.
nice_to_haves: skills/qualifications the JD marks as preferred, bonus, or nice-to-have.
Extract up to 20 must_haves and 10 nice_to_haves. Be specific — extract exact tool names and technologies, not vague categories."""

# Stage 2: semantically match JD requirements against resume text
_MATCH_SYSTEM = """You are a technical recruiter comparing a candidate's resume against a list of job requirements.
Apply semantic matching: treat synonyms and closely related technologies as matches
(e.g. "Azure OpenAI" matches "Azure Cognitive Services context", "Postgres" matches "PostgreSQL", "React" matches "ReactJS").
Do NOT match on vague category overlap — "cloud experience" does NOT match "AWS" unless AWS is explicitly present.

Output ONLY valid JSON:
{
  "match_percentage": <integer 0–100>,
  "missing_must_haves": [{ "keyword": "<keyword>", "reason": "<why it matters>" }],
  "missing_nice_to_haves": [{ "keyword": "<keyword>", "reason": "<why it matters>" }],
  "present_keywords": ["<keyword that was found>", ...]
}
match_percentage = (matched_must_haves / total_must_haves) * 100, rounded to nearest integer."""

_EXTRACT_USER = "Job description:\n\n{jd_text}"
_MATCH_USER = "Job requirements (JSON):\n{requirements}\n\nResume text:\n\n{resume_text}"


def _strip_fences(text: str) -> str:
    text = re.sub(r"^```(?:json)?\s*", "", text.strip())
    return re.sub(r"\s*```$", "", text)


def analyse_jd_gap(jd_text: str, resume_text: str) -> JdGapAnalysisResponse:
    client = get_claude_client()

    # Stage 1 — extract requirements from JD
    stage1 = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=_EXTRACT_SYSTEM,
        messages=[{"role": "user", "content": _EXTRACT_USER.format(jd_text=jd_text)}],
    )
    requirements_raw = _strip_fences(stage1.content[0].text)
    requirements = json.loads(requirements_raw)

    # Stage 2 — semantic match against resume
    stage2 = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=_MATCH_SYSTEM,
        messages=[
            {
                "role": "user",
                "content": _MATCH_USER.format(
                    requirements=requirements_raw,
                    resume_text=resume_text,
                ),
            }
        ],
    )
    match_raw = _strip_fences(stage2.content[0].text)
    match_data = json.loads(match_raw)

    return JdGapAnalysisResponse(
        match_percentage=match_data["match_percentage"],
        missing_must_haves=[
            KeywordGap(keyword=k["keyword"], reason=k.get("reason"))
            for k in match_data.get("missing_must_haves", [])
        ],
        missing_nice_to_haves=[
            KeywordGap(keyword=k["keyword"], reason=k.get("reason"))
            for k in match_data.get("missing_nice_to_haves", [])
        ],
        present_keywords=match_data.get("present_keywords", []),
    )
