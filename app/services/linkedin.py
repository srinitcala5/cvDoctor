import json
import re

from app.models.linkedin import LinkedInOptimizeResponse, LinkedInSectionResult
from app.utils.claude_client import get_claude_client

# LinkedIn platform mechanics that differ from resume optimisation:
# - Headline: 220 chars indexed heavily; keyword placement in first 60 chars matters most.
# - About: only first ~300 chars visible before "see more" — hook must land there.
# - Experience bullets: indexed differently; lead verb + quantification still applies
#   but keyword density carries more weight than on a resume because LinkedIn search ranks on it.

_SYSTEM = """You are a LinkedIn optimisation specialist who understands how recruiter search and the LinkedIn algorithm work.

Platform-specific rules you must apply:

HEADLINE
- Recruiters search by keyword; the headline is the highest-weighted field.
- Optimal format: [Primary Role] | [Specialisation] | [Differentiator or metric].
- Max 220 characters. Pack keywords into the first 60 — that is what appears in search snippets.
- Never use "Looking for new opportunities" or "Open to work" as the headline itself.

ABOUT
- Only the first ~300 characters display before "see more" — the hook must land in that window.
- Write in first person. Start with the single strongest professional claim, not a generic intro.
- Weave in 3–5 high-value keywords naturally. End with a clear statement of what the person is looking for or offering.

EXPERIENCE BULLETS
- LinkedIn's search index weights keywords in experience more heavily than on a resume.
- Each bullet: action verb + metric + technology/tool keyword.
- Aim for 3–5 bullets per role. Keyword density is as important as narrative clarity.

Output ONLY valid JSON:
{
  "headline": {
    "score": <0–100>,
    "original": "<the original headline text>",
    "suggested": "<optimised headline>"
  },
  "about": {
    "score": <0–100>,
    "original": "<the original about text>",
    "suggested": "<optimised about text>"
  },
  "experience": {
    "score": <0–100>,
    "original": "<the original experience bullets>",
    "suggested": "<optimised experience bullets>"
  }
}
Score each section 0–100 based on keyword density, platform-specific best practices, and voice preservation.
Rewrites must preserve the user's professional identity — do not invent achievements or credentials."""

_USER_TEMPLATE = """Optimise this LinkedIn profile.

HEADLINE:
{headline}

ABOUT:
{about}

EXPERIENCE BULLETS:
{experience}"""


def _strip_fences(text: str) -> str:
    text = re.sub(r"^```(?:json)?\s*", "", text.strip())
    return re.sub(r"\s*```$", "", text)


def optimise_linkedin(
    headline: str, about: str, experience: str
) -> LinkedInOptimizeResponse:
    client = get_claude_client()
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        system=_SYSTEM,
        messages=[
            {
                "role": "user",
                "content": _USER_TEMPLATE.format(
                    headline=headline, about=about, experience=experience
                ),
            }
        ],
    )
    data = json.loads(_strip_fences(message.content[0].text))

    def _section(key: str) -> LinkedInSectionResult:
        s = data[key]
        return LinkedInSectionResult(
            score=s["score"], original=s["original"], suggested=s["suggested"]
        )

    return LinkedInOptimizeResponse(
        headline=_section("headline"),
        about=_section("about"),
        experience=_section("experience"),
    )
