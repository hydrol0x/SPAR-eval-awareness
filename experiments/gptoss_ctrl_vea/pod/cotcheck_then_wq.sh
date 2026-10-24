#!/usr/bin/env bash
# usage: cotcheck_then_wq.sh GPU WAIT_FILE. Once WAIT_FILE exists, run the CoT-controllability check (pod/cotcheck_exp1.py) for edited and control
# (one process per arm), then join the add-on work queue.
cd /workspace/SPAR-eval-awareness/experiments/gptoss_ctrl_vea
GPU=${1:-0}; WAIT=${2:-rollouts/olmo31_exp1_edited/DONE}
until [ -f $WAIT ]; do sleep 30; done
export VLLM_LOGGING_LEVEL=WARNING TOKENIZERS_PARALLELISM=false VLLM_ALLOW_INSECURE_SERIALIZATION=1 CUDA_VISIBLE_DEVICES=$GPU
for arm in edited control; do
  echo "[$(date -u +%T)] cotcheck $arm"; python pod/cotcheck_exp1.py --arms $arm --data /workspace/reasonif/reasonIF_dataset.json >> /workspace/cotcheck.log 2>&1
done
echo "[$(date -u +%T)] cotcheck done"; grep COTCHECK /workspace/cotcheck.log
exec bash pod/workqueue_exp1.sh $GPU $WAIT
