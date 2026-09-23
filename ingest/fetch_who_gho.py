"""
fetch_who_gho.py

Pulls breast-cancer-related indicators by country from the WHO Global Health
Observatory OData API. This is the ANNUAL / global tier of the dashboard.

The script searches by indicator name instead of hard-coding WHO codes, then
stores both IndicatorCode and IndicatorName so the dashboard can show readable
labels while retaining the source code for traceability.
"""

import requests
import pandas as pd
from pathlib import Path

BASE_URL = "https://ghoapi.azureedge.net/api"
SEARCH_TERMS = ["breast cancer", "malignant neoplasms of the female breast"]
OUTPUT_PATH = Path(__file__).parent.parent / "data" / "raw" / "who_gho_breast_cancer.csv"


def find_indicator_codes(search_term: str) -> pd.DataFrame:
    url = f"{BASE_URL}/Indicator?$filter=contains(IndicatorName,'{search_term}')"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    return pd.DataFrame(resp.json().get("value", []))


def fetch_indicator_data(indicator_code: str) -> pd.DataFrame:
    url = f"{BASE_URL}/{indicator_code}"
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    df = pd.DataFrame(resp.json().get("value", []))
    if not df.empty:
        df["IndicatorCode"] = indicator_code
    return df


def main():
    print("Searching for breast cancer indicators...")
    matches = []
    for term in SEARCH_TERMS:
        found = find_indicator_codes(term)
        if not found.empty:
            matches.append(found)
            print(f"  '{term}' matched {len(found)} indicator(s):")
            for _, row in found.iterrows():
                print(f"    {row['IndicatorCode']}: {row['IndicatorName']}")

    if not matches:
        print("No matching indicators found — check search terms.")
        return

    indicators = pd.concat(matches, ignore_index=True).drop_duplicates("IndicatorCode")
    name_map = indicators.set_index("IndicatorCode")["IndicatorName"].to_dict()

    print("\nFetching data for each matched indicator...")
    all_data = []
    for code in indicators["IndicatorCode"]:
        print(f"  {code}")
        df = fetch_indicator_data(code)
        if not df.empty:
            df["IndicatorName"] = name_map.get(code, code)
            all_data.append(df)

    if not all_data:
        print("No data returned for any matched indicator.")
        return

    combined = pd.concat(all_data, ignore_index=True)
    keep_cols = [c for c in [
        "IndicatorCode", "IndicatorName", "SpatialDim", "TimeDim", "Dim1",
        "NumericValue", "Value"
    ] if c in combined.columns]
    combined = combined[keep_cols]

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    combined.to_csv(OUTPUT_PATH, index=False)
    print(f"\nSaved {len(combined)} rows to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
