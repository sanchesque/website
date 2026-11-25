#!/usr/bin/env bash
# Publish sanchesque.com end to end:
#   check_site.py (repo, includes C-15 brand sync) -> build_site.sh ->
#   check_site.py _site -> git push origin master -> wait for the
#   "Push on master" Workers Builds run of the pushed commit ->
#   check_site.py --live
# The output of every run is archived to logs/publish-<UTC timestamp>.log
# (logs/ is gitignored and not published: build_site.sh copies an allowlist).
# The push requires Alex's approval in the session chat before running this.
#   scripts/publish.sh             full pipeline
#   scripts/publish.sh --no-push   checks and build only, nothing published
set -euo pipefail
cd "$(dirname "$0")/.."

mkdir -p logs
LOG="logs/publish-$(date -u +%Y%m%d-%H%M%S).log"

{
  echo "== publish $(date -u +%Y-%m-%dT%H:%M:%SZ) · commit $(git rev-parse --short HEAD)"
  echo "== check_site.py (repo)"
  python3 scripts/check_site.py
  echo "== build_site.sh"
  sh scripts/build_site.sh
  echo "== check_site.py _site"
  python3 scripts/check_site.py _site
  if [ "${1:-}" = "--no-push" ]; then
    echo "== no push (--no-push), nothing published"
    exit 0
  fi
  echo "== git push origin master"
  git push origin master
  SHA=$(git rev-parse HEAD)
  echo "== waiting for the Workers Builds run of $SHA (poll every 15 s, up to 10 min)"
  DEPLOYED=""
  for i in $(seq 1 40); do
    sleep 15
    LINE=$(gh api repos/sanchesque/website/actions/runs --jq \
      "[.workflow_runs[] | select(.head_sha == \"$SHA\")][0] | if . then \"\(.status) \(.conclusion // \"null\")\" else \"\" end" \
      2>/dev/null || true)
    echo "  poll $i: ${LINE:-no run yet}"
    if [[ "$LINE" == completed\ * ]]; then
      DEPLOYED="$LINE"
      break
    fi
  done
  if [ -z "$DEPLOYED" ]; then
    echo "ERROR: the Workers Builds run of $SHA did not complete in 10 min"
    exit 1
  fi
  if [[ "$DEPLOYED" != *" success" ]]; then
    echo "ERROR: Workers Builds run of $SHA finished with: $DEPLOYED"
    exit 1
  fi
  echo "== deployed: $DEPLOYED"
  echo "== check_site.py --live"
  python3 scripts/check_site.py --live
  echo "== PUBLISHED OK"
} 2>&1 | tee "$LOG"
