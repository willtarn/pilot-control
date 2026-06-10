#!/usr/bin/env bash
#
# publish.sh — initialise this folder as a git repo and push to GitHub.
#
# Prerequisites:
#   - git installed
#   - gh CLI installed and authenticated (gh auth login)
#   - You are inside this folder (pilot_control_dataset/)
#
# Usage:
#   ./publish.sh <your-github-username> [repo-name]
#
# Example:
#   ./publish.sh willis-tarn pilot-control

set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <your-github-username> [repo-name]"
  echo "Example: $0 willis-tarn pilot-control"
  exit 1
fi

USERNAME="$1"
REPO_NAME="${2:-pilot-control}"

echo "==> Sanity check"
[[ -f README.md ]] || { echo "README.md missing — are you in the right folder?"; exit 1; }
[[ -f LICENSE ]]   || { echo "LICENSE missing"; exit 1; }
[[ -f pyproject.toml ]] || { echo "pyproject.toml missing"; exit 1; }

echo "==> Find-and-replace the <your-username> placeholders"
# sed -i on macOS needs an empty backup arg; on Linux it doesn't. Detect.
if [[ "$(uname)" == "Darwin" ]]; then
  SED_INPLACE=(sed -i '')
else
  SED_INPLACE=(sed -i)
fi
"${SED_INPLACE[@]}" "s|<your-username>|${USERNAME}|g" pyproject.toml CITATION.cff

echo "==> git init (if not already a repo)"
if [[ ! -d .git ]]; then
  git init -b main
fi

echo "==> Stage and commit"
git add .
if git diff --cached --quiet; then
  echo "    nothing new to commit"
else
  git commit -m "initial scaffold: Pilot Control benchmark dataset, Inspect harness, scoring, and docs"
fi

echo "==> Create GitHub repo (public) and push"
if gh repo view "${USERNAME}/${REPO_NAME}" >/dev/null 2>&1; then
  echo "    repo ${USERNAME}/${REPO_NAME} already exists; adding remote and pushing"
  git remote add origin "https://github.com/${USERNAME}/${REPO_NAME}.git" 2>/dev/null || true
  git push -u origin main
else
  gh repo create "${USERNAME}/${REPO_NAME}" \
    --public \
    --source=. \
    --remote=origin \
    --push \
    --description "A maritime safety benchmark for LLM agents — TARA APAC capstone project."
fi

echo
echo "==> Done."
echo "    Repo:  https://github.com/${USERNAME}/${REPO_NAME}"
echo "    CI:    https://github.com/${USERNAME}/${REPO_NAME}/actions"
echo
echo "Next:"
echo "  1) Watch the first CI run go green (~90 sec)."
echo "  2) Set the repo topics on the GitHub page: ai-safety, llm-evaluation, maritime, inspect, colregs, mass"
echo "  3) Add a one-line description and the homepage URL via the GitHub web UI."
echo "  4) Smoke-test the eval:  inspect eval inspect_eval/pilot_control_task.py@pilot_control --model openai/gpt-4o-mini --limit 2"
