#!/usr/bin/env python3
"""
Append a log entry to data/logs.json and push to GitHub.

Usage:
    python3 scripts/update_logs.py --agent Seymour --msg "CellSNP done"
    python3 scripts/update_logs.py --agent Hermes  --msg "3 papers fetched"
"""
import argparse, datetime, json, os, subprocess, sys

REPO_ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS_FILE  = os.path.join(REPO_ROOT, "data", "logs.json")
MAX_ENTRIES = 50

def run(cmd):
    subprocess.run(cmd, cwd=REPO_ROOT, check=True)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--agent", required=True, choices=["Seymour","Hermes","Broker"])
    p.add_argument("--msg",   required=True)
    args = p.parse_args()

    data = {"updated": "", "entries": []}
    if os.path.exists(LOGS_FILE):
        with open(LOGS_FILE) as f:
            data = json.load(f)

    now   = datetime.datetime.utcnow()
    amap  = {"Seymour": "s", "Hermes": "h", "Broker": "b"}
    entry = {"ts": now.strftime("%H:%M"), "agent": args.agent,
             "a": amap[args.agent], "msg": args.msg}

    data["entries"].insert(0, entry)
    data["entries"]  = data["entries"][:MAX_ENTRIES]
    data["updated"]  = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    with open(LOGS_FILE, "w") as f:
        json.dump(data, f, indent=2)

    run(["git", "add", "data/logs.json"])
    run(["git", "commit", "-m", f"Log · {args.agent} · {now.strftime('%H:%M')}"])
    run(["git", "push"])
    print(f"Pushed. Feed updates in ~60s.")

if __name__ == "__main__":
    main()
