#!/usr/bin/env bash
# Confirmatory rerun (PREREG_confirm.md). Resumable.
set -euo pipefail
W=/workspace
cd $W/SPAR-eval-awareness/experiments/gptoss_ctrl_vea
log() { echo "[$(date -u +%H:%M:%S)] $*"; }
export HF_HUB_ENABLE_HF_TRANSFER=1 VLLM_LOGGING_LEVEL=WARNING TOKENIZERS_PARALLELISM=false
mkdir -p rollouts/base rollouts/ctrldel rollouts/cdel results
PY=python
GATE=$(cat results/gate_mapping.txt)

log "downloads"
$PY - <<'PYDL'
from huggingface_hub import snapshot_download
snapshot_download("unsloth/gpt-oss-20b-BF16", local_dir="/workspace/models/base")
snapshot_download("automated-alignment-science/cot-controllability-gpt-oss-20b-lora", local_dir="/workspace/adapters")
PYDL

for a in cdel ctrldel; do
  log "merge $a (gate=$GATE)"
  [[ -f $W/models/$a/MERGE_INFO.json ]] || $PY pod/merge_lora.py --base $W/models/base --adapter-dir $W/adapters/$a --out $W/models/$a --gate-is $GATE
done

log "sanity check (gates the run)"
for a in cdel ctrldel; do
  $PY pod/gen_vllm.py gen --model $W/models/$a --name $a --prompts data/ctrl_sanity_prompts.jsonl --n-samples 1 --sample-offset 100 --out rollouts/$a/ctrl_sanity.jsonl
done
$PY - <<'PYCHK'
import json, sys
sys.path.insert(0, ".")
from src.grade_ctrl import grade
res = {}
for m in ["cdel", "ctrldel"]:
    rows = [json.loads(l) for l in open(f"rollouts/{m}/ctrl_sanity.jsonl") if json.loads(l)["condition"] == "all_caps"]
    res[m] = sum(1 for r in rows if grade("all_caps", r["reasoning"])[0]) / len(rows)
print("SANITY all_caps compliance", res, flush=True)
if not (res["cdel"] >= 0.90 and res["ctrldel"] <= 0.05):
    print("SANITY FAILED: aborting", flush=True); sys.exit(1)
PYCHK

for m in base cdel ctrldel; do
  dir=$W/models/$m
  log "$m: replication (6 new samples, indices 2-7)"
  $PY pod/gen_vllm.py gen --model $dir --name $m --prompts data/confirm_replication.jsonl --n-samples 6 --sample-offset 2 --out rollouts/$m/confirm.jsonl
  log "$m: generalization (4 samples)"
  $PY pod/gen_vllm.py gen --model $dir --name $m --prompts data/confirm_generalization.jsonl --n-samples 4 --out rollouts/$m/confirm.jsonl
done
log "ALL DONE"
touch results/CONFIRM_DONE
