"""Generate release notes from recent commits.

Designed for local/CI use; prints a markdown section enumerating commits since
last tag. In CI environments without git history or tags, gracefully falls back
to HEAD.^
"""

from __future__ import annotations

import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def _git(args: list[str]) -> str:
    return subprocess.check_output(["git", *args], cwd=REPO_ROOT).decode().strip()


def fetch_commits() -> list[str]:
    try:
        last_tag = _git(["describe", "--tags", "--abbrev=0"])
    except subprocess.CalledProcessError:
        last_tag = "HEAD^"
    log_output = _git(["log", f"{last_tag}..HEAD", "--pretty=format:* %s (%an)"])
    return [line for line in log_output.splitlines() if line]


def main() -> None:
    commits = fetch_commits()
    if not commits:
        print("No new commits since last release.")
        return
    print("### Changes")
    for line in commits:
        print(line)


if __name__ == "__main__":
    main()
