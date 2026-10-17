#!/usr/bin/env bash
# One-shot bootstrap for a fresh RunPod PyTorch pod: clone branch, install deps, launch sweep in background.
set -euo pipefail
mkdir -p /workspace && cd /workspace
if [[ ! -d SPAR-eval-awareness ]]; then
  git clone -b eval-awareness-cot-control-exp https://github.com/hydrol0x/SPAR-eval-awareness.git
fi
cd SPAR-eval-awareness/experiments/olmo_cot_control
python -m pip install -q -U pip
python -m pip install -q "vllm>=0.11" "transformers>=4.57" hf_transfer pandas matplotlib tqdm httpx huggingface_hub
nvidia-smi --query-gpu=name,memory.total --format=csv
export CKPT_LIST="${CKPT_LIST:-scripts/checkpoints.txt}" EXTRA_ARGS="${EXTRA_ARGS:-}"
nohup bash scripts/run_sweep.sh "${N_QUESTIONS:-100}" > logs_sweep.out 2>&1 &
echo "sweep launched, pid $!"
