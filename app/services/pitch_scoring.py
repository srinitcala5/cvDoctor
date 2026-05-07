import json
import re

from app.models.pitch import PitchFeedbackResponse, PitchScoreBar
from app.utils.claude_client import get_claude_client

# Pitch scoring focuses on narrative structure, not just content.
# The four dimensions map to what a recruiter or interviewer actually evaluates
# in the first 60 seconds of a candidate interaction.

_SYSTEM = """You are a career coach evaluating a candidate's elevator pitch transcript.
Score the pitch on four dimensions, each 0–25 (100 total).

STRUCTURE (0–25) — Does the pitch follow a clear arc?
  0  — No discernible structure; rambling or stream of consciousness.
 12  — Opening and body present but closing is weak or absent.
 25  — Clear three-part arc: hook → value proposition → specific ask/close.

CLARITY (0–25) — Is the message immediately understandable?
  0  — Jargon-heavy or vague; listener would not know what the candidate does.
 12  — Generally clear but one or two confusing segments.
 25  — A non-specialist could explain back who this person is and what they offer after one listen.

KEYWORD COVERAGE (0–25) — Are role-relevant terms present?
  0  — No professional keywords; could describe anyone in any industry.
 12  — Some domain vocabulary but missing critical role-level or industry-level terms.
 25  — Key professional keywords naturally woven in without sounding like a keyword list.

PACING (0–25) — Does the transcript suggest appropriate delivery speed?
  0  — Word count implies they rushed (<100 WPM for stated duration) or spoke extremely slowly (>200 WPM).
 12  — Pacing acceptable but word count suggests hesitation or speed issues.
 25  — Word count implies natural conversational pace (120–160 WPM) and the text reads as confidently delivered.

For highlighted_phrases: pick 3–5 specific phrases from the transcript that are either strong (mark with "+") or weak (mark with "−").
Format each as: "+ phrase here" or "− phrase here".

Output ONLY valid JSON:
{
  "scores": [
    { "label": "Structure", "score": <0–25> },
    { "label": "Clarity", "score": <0–25> },
    { "label": "Keyword Coverage", "score": <0–25> },
    { "label": "Pacing", "score": <0–25> }
  ],
  "highlighted_phrases": ["+ ...", "− ...", ...],
  "suggestions": ["<specific actionable improvement>", "<improvement 2>", "<improvement 3>"]
}"""

_USER_TEMPLATE = """Evaluate this elevator pitch.
Duration: {duration_seconds:.0f} seconds ({wpm} WPM)

Transcript:
{transcript}"""


def _strip_fences(text: str) -> str:
    text = re.sub(r"^```(?:json)?\s*", "", text.strip())
    return re.sub(r"\s*```$", "", text)


def score_pitch(
    transcript: str, duration_seconds: float, wpm: int
) -> PitchFeedbackResponse:
    client = get_claude_client()
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=_SYSTEM,
        messages=[
            {
                "role": "user",
                "content": _USER_TEMPLATE.format(
                    transcript=transcript,
                    duration_seconds=duration_seconds,
                    wpm=wpm,
                ),
            }
        ],
    )
    data = json.loads(_strip_fences(message.content[0].text))
    return PitchFeedbackResponse(
        transcript=transcript,
        highlighted_phrases=data.get("highlighted_phrases", []),
        scores=[PitchScoreBar(label=s["label"], score=s["score"]) for s in data["scores"]],
        suggestions=data.get("suggestions", []),
    )
