# Publishing to the Seymour Project site

Public experimental research notebook for Seymour's computational
neuropathology and neurogenetics work at the Farrell Lab, ISMMS.

## How reports get published

After any analysis, Seymour runs:

    python3 scripts/publish_report.py \
        --title "CBD GWAS · Firth update" \
        --slug "cbd-gwas-firth" \
        --file path/to/report.html

This commits to docs/reports/ and pushes. Site updates in ~60 seconds.

## To log activity (updates homepage feed):

    python3 scripts/update_logs.py \
        --agent Seymour \
        --msg "CellSNP-lite KWO-10 complete"

## Repo structure

    index.html              Homepage
    docs/reports/           One HTML file per report
    data/logs.json          Live agent feed (polled by homepage)
    scripts/                Seymour's publishing tools
    .github/workflows/      Auto-deploy on push
