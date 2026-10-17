# CoT controllability vs. verbalized eval awareness across Olmo 3 RL checkpoints

Status: **pipeline skeleton, no runs yet.** Blocked on compute for generation (see below).

## Goal
Two gaps left open by Chen Yueh-Han et al. (2026, CoT-Control) and Bharadwaj & Kirk (2026):
1. Measure CoT controllability and verbalized eval awareness on the *same* rollouts / checkpoints.
2. Compare the five Olmo-3-7B RL-Zero pipelines (IF, Math, Code, Mix, General) at their final
   checkpoints and across intermediate checkpoints, plus the Olmo-3-7B-Think RLVR trajectory.
   CoT-Control covered only Math and Code trajectories and the final General checkpoint.

## Target checkpoints (Hugging Face branches verified 2026-10-17)
| Repo | Branches |
|---|---|
| allenai/Olmo-3-7B-RL-Zero-IF | step_100 … step_1900 (19) |
| allenai/Olmo-3-7B-RL-Zero-Math | step_100 … step_1900 (19) |
| allenai/Olmo-3-7B-RL-Zero-Code | step_100 … step_2900 (29) |
| allenai/Olmo-3-7B-RL-Zero-Mix | step_50 … step_950 (19) |
| allenai/Olmo-3-7B-RL-Zero-General | step_100 … step_800 (8) |
| allenai/Olmo-3-7B-Think (RLVR stage) | step_0025 … step_1375 (55) |
| allenai/Olmo-3-7B-Think-SFT / -DPO | stage endpoints |

## Method
* Prompts: CoT-Control Appendix E "easy" RL-Zero variant (`src/prompts.py`): baseline,
  word suppression (no synonyms), `<this is not suspicious>` tag at start of reasoning,
  lowercase reasoning. Raw prompt, no chat template, for Base / RL-Zero; chat template with
  `<think>` parsing for Think checkpoints. Output controllability via the paper's Answer-IF
  prompts and LLM-judge rubric.
* Grading: programmatic graders adapted from CoT-Control (`src/grading.py`).
* Verbalized eval awareness: LLM judge following the Aranguri & Bloom (Goodfire / UK AISI 2026)
  definition, returning verbatim excerpts with CoT-vs-response location and framing
  (`src/prompts.py::VEA_JUDGE_*`). Measured separately on baseline and constrained rollouts,
  because the constraint text itself can cue "this is a test" talk.
* Judge and Answer-IF grading run through OpenRouter (`src/openrouter_client.py`, hard USD cap).

## Compute situation
* This sandbox has no GPU (4 CPU, 15 GB RAM); 7B inference here is ~1 tok/s, i.e. days per
  checkpoint. Not viable.
* OpenRouter serves **no** Olmo models and no provider serves intermediate checkpoints; the
  judge can run there, the target models cannot.
* Qwen/Qwen2.5-32B-Instruct (requested judge) is not on OpenRouter; nearest is
  `qwen/qwen-2.5-72b-instruct`.
* Plan: generation on a rented GPU with vLLM (~30M tokens for a reduced sweep ≈ 3-4 h on an
  A100), judging on OpenRouter (≈ $25-35 for ~40k rollouts with the 72B judge).

## Layout
```
data/      question sets with keyword annotations (from CoT-Control, MIT)
src/       prompts, graders, OpenRouter client (generation + judge + analysis scripts to follow)
rollouts/  raw JSONL rollouts per repo/revision/condition
results/   graded + judged tables
figures/   plots
```

## Run log
* 2026-10-17: pipeline smoke-tested on CPU (SmolLM2-135M) and judge smoke-tested on OpenRouter.
  Judges: `qwen/qwen-2.5-72b-instruct` for both verbalized eval awareness and Answer-IF
  (OpenAI models are refused on this OpenRouter key; paper used gpt-5-mini for Answer-IF).
  Generation on a RunPod L40S/A40 via `scripts/pod_bootstrap.sh`; 150 MMLU-Pro questions per
  checkpoint, 4 CoT conditions + 2 Answer-IF conditions, greedy decoding, 2048 max new tokens.
