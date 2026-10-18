#!/usr/bin/env bash
set -euo pipefail
mkdir -p /workspace && cd /workspace
[[ -d SPAR-eval-awareness ]] || git clone -b eval-awareness-cot-control-exp https://github.com/hydrol0x/SPAR-eval-awareness.git
cd SPAR-eval-awareness/experiments/gptoss_ctrl_vea
python -m pip install -q -U pip
python -m pip install -q "vllm==0.31.0" hf_transfer "huggingface_hub>=0.34" safetensors accelerate
python -c "import vllm, torch, transformers; print('vllm', vllm.__version__, 'torch', torch.__version__, 'transformers', transformers.__version__)"
nvidia-smi --query-gpu=name,memory.total --format=csv
RUN_SCRIPT=${RUN_SCRIPT:-run_main.sh}
nohup bash pod/$RUN_SCRIPT > /workspace/main_run.log 2>&1 &
echo "main run launched, pid $!"
