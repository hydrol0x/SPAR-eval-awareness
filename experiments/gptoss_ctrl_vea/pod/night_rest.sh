#!/usr/bin/env bash
# Overnight chain after the suppression judge (amendment 7): Experiment 3 base -> full Qwen judge of every sample-0 Exp1
# rollout (PREREG_exp1.md amendment 8) -> Experiment 3 edited and control -> results/NIGHT_DONE.
cd /workspace/SPAR-eval-awareness/experiments/gptoss_ctrl_vea
log() { echo "[$(date -u +%T)] $*"; }
export VLLM_LOGGING_LEVEL=WARNING TOKENIZERS_PARALLELISM=false VLLM_ALLOW_INSECURE_SERIALIZATION=1
until [ -f results/exp1_judge/JUDGE_DONE ]; do sleep 30; done
exp3() {  # arm samples
  local pids=""
  for k in 0 1 2; do CUDA_VISIBLE_DEVICES=$k python pod/exp3_cotcontrol.py --arm $1 --n-samples $2 --shard $k/3 \
      --data /workspace/reasonif/reasonIF_dataset.json >> /workspace/exp3_$1_s$k.log 2>&1 & pids="$pids $!"; done
  for p in $pids; do wait $p; done
}
log "exp3 base start"; exp3 base 4; touch results/EXP3_BASE_DONE; log "exp3 base done"
log "full judge start"; pids=""
for k in 0 1 2; do CUDA_VISIBLE_DEVICES=$k python pod/judge_exp1_vllm.py --model /workspace/models/judge --shard $k/3 --all-items \
    --sets fortress_adv fortress_benign --tag full_ >> /workspace/judge_full_s$k.log 2>&1 & pids="$pids $!"; done
for p in $pids; do wait $p; done
touch results/exp1_judge/JUDGE_FULL_DONE; log "full judge done"
for arm in edited control; do log "exp3 $arm start"; exp3 $arm 2; log "exp3 $arm done"; done
touch results/NIGHT_DONE; log "night done"
