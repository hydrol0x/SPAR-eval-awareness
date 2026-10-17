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
echo "== judge: Answer-IF (results/judged)"
$PY -m src.judge_vea --rollouts 'rollouts/**/*.jsonl' --out-dir results/judged --tasks answer_if --budget-usd "${BUDGET:-40}" --concurrency 24 2>&1 | grep -E "^\[judge\] spend|Error|error" | tail -3
echo "== judge: VEA strict v2 (results/judged_v2)"
$PY -m src.judge_vea --rollouts 'rollouts/**/*.jsonl' --out-dir results/judged_v2 --tasks cot --vea-prompt-version v2 --budget-usd "${BUDGET:-40}" --concurrency 24 2>&1 | grep -E "^\[judge\] spend|Error|error" | tail -3
echo "== analyze"; $PY -m src.analyze 2>&1 | grep -v -E "UserWarning|ax.set_title" | tail -45
$PY -m src.report 2>&1 | tail -1
echo "== commit"
git add -A rollouts results figures results.md >/dev/null 2>&1 || true
if ! git diff --cached --quiet; then
  n=$(ls rollouts/*/*.jsonl 2>/dev/null | wc -l)
  git -c commit.gpgsign=false commit -q -m "Sync rollouts and judged results ($n checkpoints)

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01Tayx38fMPP2pjBkCUktg4h" && git push -q origin eval-awareness-cot-control-exp && echo "pushed ($n checkpoint files)"
else echo "nothing new"; fi
