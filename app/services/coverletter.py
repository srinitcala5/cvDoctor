import json
import re

from app.models.coverletter import CoverLetterResponse, CoverLetterScore
from app.utils.claude_client import get_claude_client

_GENERATE_SYSTEM = """You are a professional cover letter writer who produces letters that read as genuinely human.

Rules you must follow:
1. Match the candidate's writing register from their resume — formal if the resume is formal, conversational if it is.
2. Open with a specific hook tied to the company or role — never "I am writing to apply for...".
3. One evidence paragraph: pick the single strongest bullet from the resume and expand it with context, stakes, and outcome.
4. Close with a direct, confident ask — not "I hope to hear from you".
5. Keep it to three paragraphs, 250–350 words total. Never exceed 400 words.
6. Do not use hollow phrases: "passionate", "team player", "results-driven", "detail-oriented".
7. Output ONLY the cover letter text — no subject line, no date, no address block."""

_GENERATE_USER = """Write a cover letter for this candidate applying to this role.

RESUME:
{resume_text}

JOB DESCRIPTION:
{jd_text}"""

_SCORE_SYSTEM = """You are a senior recruiter evaluating a cover letter. Score it on four dimensions, each 0–25 (100 total).

TARGETED KEYWORDS (0–25)
  0  — No keywords from the JD appear in the letter.
 12  — Some keywords present but critical role-specific terms are absent.
 25  — Key technical and domain terms from the JD are woven naturally into the letter.

OPENING STRENGTH (0–25)
  0  — Generic opening ("I am writing to apply...").
 12  — Personalised but low-energy or vague.
 25  — Immediately specific to the company/role, creates genuine interest.

EVIDENCE QUALITY (0–25)
  0  — No concrete examples; pure assertion.
 12  — One example present but lacking quantified outcome or stakes.
 25  — At least one clear, specific achievement with a measurable result.

CALL TO ACTION (0–25)
  0  — Passive or no close ("I hope to hear from you").
 12  — Some initiative shown but tentative.
 25  — Confident, specific ask that moves the conversation forward.

Output ONLY valid JSON:
{
  "targeted_keywords": <0–25>,
  "opening_strength": <0–25>,
  "evidence_quality": <0–25>,
  "call_to_action": <0–25>,
  "feedback": ["<specific actionable feedback item>", "<item 2>", "<item 3>"]
}"""

_SCORE_USER = """Rate this cover letter against the job description.

JOB DESCRIPTION:
{jd_text}

COVER LETTER:
{letter_text}"""


def _strip_fences(text: str) -> str:
    text = re.sub(r"^```(?:json)?\s*", "", text.strip())
    return re.sub(r"\s*```$", "", text)


def generate_and_score_cover_letter(
    resume_text: str, jd_text: str
) -> CoverLetterResponse:
    client = get_claude_client()

    gen = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=_GENERATE_SYSTEM,
        messages=[
            {
                "role": "user",
                "content": _GENERATE_USER.format(
                    resume_text=resume_text, jd_text=jd_text
                ),
            }
        ],
    )
    letter_text = gen.content[0].text.strip()

    score_msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        system=_SCORE_SYSTEM,
        messages=[
            {
                "role": "user",
                "content": _SCORE_USER.format(
                    jd_text=jd_text, letter_text=letter_text
                ),
            }
        ],
    )
    score_data = json.loads(_strip_fences(score_msg.content[0].text))

    return CoverLetterResponse(
        text=letter_text,
        score=CoverLetterScore(
            targeted_keywords=score_data["targeted_keywords"],
            opening_strength=score_data["opening_strength"],
            evidence_quality=score_data["evidence_quality"],
            call_to_action=score_data["call_to_action"],
        ),
        feedback=score_data.get("feedback", []),
    )
