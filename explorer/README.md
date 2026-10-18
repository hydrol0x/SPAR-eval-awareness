# Rollout Atlas

A static browser for every rollout in this repo: the gpt-oss-20b fine-tune and steering experiment
(six models, main run, confirmatory rerun, controllability check), the gpt-oss pilot, and all 76 Olmo-3
7B / 32B checkpoints from the CoT-controllability sweep.

## Run it locally

```bash
python explorer/build.py                      # ~20 s, writes explorer/data/ (about 350 MB, gitignored)
python -m http.server 8000 -d explorer        # then open http://localhost:8000
```

Python 3.9+ with the standard library only. Rebuild after new rollouts or judgments land.

## GitHub Pages

`.github/workflows/explorer-pages.yml` builds the data in CI and publishes the site on every push to
`eval-awareness-cot-control-exp` that touches `experiments/` or `explorer/`. One-time setup in the repo:
Settings → Pages → Build and deployment → Source: **GitHub Actions**. The site is public, like the repo.

## What it shows

* **Filters:** model, condition / constraint, text search (regex) in reasoning, answer or prompt, and label
  chips that cycle any → yes → no. gpt-oss labels: cue mentioned in the reasoning by each v4 judge, v4 judges
  disagree, v3 judge flagged, v3 quote not in the model text, cue words echoed, refusal, token limit, and for the
  controllability check whether the reasoning follows the instruction. Olmo labels: follows the constraint, talks
  about the constraint, correct answer, Answer-IF compliant, judge flagged, judge quote not in model text.
* **Highlights:** the eval cue in the prompt; v4 judge quotes (verified to be in the model text); v3 judge quotes;
  words from the cue echoed in the reasoning; your search. For Olmo: the banned word, the required tag, and
  capital letters under a lowercase rule.
* **Judges table:** every judge's verdict and quote, and where the quote actually occurs (reasoning, answer, or only
  in the prompt, which is the v3 artifact).
* **Same prompt, all models** (`p`): the six gpt-oss models side by side on one prompt and sample; for Olmo, one
  question under every constraint.
* **Links:** the URL hash keeps the view and the selected rollout, so a link opens the same rollout.

Keys: `j` / `k` next and previous, `p` side-by-side view, `/` search, `Esc` back.
