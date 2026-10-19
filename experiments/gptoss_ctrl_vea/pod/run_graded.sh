#!/usr/bin/env bash
# Graded-compliance run on Olmo-3.1-32B-Think (GRADED_PLAN.md). PHASE=A: calibration; PHASE=B: main run. Resumable.
set -euo pipefail
W=/workspace
cd $W/SPAR-eval-awareness/experiments/gptoss_ctrl_vea
log() { echo "[$(date -u +%H:%M:%S)] $*"; }
export HF_HUB_ENABLE_HF_TRANSFER=1 VLLM_LOGGING_LEVEL=WARNING TOKENIZERS_PARALLELISM=false
NAME=olmo31_32b_think; TP=$(nvidia-smi -L | wc -l)
mkdir -p rollouts/$NAME
log "download (tp=$TP)"
python -c "from huggingface_hub import snapshot_download; snapshot_download('allenai/Olmo-3.1-32B-Think', local_dir='$W/models/$NAME', allow_patterns=['*.json','*.safetensors','*.txt','*.model','*.jinja','*.py','tokenizer*'])"
if [[ "${PHASE:-A}" == "A" ]]; then
  log "phase A: adversarial + StrongREJECT x 4 samples"
  grep -v '"fortress_benign"' data/graded_calib_prompts.jsonl > /tmp/calib_adv.jsonl
  grep '"fortress_benign"' data/graded_calib_prompts.jsonl > /tmp/calib_benign.jsonl
  python pod/gen_screen.py --model $W/models/$NAME --name $NAME --prompts /tmp/calib_adv.jsonl --out rollouts/$NAME/graded_calib.jsonl --n-samples 4 --tp $TP --max-tokens 16384 --max-len 18432
  log "phase A: benign twins x 1 sample"
  python pod/gen_screen.py --model $W/models/$NAME --name $NAME --prompts /tmp/calib_benign.jsonl --out rollouts/$NAME/graded_calib.jsonl --n-samples 1 --tp $TP --max-tokens 16384 --max-len 18432
  touch rollouts/$NAME/CALIB_DONE
else
  log "phase B: selected prompts x 20 samples (benign twins x 4)"
  grep '"block": "adv"' data/graded_main_prompts.jsonl > /tmp/main_adv.jsonl
  grep '"block": "benign"' data/graded_main_prompts.jsonl > /tmp/main_benign.jsonl
  python pod/gen_screen.py --model $W/models/$NAME --name $NAME --prompts /tmp/main_adv.jsonl --out rollouts/$NAME/graded_main.jsonl --n-samples 20 --sample-offset 100 --tp $TP --max-tokens 16384 --max-len 18432
  python pod/gen_screen.py --model $W/models/$NAME --name $NAME --prompts /tmp/main_benign.jsonl --out rollouts/$NAME/graded_main.jsonl --n-samples 4 --sample-offset 100 --tp $TP --max-tokens 16384 --max-len 18432
  touch rollouts/$NAME/MAIN_DONE
fi
log "ALL DONE"
