"""Read files from a RunPod pod through its Jupyter server (HTTP proxy), no SSH needed.

  POD_ID=... JUPYTER_TOKEN=... python scripts/pod_fetch.py ls  <remote_dir>
  POD_ID=... JUPYTER_TOKEN=... python scripts/pod_fetch.py cat <remote_file> [--tail N]
  POD_ID=... JUPYTER_TOKEN=... python scripts/pod_fetch.py sync <remote_dir> <local_dir>   # copies *.jsonl / *.txt / *.log, skipping unchanged sizes

Remote paths are relative to the Jupyter root (the pod's /workspace).
"""
from __future__ import annotations
import argparse, base64, json, os, sys
from pathlib import Path
import httpx

POD = os.environ["POD_ID"]; TOK = os.environ["JUPYTER_TOKEN"]
BASE = f"https://{POD}-8888.proxy.runpod.net/api/contents"
client = httpx.Client(timeout=120, params={"token": TOK})


def get(path: str, content: int = 1):
    r = client.get(f"{BASE}/{path.strip('/')}", params={"content": content})
    r.raise_for_status()
    return r.json()


def read_text(path: str) -> str:
    d = get(path)
    if d["format"] == "base64":
        return base64.b64decode(d["content"]).decode("utf-8", "replace")
    if d["format"] == "json":
        return json.dumps(d["content"])
    return d["content"]


def ls(path: str):
    d = get(path)
    for e in sorted(d["content"], key=lambda e: e["name"]):
        print(f"{e['type']:9s} {e.get('size') or '':>10} {e['last_modified'][:19]} {e['path']}")


def sync(remote: str, local: str, exts=(".jsonl", ".txt", ".log", ".csv", ".json")):
    Path(local).mkdir(parents=True, exist_ok=True)
    d = get(remote)
    n = 0
    for e in d["content"]:
        if e["type"] == "directory":
            sync(e["path"], str(Path(local) / e["name"]), exts); continue
        if not e["name"].endswith(exts): continue
        dst = Path(local) / e["name"]
        if dst.exists() and e.get("size") and dst.stat().st_size == e["size"]: continue
        dst.write_text(read_text(e["path"])); n += 1
        print(f"fetched {e['path']} ({e.get('size')} B)")
    return n


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("cmd", choices=["ls", "cat", "sync"]); ap.add_argument("args", nargs="*"); ap.add_argument("--tail", type=int)
    a = ap.parse_args()
    if a.cmd == "ls": ls(a.args[0] if a.args else "")
    elif a.cmd == "cat":
        t = read_text(a.args[0]); print("\n".join(t.splitlines()[-a.tail:]) if a.tail else t)
    else: print(f"synced {sync(a.args[0], a.args[1])} files")
