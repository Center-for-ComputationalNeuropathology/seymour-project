#!/bin/bash
# publish_papers.sh — rebuild data/papers.json from the daily scan reports and
# push it to GitHub (which redeploys the Pages site). Safe to run repeatedly:
# it only commits/pushes when papers.json actually changed.
set -uo pipefail

REPO="${SEYMOUR_REPO:-$HOME/seymour-project}"
cd "$REPO" || { echo "publish_papers: repo not found at $REPO"; exit 1; }

python3 "$REPO/scripts/build_papers_json.py" || { echo "publish_papers: build failed"; exit 1; }

if git diff --quiet -- data/papers.json 2>/dev/null; then
  echo "publish_papers: no change in data/papers.json — nothing to publish."
  exit 0
fi

git add data/papers.json
git commit -m "Update daily paper summaries ($(date -u +%Y-%m-%d))" || {
  echo "publish_papers: nothing to commit."; exit 0; }
git push origin main && echo "publish_papers: published."
