"""
PR Overseer — Claude code review script.
Reads pr_diff.txt and ticket.json, sends both to the Claude API,
writes verdict and review body to review_output.txt.
"""

import json
import os
import sys

import anthropic

SYSTEM_PROMPT = """You are a senior engineer reviewing a PR for the cvDoctor project.
You will receive a Jira ticket description and a git diff.
Review the diff against the acceptance criteria in the ticket.
Output a structured review with:
- VERDICT: APPROVED or CHANGES_REQUESTED
- SUMMARY: one paragraph
- ISSUES: numbered list of specific problems (empty if none)
- SUGGESTIONS: numbered list of optional improvements
Be direct. Flag real problems only. Do not nitpick style."""


def main() -> None:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ANTHROPIC_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    with open("pr_diff.txt", "r", encoding="utf-8") as f:
        diff = f.read()

    with open("ticket.json", "r", encoding="utf-8") as f:
        ticket_raw = json.load(f)

    # Extract readable description from Jira API v3 response
    fields = ticket_raw.get("fields", {})
    summary = fields.get("summary", "(no summary)")
    description_doc = fields.get("description", {})
    description_text = _extract_jira_description(description_doc)

    user_message = f"""Jira ticket: {summary}

Description:
{description_text}

Git diff:
```diff
{diff}
```"""

    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    review_text = response.content[0].text.strip()

    with open("review_output.txt", "w", encoding="utf-8") as f:
        f.write(review_text)

    # Emit verdict as a GitHub Actions output for the workflow condition
    verdict = "APPROVED" if "VERDICT: APPROVED" in review_text else "CHANGES_REQUESTED"
    output_file = os.environ.get("GITHUB_OUTPUT", "")
    if output_file:
        with open(output_file, "a", encoding="utf-8") as f:
            f.write(f"verdict={verdict}\n")

    print(f"Review complete. Verdict: {verdict}")


def _extract_jira_description(doc: dict | None) -> str:
    """Flatten Atlassian Document Format (ADF) to plain text."""
    if not doc or not isinstance(doc, dict):
        return "(no description)"
    lines: list[str] = []
    for block in doc.get("content", []):
        for inline in block.get("content", []):
            if inline.get("type") == "text":
                lines.append(inline.get("text", ""))
        lines.append("\n")
    return "".join(lines).strip() or "(no description)"


if __name__ == "__main__":
    main()
