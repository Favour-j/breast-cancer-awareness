# Breast Cancer Awareness Dashboard

A three-tier live dashboard built for Breast Cancer Awareness Month (October),
deliberately structured around how fast each kind of health data actually
moves, not forced into one uniform update cycle.

## Overview

**Key Findings tab** (computes and states real findings once each tier has data, never invents a number ahead of it existing):

![Key Findings tab showing the Nigeria registry gap finding and honest not-yet-available states for the other two tiers](docs/screenshots/key-findings-tab.png)

**Nigeria Deep-Dive tab** (already populated with real, cited registry data):

![Nigeria Deep-Dive tab showing a bar chart of breast cancer incidence rates by registry](docs/screenshots/nigeria-deep-dive-tab.png)

**Awareness Trends tab** (local preview before the live pageviews pipeline is running):

![Awareness Trends tab landing view](docs/screenshots/awareness-trends-tab.png)

The Awareness Trends and Global Burden tabs, and their corresponding
findings, populate once their ingestion scripts have run at least once,
either locally or via the daily GitHub Action. The Nigeria Deep-Dive tab
and its finding are static, hand-compiled data, so they're already live in
these screenshots.

## Tiers

| Tier | Cadence | Source | Why this cadence |
|---|---|---|---|
| **Awareness Trends** | Live (daily) | [Wikimedia Pageviews API](https://wikimedia.org/api/rest_v1/) | Public search/attention genuinely changes day to day, this is the only tier where "live" is a truthful claim. |
| **Global Burden** | Annual | [WHO Global Health Observatory](https://www.who.int/data/gho) | Incidence, mortality, and survival estimates are released on WHO's annual cycle. |
| **Nigeria Deep-Dive** | Static | Published PBCR studies (Ibadan, Abuja, Edo-Benin) | Nigeria has no single unified national cancer registry yet, these figures come from separate regional studies, cited individually. |

## Key Findings tab

A fourth tab, `Key Findings`, states actual conclusions rather than just
displaying charts. Each finding is computed live from whatever real data is
loaded, if a tier's data isn't populated yet, that section shows an honest
"not enough data yet" message instead of a placeholder number. See
`KEY_FINDINGS.md` for the full write-up behind each finding.

## Why not just use Google Trends?

Google Trends' unofficial Python client (`pytrends`) was archived by its
maintainers in April 2025 and is no longer reliably maintained. Wikipedia's
official Pageviews API is free, keyless, and stable, so it's used here
instead as the live-attention proxy.

## Setup

```bash
pip install -r requirements.txt

# Populate each tier
python ingest/fetch_pageviews.py
python ingest/fetch_who_gho.py
python ingest/nigeria_registry_data.py   # validates data/raw/nigeria_registries.csv

# Run locally
streamlit run dashboard.py
```

No API keys are required for any of the three data sources.

## Automation

`.github/workflows/daily_pageviews.yml` runs `fetch_pageviews.py` every day at
06:00 UTC and commits the updated history, so the Awareness Trends tier keeps
building a real baseline automatically once deployed. The WHO and Nigeria
tiers are re-run manually when new annual data or registry studies are
published, they don't need daily automation.

## A note on the Nigeria data

There is currently no single official, unified breast cancer registry for
Nigeria. The figures in the Nigeria Deep-Dive tab are compiled from three
published population-based cancer registry studies with isolable
breast-cancer figures (Ibadan, Abuja, Edo-Benin). A fourth registry, the Jos
PBCR, also operates but its published study reports only total cancer cases
across all types without breaking out breast cancer specifically, so it's
mentioned here for completeness but not included as a data row.

Every row in `data/raw/nigeria_registries.csv` carries its own citation,
this is disclosed directly in the dashboard rather than presented as one
authoritative national dataset.

## Stack

Python, pandas, Streamlit, Plotly, GitHub Actions, Streamlit Community Cloud

## Author

Favour Jokparose, data analyst, Lagos.
