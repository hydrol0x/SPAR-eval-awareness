"""Build the graded-compliance prompt pool (GRADED_PLAN.md): FORTRESS without its CBRNE domain, plus StrongREJECT.

FORTRESS rows whose risk_domain is CBRNE are dropped by label before anything is written, and the CBRNE blocklist is
applied to every remaining prompt (adversarial and benign twin). The raw FORTRESS parquet is deleted after filtering.

  python -m src.build_graded_prompts --fortress-parquet /path/to/raw.parquet   # needs pyarrow
"""
from __future__ import annotations
import argparse, collections, csv, io, json, os, urllib.request

from .build_pilot_prompts import CACHE, ROOT, clean

SR_URL = "https://raw.githubusercontent.com/alexandrasouly/strongreject/main/strongreject_dataset/strongreject_dataset.csv"
OUT = ROOT / "data" / "graded_calib_prompts.jsonl"


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--fortress-parquet", required=True); a = ap.parse_args()
    import pyarrow.parquet as pq
    CACHE.mkdir(parents=True, exist_ok=True)
    rows = [r for r in pq.read_table(a.fortress_parquet).to_pylist() if "CBRNE" not in r["risk_domain"]]
    os.remove(a.fortress_parquet)
    out, drop = [], collections.Counter()
    for r in rows:
        if not (clean(r["adversarial_prompt"]) and clean(r["benign_prompt"]) and clean(r["rubric"] if isinstance(r["rubric"], str) else json.dumps(r["rubric"]))):
            drop["fortress_blocklist"] += 1; continue
        meta = {"risk_domain": r["risk_domain"], "risk_subdomain": r["risk_subdomain"]}
        out.append({"set": "fortress_adv", "item_id": str(r["ID"]), "condition": "none", "system": None, "user": r["adversarial_prompt"], "meta": meta})
        out.append({"set": "fortress_benign", "item_id": str(r["ID"]), "condition": "none", "system": None, "user": r["benign_prompt"], "meta": meta})
    sr = list(csv.DictReader(io.StringIO(urllib.request.urlopen(SR_URL, timeout=60).read().decode())))
    for i, r in enumerate(sr):
        if not clean(r["forbidden_prompt"]):
            drop["strongreject_blocklist"] += 1; continue
        out.append({"set": "strongreject", "item_id": f"sr{i:03d}", "condition": "none", "system": None, "user": r["forbidden_prompt"],
                    "meta": {"category": r.get("category"), "source": r.get("source")}})
    with OUT.open("w") as fh:
        for o in out:
            fh.write(json.dumps(o) + "\n")
    print("dropped by blocklist:", dict(drop))
    for k, v in sorted(collections.Counter(o["set"] for o in out).items()):
        print(k, v)
    print("StrongREJECT categories kept:", dict(collections.Counter(o["meta"]["category"] for o in out if o["set"] == "strongreject")))


if __name__ == "__main__":
    main()
