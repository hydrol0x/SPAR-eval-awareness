#!/usr/bin/env bash
# Amendment 7: once the suppression runs for edited and control are done, judge (provisional Qwen judge, same rules as
# JUDGE_EXP1.md) sample 0 of every adversarial prompt for edited and control in the suppression conditions and their
# comparison conditions, as three single-GPU shards; then touch results/exp1_judge/JUDGE_DONE.
cd /workspace/SPAR-eval-awareness/experiments/gptoss_ctrl_vea
until [ -f rollouts/olmo31_exp1_edited/DONE_C ] && [ -f rollouts/olmo31_exp1_control/DONE_C ] && grep -q JUDGE_DL_DONE /workspace/dl_judge.log; do sleep 30; done
echo "[$(date -u +%T)] judge start"
export VLLM_LOGGING_LEVEL=WARNING TOKENIZERS_PARALLELISM=false
pids=""
for k in 0 1 2; do
  CUDA_VISIBLE_DEVICES=$k python pod/judge_exp1_vllm.py --model /workspace/models/judge --shard $k/3 --arms edited control --all-items \
    --conditions sys_explicit_suppress user_explicit_suppress sys_suppress sys_explicit user_explicit none > /workspace/judge_s$k.log 2>&1 & pids="$pids $!"
done
for p in $pids; do wait $p; done
grep -h "wrote" /workspace/judge_s*.log
mkdir -p results/exp1_judge; touch results/exp1_judge/JUDGE_DONE; echo "[$(date -u +%T)] judge done"
