"""
nigeria_registry_data.py

This is the STATIC tier — there is no live API for Nigerian cancer
registry data. Nigeria does not (yet) have a single unified national
cancer registry; the numbers here are hand-compiled from published
population-based cancer registry (PBCR) studies.

This script does NOT fetch anything. It loads and validates the
hand-compiled CSV against an expected schema, so a typo in the data
file gets caught before it silently breaks the dashboard.

To update: edit data/raw/nigeria_registries.csv directly, keeping the
`citation` column filled in for every row — that's what lets the
dashboard disclose its sourcing honestly instead of implying a single
official dataset exists.
"""

import pandas as pd
from pathlib import Path

INPUT_PATH = Path(__file__).parent.parent / "data" / "raw" / "nigeria_registries.csv"
OUTPUT_PATH = Path(__file__).parent.parent / "data" / "processed" / "nigeria_registries_clean.csv"

EXPECTED_COLUMNS = [
    "registry",
    "region",
    "years_covered",
    "breast_asr_per_100k_women",
    "breast_cases_n",
    "notes",
    "citation",
]


def load_and_validate() -> pd.DataFrame:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"{INPUT_PATH} not found. This file is hand-compiled — see the "
            "docstring above for how to build it."
        )

    df = pd.read_csv(INPUT_PATH)

    missing_cols = set(EXPECTED_COLUMNS) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing expected columns: {missing_cols}")

    if df["citation"].isna().any() or (df["citation"].str.strip() == "").any():
        bad_rows = df[df["citation"].isna() | (df["citation"].str.strip() == "")]
        raise ValueError(
            f"Every row must have a citation. Rows missing one:\n{bad_rows[['registry']]}"
        )

    # Every row should have EITHER an ASR OR a case count — otherwise
    # there's nothing to plot for that registry.
    no_data_mask = df["breast_asr_per_100k_women"].isna() & df["breast_cases_n"].isna()
    if no_data_mask.any():
        raise ValueError(
            f"Rows with neither an ASR nor a case count:\n{df[no_data_mask][['registry']]}"
        )

    return df


def main():
    df = load_and_validate()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Validated {len(df)} registry rows. Saved clean copy to {OUTPUT_PATH}")
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()
