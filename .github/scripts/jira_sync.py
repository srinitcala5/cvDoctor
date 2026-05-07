"""
PR Overseer — Jira sync script.
Transitions the ticket to Done and posts the PR URL as a comment.
Only called when the Claude review verdict is APPROVED.
"""

import os
import re
import sys

import requests

JIRA_BASE = "https://qbitworks.atlassian.net"
JIRA_EMAIL = "srinivas@qbitworks.atlassian.net"
DONE_STATUS_NAME = "Done"


def _auth() -> tuple[str, str]:
    token = os.environ.get("JIRA_TOKEN")
    if not token:
        print("JIRA_TOKEN not set", file=sys.stderr)
        sys.exit(1)
    return (JIRA_EMAIL, token)


def _ticket_from_branch(branch: str) -> str | None:
    match = re.search(r"(CVDOC-\d+)", branch, re.IGNORECASE)
    return match.group(1).upper() if match else None


def main() -> None:
    branch = os.environ.get("GITHUB_HEAD_REF", "")
    pr_url = os.environ.get("PR_URL", "")
    ticket_key = _ticket_from_branch(branch)

    if not ticket_key:
        print(f"Could not extract ticket key from branch: {branch}", file=sys.stderr)
        sys.exit(1)

    auth = _auth()
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    # Find the transition ID for Done
    trans_url = f"{JIRA_BASE}/rest/api/3/issue/{ticket_key}/transitions"
    resp = requests.get(trans_url, auth=auth, headers=headers, timeout=10)
    resp.raise_for_status()
    transitions = resp.json().get("transitions", [])
    done_id = next(
        (t["id"] for t in transitions if t["name"].lower() == DONE_STATUS_NAME.lower()),
        None,
    )
    if not done_id:
        print(f"No '{DONE_STATUS_NAME}' transition found for {ticket_key}", file=sys.stderr)
        sys.exit(1)

    # Transition to Done
    resp = requests.post(
        trans_url,
        auth=auth,
        headers=headers,
        json={"transition": {"id": done_id}},
        timeout=10,
    )
    resp.raise_for_status()
    print(f"Transitioned {ticket_key} to {DONE_STATUS_NAME}.")

    # Post PR URL as a comment
    if pr_url:
        comment_url = f"{JIRA_BASE}/rest/api/3/issue/{ticket_key}/comment"
        body = {
            "body": {
                "version": 1,
                "type": "doc",
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"type": "text", "text": f"PR merged: {pr_url}"}],
                    }
                ],
            }
        }
        resp = requests.post(comment_url, auth=auth, headers=headers, json=body, timeout=10)
        resp.raise_for_status()
        print(f"Posted PR URL to {ticket_key}.")


if __name__ == "__main__":
    main()
