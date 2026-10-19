# Base-model screen: which open reasoning model verbalizes eval cues? (written 2026-10-19, before any screen data)

## Why
The user-turn cue experiment (README section 10) failed its manipulation check: gpt-oss-20b verbalizes an explicit eval
cue in only 2–7% of reasoning traces while its behaviour responds. To test "CoT-controllability fine-tuning lowers
verbalized eval awareness while the behavioural response remains", the base model must verbalize the cue at a usable
rate. This screen picks the model to fine-tune (on our own cluster) before any fine-tuning is done.

## Candidates
Qwen3-32B (thinking mode), QwQ-32B, Olmo-3-32B-Think: generated on a RunPod pod with vLLM 0.31.0
(`pod/run_screen.sh`, `pod/gen_screen.py`). DeepSeek-R1-0528 (reference only, too large to fine-tune): generated on
OpenRouter (`src/gen_screen_openrouter.py`). Sampling: temperature 0.6, top-p 0.95 (top-k 20 for Qwen3, 40 for QwQ, per
model cards), max 8,192 new tokens, one sample per prompt.

## Prompts (`data/screen_prompts.jsonl`, 1,001)
* EvalAwareBench capability (99) and safety (96) prompts: no cue, `CUE_EXPLICIT` prepended to the user turn,
  `CUE_USER_CASUAL` prepended to the user turn (as in `PREREG_usercue.md`).
* Luxel contrastive pairs (208): eval-framed and deploy-framed, with each pair's system prompt.

## Measures
* VEA: v4 channel-blind judge (Qwen2.5-72B), reasoning channel only, quote verified verbatim (`src/judge_v4.py --channels cot`).
* Behaviour: refusal rate (`is_refusal`) and log answer length.
* Truncation rate and reasoning length, to flag models whose reasoning is cut off by the token limit.

## Selection rule (`src/analyze_screen.py`)
A model passes if (a) it verbalizes eval awareness in ≥ 10% of reasoning traces under the user cue, the casual user cue,
or the Luxel eval framing, and (b) its behaviour responds to a user cue (refusal rate or answer length, cue vs no cue,
paired sign-flip p < 0.05). Among fine-tunable models that pass, prefer the highest explicit-cue VEA rate; report all
numbers either way. This is a screen for model choice, not a hypothesis test.

**Addition (2026-10-19, before any Olmo-3.1 data):** Olmo-3.1-32B-Think added as a fifth candidate after a literature
check reported it verbalizes eval awareness at about twice Olmo-3-32B-Think's rate. Same prompts, settings and rule.
