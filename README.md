# Breast Cancer Surveillance Observatory — Streamlit

Updated from your original dashboard.py, with dark clinical styling, four analytical tabs, responsive KPI cards, interactive Plotly charts, country explorer, and preserved glossary, exclusions and citations.

## Run

Use Python 3.10 or newer. Open a terminal in this extracted folder:

```sh
python -m pip install -r requirements.txt
python -m streamlit run dashboard.py
```

Open http://localhost:8501. Keep icons.py alongside dashboard.py and retain the hidden .streamlit folder.

## Your existing data

The upload contained dashboard.py and icons.py, but no CSV files. This version preserves your original CSV loading rather than inventing observations. Copy your existing files into:

- data/raw/pageviews_history.csv — article,date,views
- data/raw/who_gho_breast_cancer.csv — IndicatorCode,IndicatorName,SpatialDim,TimeDim,NumericValue,Value; optional Dim1
- data/raw/nigeria_registries.csv (or data/processed/nigeria_registries_clean.csv) — registry,region,years_covered,breast_asr_per_100k_women,breast_cases_n,notes,citation

The app runs without CSVs and shows unavailable-dataset notices. Published Nigeria reference values and citations remain visible; attention charts and WHO comparisons require your CSVs. No API or background ingestion is added. The React web dashboard is unchanged.

## Sources

Wikimedia Pageviews REST API; WHO Global Health Observatory; Sub-Saharan Africa PBCR Network; Jedy-Agba et al. 2012, Cancer Epidemiology (PubMed 22621842); Edo-Benin method-of-detection study (PMC12380961).

Regional registry rates must not be averaged into an unverified Nigeria national incidence estimate. Edo-Benin's 205 cases are a cohort count, not an ASR.

## Tests

```sh
python -m unittest discover -s tests
```
