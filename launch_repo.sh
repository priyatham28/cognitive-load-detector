#!/usr/bin/env bash
set -euo pipefail

if ! command -v gh >/dev/null 2>&1; then
  echo "GitHub CLI (gh) is required. Install from https://cli.github.com/ and run 'gh auth login'." >&2
  exit 1
fi
if ! command -v git >/dev/null 2>&1; then
  echo "git is required." >&2
  exit 1
fi

REPO_NAME="${1:-}"
VISIBILITY="${2:-private}" # or public
DESC="${3:-Auto-initialized by bootstrap script}"

if [[ -z "$REPO_NAME" ]]; then
  echo "Usage: $0 <repo_name> [private|public] [description]" >&2
  exit 1
fi

# Initialize repo if not yet
if [ ! -d .git ]; then
  git init
  git add .
  git commit -m "chore: initial commit"
fi

# Create GitHub repo and push
gh repo create "$REPO_NAME" --"$VISIBILITY" --source=. --remote=origin --push

# Protect default branch
DEFAULT_BRANCH="$(git symbolic-ref --short HEAD)"
gh api -X PUT "repos/{owner}/$REPO_NAME/branches/$DEFAULT_BRANCH/protection"   -F required_status_checks[strict]=true   -F enforce_admins=true   -F required_pull_request_reviews[dismiss_stale_reviews]=true   -F restrictions=

# Create first release
git tag v0.1.0 || true
git push origin --tags
gh release create v0.1.0 -t "v0.1.0" -n "Initial skeleton"

# Enable Actions and Pages (if desired)
# gh api -X POST repos/{owner}/$REPO_NAME/pages --input <(echo '{"build_type":"workflow"}') || true

echo "Done. Repo URL:"
gh repo view "$REPO_NAME" --web