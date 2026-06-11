#!/usr/bin/env python3
"""
Publish a report HTML file to the Seymour Project site.

Usage:
    python3 scripts/publish_report.py \
        --title "CBD GWAS · Firth update" \
        --slug "cbd-gwas-firth" \
        --file path/to/report.html
"""
import argparse, datetime, os, subprocess, sys

REPO_ROOT   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(REPO_ROOT, "docs", "reports")

def run(cmd):
    print(f"  $ {' '.join(cmd)}")
    r = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"ERROR: {r.stderr}", file=sys.stderr)
        sys.exit(1)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--title", required=True)
    p.add_argument("--slug",  required=True)
    p.add_argument("--file",  required=True)
    args = p.parse_args()

    with open(args.file) as f:
        html = f.read()

    date     = datetime.date.today().isoformat()
    filename = f"{args.slug}-{date}.html"
    filepath = os.path.join(REPORTS_DIR, filename)

    os.makedirs(REPORTS_DIR, exist_ok=True)
    with open(filepath, "w") as f:
        f.write(html)
    print(f"Written: {filepath}")

    rel = os.path.relpath(filepath, REPO_ROOT)
    run(["git", "add", rel])
    run(["git", "commit", "-m", f"Publish {date} · {args.title}"])
    run(["git", "push"])
    print(f"\nDone! Live at: https://seymour.kurtfarrelllab.org/docs/reports/{filename}")

if __name__ == "__main__":
    main()
