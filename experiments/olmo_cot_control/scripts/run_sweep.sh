#!/usr/bin/env bash
# Runs generate_local over scripts/checkpoints.txt in order; resumable (skips existing outputs).
# Usage: bash scripts/run_sweep.sh [n_questions]
set -uo pipefail
cd "$(dirname "$0")/.."
N=${1:-150}
export HF_HUB_ENABLE_HF_TRANSFER=1
mkdir -p logs
while read -r repo rev; do
  [[ -z "$repo" || "$repo" == \#* ]] && continue
  out="rollouts/${repo//\//__}/${rev}.jsonl"
  if [[ -s "$out" ]]; then echo "[sweep] skip $repo@$rev"; continue; fi
  echo "[sweep] $(date -u +%FT%TZ) start $repo@$rev"
  python -m src.generate_local --repo "$repo" --revision "$rev" --n-questions "$N" --purge-cache \
      > "logs/gen_${repo//\//__}_${rev}.log" 2>&1
  rc=$?
  tail -n 3 "logs/gen_${repo//\//__}_${rev}.log"
  echo "[sweep] $(date -u +%FT%TZ) done $repo@$rev rc=$rc"
  echo "$(date -u +%FT%TZ) $repo $rev rc=$rc" >> logs/sweep_progress.txt
done < scripts/checkpoints.txt
echo "[sweep] ALL DONE $(date -u +%FT%TZ)"
