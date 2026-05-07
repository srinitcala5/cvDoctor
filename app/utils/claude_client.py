import os

from anthropic import Anthropic


def get_claude_client() -> Anthropic:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not configured.")
    return Anthropic(api_key=api_key)
