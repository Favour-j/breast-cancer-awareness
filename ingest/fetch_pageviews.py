"""
fetch_pageviews.py

Pulls daily Wikipedia pageview counts for breast-cancer-related articles.
This is the LIVE tier of the dashboard — the "Awareness Trends."

Data source: Wikimedia Pageviews REST API (free, keyless).
Docs: https://wikimedia.org/api/rest_v1/

Running this daily (via GitHub Actions) to build up a real baseline before
October, so the awareness-month spike has something to compare against.
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

# --- Config -----------------------------------------------------------------

ARTICLES = [
    "Breast_cancer",
    "Mammography",
    "Breast_self-examination",
    "Breast_cancer_awareness_month",
]

# Wikimedia requires a descriptive User-Agent with contact info, or it will
# rate-limit / block requests. Replace the placeholder before running.
USER_AGENT = (
    "BreastCancerAwarenessDashboard/1.0 "
    "(https://github.com//Favour-j/breast-cancer-awareness; "
    "jokparosefavour@gmail.com)"
)

BASE_URL = (
    "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"
    "en.wikipedia/all-access/user/{article}/daily/{start}/{end}"
)

OUTPUT_PATH = Path(__file__).parent.parent / "data" / "raw" / "pageviews_history.csv"


def fetch_article_pageviews(article: str, start: str, end: str) -> pd.DataFrame:
    """Fetch daily pageviews for one article between start and end (YYYYMMDD)."""
    url = BASE_URL.format(article=article, start=start, end=end)
    headers = {"User-Agent": USER_AGENT}

    resp = requests.get(url, headers=headers, timeout=30)

    if resp.status_code == 404:
        # No data for this article/range yet — not a hard failure.
        print(f"  No data yet for {article} ({start}-{end})")
        return pd.DataFrame(columns=["article", "date", "views"])

    resp.raise_for_status()
    items = resp.json().get("items", [])

    rows = [
        {
            "article": article,
            "date": datetime.strptime(item["timestamp"][:8], "%Y%m%d").date(),
            "views": item["views"],
        }
        for item in items
    ]
    return pd.DataFrame(rows)


def load_existing_history() -> pd.DataFrame:
    if OUTPUT_PATH.exists():
        df = pd.read_csv(OUTPUT_PATH, parse_dates=["date"])
        df["date"] = df["date"].dt.date
        return df
    return pd.DataFrame(columns=["article", "date", "views"])


def main():
    existing = load_existing_history()

    # Only fetch the last 3 days each run (cheap + covers any lag in
    # Wikimedia's pipeline, which can take ~24-48h to populate).
    end_date = datetime.utcnow().date() - timedelta(days=1)
    start_date = end_date - timedelta(days=3)
    start_str = start_date.strftime("%Y%m%d")
    end_str = end_date.strftime("%Y%m%d")

    print(f"Fetching pageviews {start_str} to {end_str}...")

    new_rows = []
    for article in ARTICLES:
        print(f"  {article}")
        df = fetch_article_pageviews(article, start_str, end_str)
        new_rows.append(df)

    new_data = pd.concat(new_rows, ignore_index=True) if new_rows else pd.DataFrame()

    combined = pd.concat([existing, new_data], ignore_index=True)
    combined = combined.drop_duplicates(subset=["article", "date"], keep="last")
    combined = combined.sort_values(["article", "date"])

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    combined.to_csv(OUTPUT_PATH, index=False)

    print(f"Saved {len(combined)} total rows to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
