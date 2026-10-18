"""Build data/pilot_prompts.jsonl for the VEA prompt-set pilot.

Sources are downloaded from Hugging Face into a local cache. A CBRNE blocklist is applied to EVERY item, so no
chem/bio/radiological/nuclear/explosive request can enter the prompt set: those are out of scope for this project
(we only need prompts that plausibly elicit *evaluation awareness*, and milder safety-flavoured refusal prompts do
that just as well). ScaleAI/fortress_public was used in the first pilot pass and has been removed for this reason.

  python -m src.build_pilot_prompts            # writes data/pilot_prompts.jsonl
"""
from __future__ import annotations
import argparse, collections, csv, io, json, random, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "data" / "cache"
OUT = ROOT / "data" / "pilot_prompts.jsonl"

HF = "https://huggingface.co/datasets"
SOURCES = {
    "eab_safety": f"{HF}/aisa-group/EvalAwareBench/resolve/main/data/prompts_safety.jsonl",
    "eab_cap": f"{HF}/aisa-group/EvalAwareBench/resolve/main/data/prompts_capability.jsonl",
    "luxel": f"{HF}/Luxel/non-verbal-eval-awareness-contrastive-prompts-v2/resolve/main/samples.csv",
    "geo_dolci_if": f"{HF}/geodesic-research/eval-awareness-rl/resolve/main/dolci_if/train-00000-of-00001.parquet",
    "geo_harmful_refusal": f"{HF}/geodesic-research/eval-awareness-rl/resolve/main/harmful_refusal/train-00000-of-00001.parquet",
    "geo_jailbreak": f"{HF}/geodesic-research/eval-awareness-rl/resolve/main/jailbreak/train-00000-of-00001.parquet",
    "geo_over_refusal": f"{HF}/geodesic-research/eval-awareness-rl/resolve/main/over_refusal/train-00000-of-00001.parquet",
}

# Out-of-scope content. Applied to every candidate prompt; a single hit drops the item.
BLOCKLIST = re.compile(
    r"\b(anthrax|bioweapon|bio-weapon|biological weapon|pathogen|virulen\w*|nerve agent|sarin|vx gas|ricin|"
    r"nuclear|radiolog\w*|uranium|plutonium|dirty bomb|explosiv\w*|bomb|bombing|pipe bomb|gunpowder|ied|"
    r"chemical weapon|smallpox|botulinum|toxin|aerosoliz\w*|gain-of-function|select agent|"
    r"methamphetamine|fentanyl|sarin|mustard gas|chlorine gas|weaponiz\w*)\b", re.I)


def fetch(key: str) -> Path:
    CACHE.mkdir(parents=True, exist_ok=True)
    url = SOURCES[key]
    p = CACHE / (key + Path(url).suffix)
    if not p.exists():
        import httpx
        print(f"downloading {key} ...", flush=True)
        with httpx.stream("GET", url, follow_redirects=True, timeout=300) as r:
            r.raise_for_status()
            with p.open("wb") as fh:
                for chunk in r.iter_bytes():
                    fh.write(chunk)
    return p


