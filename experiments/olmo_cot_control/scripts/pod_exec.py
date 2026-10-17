"""Execute a shell command on the pod through the Jupyter kernel websocket (no SSH needed).

  POD_ID=... JUPYTER_TOKEN=... python scripts/pod_exec.py "nvidia-smi"
"""
from __future__ import annotations
import asyncio, json, os, sys, uuid
import httpx, websockets

POD = os.environ["POD_ID"]; TOK = os.environ["JUPYTER_TOKEN"]
HTTP = f"https://{POD}-8888.proxy.runpod.net"
WS = f"wss://{POD}-8888.proxy.runpod.net"


def get_kernel() -> str:
    c = httpx.Client(timeout=60, params={"token": TOK})
    ks = c.get(f"{HTTP}/api/kernels").json()
    for k in ks:
        if k.get("name", "").startswith("python"):
            return k["id"]
    return c.post(f"{HTTP}/api/kernels", json={"name": "python3"}).json()["id"]


async def run(cmd: str, timeout: float = 3600) -> int:
    kid = get_kernel()
    code = ("import subprocess,sys\n"
            f"p=subprocess.run({cmd!r}, shell=True, capture_output=True, text=True)\n"
            "sys.stdout.write(p.stdout); sys.stderr.write(p.stderr); print(f'\\n[exit {p.returncode}]')")
    sid = uuid.uuid4().hex
    async with websockets.connect(f"{WS}/api/kernels/{kid}/channels?token={TOK}&session_id={sid}", max_size=None, ping_interval=20) as ws:
        msg_id = uuid.uuid4().hex
        hdr = {"msg_id": msg_id, "username": "u", "session": sid, "msg_type": "execute_request", "version": "5.3"}
        await ws.send(json.dumps({"header": hdr, "parent_header": {}, "metadata": {}, "channel": "shell",
                                  "content": {"code": code, "silent": False, "store_history": False, "allow_stdin": False, "stop_on_error": True}}))
        rc = 0
        while True:
            m = json.loads(await asyncio.wait_for(ws.recv(), timeout=timeout))
            if m.get("parent_header", {}).get("msg_id") != msg_id:
                continue
            t = m["msg_type"]
            if t == "stream":
                sys.stdout.write(m["content"]["text"]); sys.stdout.flush()
            elif t == "error":
                print("\n".join(m["content"].get("traceback", []))); rc = 1
            elif t == "status" and m["content"]["execution_state"] == "idle":
                break
        return rc


if __name__ == "__main__":
    sys.exit(asyncio.run(run(" ".join(sys.argv[1:]))))
