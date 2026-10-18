#!/usr/bin/env bash
# Main experiment on one 80GB GPU. Every stage is resumable: re-running skips finished work.
set -euo pipefail
W=/workspace
cd $W/SPAR-eval-awareness/experiments/gptoss_ctrl_vea
log() { echo "[$(date -u +%H:%M:%S)] $*"; }
export HF_HUB_ENABLE_HF_TRANSFER=1 VLLM_LOGGING_LEVEL=WARNING TOKENIZERS_PARALLELISM=false
mkdir -p rollouts/base rollouts/ctrldel rollouts/cdel results
PY=python

log "downloads"
$PY - <<'PYDL'
from huggingface_hub import snapshot_download, hf_hub_download
snapshot_download("unsloth/gpt-oss-20b-BF16", local_dir="/workspace/models/base")
snapshot_download("automated-alignment-science/cot-controllability-gpt-oss-20b-lora", local_dir="/workspace/adapters")
for f in ["datasets/sft_edited_reasoning_full.jsonl", "datasets/sft_raw_trace_control_full.jsonl"]:
    hf_hub_download("automated-alignment-science/cot-controllability-steering-vectors", f, repo_type="dataset", local_dir="/workspace/adapters")
PYDL
df -h $W | tail -1

gen() {  # name model_dir
  $PY pod/gen_vllm.py gen --model "$2" --name "$1" --prompts data/ctrl_check_prompts.jsonl --n-samples 1 --out rollouts/$1/ctrl_check.jsonl
  $PY pod/gen_vllm.py gen --model "$2" --name "$1" --prompts data/main_prompts.jsonl --n-samples 2 --out rollouts/$1/main.jsonl
}
nll() {  # model_dir sft_file tag
  if ! grep -q "\"$1\".*\"$2\"" results/merge_nll.jsonl 2>/dev/null; then
    $PY pod/gen_vllm.py nll --model "$1" --sft "$2" --n 64 --out results/merge_nll.jsonl
  fi
}
SFT_C=$W/adapters/datasets/sft_edited_reasoning_full.jsonl
SFT_R=$W/adapters/datasets/sft_raw_trace_control_full.jsonl

log "base: controllability check (also proves vLLM serves bf16 gpt-oss)"
$PY pod/gen_vllm.py gen --model $W/models/base --name base --prompts data/ctrl_check_prompts.jsonl --n-samples 1 --out rollouts/base/ctrl_check.jsonl

log "gate mapping check on the compliant adapter"
nll $W/models/base $SFT_C
if [[ ! -f $W/models/cdel/MERGE_INFO.json ]]; then
  for g in w1 w3; do
    [[ -f $W/models/cdel_$g/MERGE_INFO.json ]] || $PY pod/merge_lora.py --base $W/models/base --adapter-dir $W/adapters/cdel --out $W/models/cdel_$g --gate-is $g
    nll $W/models/cdel_$g $SFT_C
  done
  GATE=$($PY - <<'PYSEL'
import json
rows=[json.loads(l) for l in open("results/merge_nll.jsonl")]
best={}
for r in rows:
    for g in ("w1","w3"):
        if r["model"].endswith("cdel_"+g): best[g]=r["mean_nll"]
print(min(best, key=best.get))
PYSEL
)
  log "chosen gate mapping: $GATE (lower NLL on compliant SFT targets)"
  echo "$GATE" > results/gate_mapping.txt
  OTHER=$([[ $GATE == w1 ]] && echo w3 || echo w1)
  rm -rf $W/models/cdel_$OTHER
  mv $W/models/cdel_$GATE $W/models/cdel
fi
GATE=$(cat results/gate_mapping.txt)

log "base: main"
$PY pod/gen_vllm.py gen --model $W/models/base --name base --prompts data/main_prompts.jsonl --n-samples 2 --out rollouts/base/main.jsonl
log "cdel (compliant): check + main"
gen cdel $W/models/cdel

log "ctrldel (control): merge with gate=$GATE"
[[ -f $W/models/ctrldel/MERGE_INFO.json ]] || $PY pod/merge_lora.py --base $W/models/base --adapter-dir $W/adapters/ctrldel --out $W/models/ctrldel --gate-is $GATE
nll $W/models/base $SFT_R
nll $W/models/ctrldel $SFT_R
nll $W/models/cdel $SFT_R
nll $W/models/ctrldel $SFT_C
gen ctrldel $W/models/ctrldel

log "ALL DONE"
touch results/ALL_DONE
