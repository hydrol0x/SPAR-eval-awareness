#!/usr/bin/env bash
# One check-in: pull new rollouts off the pod, judge them, aggregate, commit, push.
# Env: POD_ID, JUPYTER_TOKEN, PY (python with httpx/pandas/matplotlib)
set -uo pipefail
cd "$(dirname "$0")/.."
PY=${PY:-python3}
REMOTE=workspace/SPAR-eval-awareness/experiments/olmo_cot_control
echo "== $(date -u +%FT%TZ) sync"
$PY scripts/pod_fetch.py sync $REMOTE/rollouts rollouts || echo "sync failed"
$PY scripts/pod_fetch.py sync $REMOTE/logs logs_pod || true
$PY scripts/pod_fetch.py cat $REMOTE/logs/sweep_progress.txt > results/sweep_progress.txt 2>/dev/null || true
echo "== judge"; $PY -m src.judge_vea --rollouts 'rollouts/**/*.jsonl' --out-dir results/judged --budget-usd "${BUDGET:-40}" --concurrency 24 2>&1 | grep -E "^\[judge\]|Error|error" | tail -20
echo "== analyze"; $PY -m src.analyze 2>&1 | tail -40
echo "== commit"
git add -A rollouts results figures >/dev/null 2>&1 || true
if ! git diff --cached --quiet; then
  n=$(ls rollouts/*/*.jsonl 2>/dev/null | wc -l)
  git -c commit.gpgsign=false commit -q -m "Sync rollouts and judged results ($n checkpoints)

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01Tayx38fMPP2pjBkCUktg4h" && git push -q origin eval-awareness-cot-control-exp && echo "pushed ($n checkpoint files)"
else echo "nothing new"; fi
