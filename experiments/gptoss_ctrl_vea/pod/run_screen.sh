#!/usr/bin/env bash
# Base-model screen (SCREEN_PLAN.md). Resumable. One model at a time; each is deleted after its rollouts are written.
set -euo pipefail
W=/workspace
cd $W/SPAR-eval-awareness/experiments/gptoss_ctrl_vea
log() { echo "[$(date -u +%H:%M:%S)] $*"; }
export HF_HUB_ENABLE_HF_TRANSFER=1 VLLM_LOGGING_LEVEL=WARNING TOKENIZERS_PARALLELISM=false
# name | HF repo | top_k (model-card sampling: temperature 0.6, top_p 0.95)
MODELS="screen_qwen3_32b|Qwen/Qwen3-32B|20 screen_qwq_32b|Qwen/QwQ-32B|40 screen_olmo3_32b_think|allenai/Olmo-3-32B-Think|-1 screen_olmo31_32b_think|allenai/Olmo-3.1-32B-Think|-1"
for spec in $MODELS; do
  IFS='|' read -r name repo topk <<< "$spec"
  mkdir -p rollouts/$name
  if [[ -f rollouts/$name/DONE ]]; then continue; fi
  log "$name: download $repo"
  python -c "from huggingface_hub import snapshot_download; snapshot_download('$repo', local_dir='$W/models/$name', allow_patterns=['*.json','*.safetensors','*.txt','*.model','*.jinja','*.py','tokenizer*'])"
  log "$name: generate"
  python pod/gen_screen.py --model $W/models/$name --name $name --prompts data/screen_prompts.jsonl --out rollouts/$name/screen.jsonl --top-k $topk
  touch rollouts/$name/DONE; rm -rf $W/models/$name
done
log "ALL DONE"
touch results/SCREEN_DONE
