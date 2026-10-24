#!/usr/bin/env bash
# Waits for all Exp1 generation (main + add-on, three arms) and the judge download, then runs the provisional Qwen judge
# as three single-GPU shards (pod/judge_exp1_vllm.py) and touches results/exp1_judge/JUDGE_DONE.
cd /workspace/SPAR-eval-awareness/experiments/gptoss_ctrl_vea
R=rollouts
until [ -f $R/olmo31_exp1_base/DONE_B ] && [ -f $R/olmo31_exp1_edited/DONE_B ] && [ -f $R/olmo31_exp1_control/DONE_B ] \
      && grep -q JUDGE_DL_DONE /workspace/dl_judge.log; do sleep 60; done
echo "[$(date -u +%T)] judge start"
export VLLM_LOGGING_LEVEL=WARNING TOKENIZERS_PARALLELISM=false
pids=""
for k in 0 1 2; do CUDA_VISIBLE_DEVICES=$k python pod/judge_exp1_vllm.py --model /workspace/models/judge --shard $k/3 > /workspace/judge_s$k.log 2>&1 & pids="$pids $!"; done
for p in $pids; do wait $p; done
grep -h "wrote" /workspace/judge_s*.log
touch results/exp1_judge/JUDGE_DONE; echo "[$(date -u +%T)] judge done"
