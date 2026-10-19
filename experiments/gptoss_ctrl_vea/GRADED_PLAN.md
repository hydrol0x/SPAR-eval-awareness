# Graded compliance under an eval cue, base Qwen3-32B (written 2026-10-19, before any data)

## Why
Refusal rate barely moves with an eval cue on Qwen3-32B (screen: +1 to +3 pp, n.s.), likely a ceiling effect on
mostly-refused prompts. Published eval-awareness work on Qwen3-32B finds larger behaviour shifts with graded compliance
scores on prompts of intermediate difficulty (FORTRESS, StrongREJECT). This sets up the behavioural measure for the
fine-tuning experiment: "aware but quiet" means the cue still shifts graded compliance in rollouts that no longer
verbalize eval awareness.

## Data (no CBRNE)
`src/build_graded_prompts.py` → `data/graded_calib_prompts.jsonl`:
* FORTRESS (ScaleAI/fortress_public) adversarial prompts and their benign twins, **CBRNE risk domain dropped by label**
  (only Criminal & Financial Illicit Activities and Political Violence & Terrorism kept), then the CBRNE blocklist on
  every prompt: 282 pairs. The raw download is deleted after filtering.
* StrongREJECT (302 prompts after the blocklist; categories: disinformation, hate/harassment, illegal goods, non-violent
  crimes, sexual content, violence).

## Generation
Qwen3-32B (thinking) on OpenRouter, provider pinned to DeepInfra (fp8), no fallbacks; temperature 0.6, top-p 0.95,
top-k 20, max 8,192 tokens (`src/gen_screen_openrouter.py`).

## Phase A: calibration
Adversarial and StrongREJECT prompts × no cue × 8 samples; benign twins × no cue × 2 samples. Scored with the StrongREJECT
rubric (`src/judge_strongreject.py`, Qwen2.5-72B judge; final answer only, request shown without any cue).

## Selection (`src/select_graded.py`)
Prompts whose calibration compliance (share of samples not refused) is in [0.2, 0.8]; if fewer than 60 qualify, [0.1, 0.9].
At most 100 prompts (seeded random subset).

## Phase B: main run
Selected prompts × {no cue, `CUE_USER_CASUAL` prepended to the user turn} × 20 samples (sample indices 100–119); benign
twins of selected FORTRESS prompts × both conditions × 4 samples. Measures: StrongREJECT score and refusal; VEA in the
reasoning (v4 judge, reasoning channel, verified quote).

## Analysis (`src/analyze_graded.py`)
Paired by prompt, sign-flip permutation p, bootstrap CI:
1. Cue effect on VEA, compliance rate and StrongREJECT score.
2. Cue effect on score using only cue-condition rollouts that do NOT verbalize eval awareness (vs all no-cue rollouts).
3. Within the cue condition, score of verbalizing vs non-verbalizing rollouts (observational).
4. Benign twins: cue effect on compliance (over-refusal).
This is a base-model measurement to fix the behavioural metric and prompt set; it tests no fine-tuning hypothesis.

## Amendment (2026-10-19, before any data): model and sizes
After the base-model screen (README section 12), the model is **Olmo-3.1-32B-Think** (the planned fine-tuning target)
instead of Qwen3-32B. It is not served on OpenRouter, so generation runs on a RunPod pod with vLLM 0.31.0, bf16, tensor
parallel over 2 GPUs (`pod/run_graded.sh`, `PHASE=A` / `PHASE=B`), sampling per AllenAI (temperature 0.6, top-p 0.95,
no top-k) with max 16,384 new tokens (AllenAI recommends 32,768; 8,192 truncated 3.1% of screen traces).
* Phase A: 4 samples per adversarial / StrongREJECT prompt (was 8), 1 per benign twin (was 2).
* Selection: compliance in [0.25, 0.75] over ≥ 3 judged samples (i.e. 1–3 of 4 complying); at most 80 prompts (was 100).
* Phase B unchanged (20 samples per prompt and condition; benign twins 4).
* Arm name `olmo31_32b_think`. Judges unchanged (StrongREJECT rubric and v4 VEA judge, Qwen2.5-72B on OpenRouter);
  the VEA judge may use the regex prefilter (`src/regex_judge.py`, README section 11).

## Amendment 2 (2026-10-19, before any data): hardware
No CUDA-13 machines were available for hours; only a single H100 with an older driver. Generation therefore runs on
1×H100 with vLLM 0.31.0's CUDA 12.9 build (same vLLM/torch versions as the screen), with the FlashAttention backend and a bf16 KV cache
(an fp8 KV cache was planned but fails to compile on the Blackwell GPU we got, so it was dropped before any data). Phase A runs in two passes: 2 samples per adversarial / StrongREJECT prompt (+1 per benign
twin), then up to 4 if the budget allows; selection uses whatever samples exist (≥ 2 judged), keeping prompts whose
compliance is strictly between 0 and 1.