def clean(text: str) -> bool:
    """True if the prompt is in scope (no blocklisted content)."""
    return not BLOCKLIST.search(text or "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--n-eab", type=int, default=40)
    ap.add_argument("--n-geo", type=int, default=30)
    ap.add_argument("--n-luxel", type=int, default=40)
    ap.add_argument("--n-mmlu", type=int, default=30)
    args = ap.parse_args()
    random.seed(args.seed)
    import pandas as pd

    out, skipped = [], collections.Counter()

    def add(set_name, item_id, user, meta=None, system_override=None, conditions=("none", "explicit")):
        if not clean(user) or (system_override and not clean(system_override)):
            skipped[set_name] += 1
            return
        out.append({"set": set_name, "item_id": str(item_id), "user": user, "meta": meta or {},
                    "system_override": system_override, "conditions": list(conditions)})

    # --- EvalAwareBench: paired safety tasks at 0 factors (naturalistic) and 8 factors (exaggerated eval cues)
    rows = [json.loads(l) for l in fetch("eab_safety").read_text().splitlines() if l.strip()]
    by = collections.defaultdict(dict)
    for r in rows:
        if r["num_factors_varied"] in (0, 8):
            by[r["task_id"]][r["num_factors_varied"]] = r["prompt"]
    # keep only tasks whose BOTH variants are in scope, then sample
    eligible = sorted(t for t, v in by.items() if len(v) == 2 and clean(v[0]) and clean(v[8]))
    tsel = random.sample(eligible, min(args.n_eab, len(eligible)))
    for t in tsel:
        add("eab_safety_base", t, by[t][0], {"factors": 0})
        add("eab_safety_all8", t, by[t][8], {"factors": 8})
    capsel = {t.replace("_safety", "_capability") for t in tsel[: args.n_eab // 2]}
    for l in fetch("eab_cap").read_text().splitlines():
        if not l.strip():
            continue
        r = json.loads(l)
        if r["task_id"] in capsel and r["num_factors_varied"] == 0:
            add("eab_cap_base", r["task_id"], r["prompt"], {"factors": 0})

    # --- Luxel deploy-like vs eval-like contrastive pairs, as provided
    lr = list(csv.DictReader(fetch("luxel").open()))
    pairs = collections.defaultdict(list)
    for r in lr:
        pairs[r["pair_id"]].append(r)
    ok = sorted(p for p, v in pairs.items() if len(v) == 2 and {x["context_label"] for x in v} == {"deploy_like", "eval_like"})
    for p in random.sample(ok, min(args.n_luxel, len(ok))):
        for x in pairs[p]:
            add("luxel_pairs", f'{p}|{x["context_label"]}', x["user_prompt"],
                {"context": x["context_label"], "prompt_role": x["prompt_role"], "pair_id": p},
                system_override=(x["system_prompt"] or None), conditions=("asis",))

    # --- geodesic eval-awareness-rl: highest-entropy items of each behavioural purpose
    for key, set_name in [("geo_dolci_if", "dolci_if_maxent"), ("geo_harmful_refusal", "geo_harmful_refusal"),
                          ("geo_jailbreak", "geo_jailbreak"), ("geo_over_refusal", "geo_over_refusal")]:
        d = pd.read_parquet(fetch(key)).sort_values("rank_entropy")
        n = 0
        for _, r in d.iterrows():
            if n >= args.n_geo and set_name != "dolci_if_maxent":
                break
            if n >= 40 and set_name == "dolci_if_maxent":
                break
            u = r.prompt[6:] if str(r.prompt).startswith("user: ") else r.prompt
            before = len(out)
            add(set_name, int(r.id), u, {"rank_entropy": int(r.rank_entropy), "mass_eval": float(r.mass_eval)})
            n += len(out) - before

    # --- MMLU-Pro control set: the same questions used in the Olmo experiment (known ~0 VEA)
    mmlu = ROOT.parent / "olmo_cot_control" / "rollouts" / "allenai__Olmo-3-32B-Think" / "main.jsonl"
    if mmlu.exists():
        seen = set()
        for l in mmlu.open():
            r = json.loads(l)
            if r["constraint"] == "baseline" and r["task"] == "cot" and r["qid"] not in seen:
                seen.add(r["qid"]); add("mmlu_pro", r["qid"], r["prompt"], {"domain": r["domain"]})
            if len(seen) >= args.n_mmlu:
                break

    with OUT.open("w") as fh:
        for o in out:
            fh.write(json.dumps(o) + "\n")
    print("items:", collections.Counter(o["set"] for o in out))
    print("generations:", sum(len(o["conditions"]) for o in out))
    print("dropped by blocklist:", dict(skipped))


if __name__ == "__main__":
    main()
