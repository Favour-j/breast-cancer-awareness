"""Public-facing Breast Cancer Awareness Dashboard."""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import pycountry
from pathlib import Path
from datetime import datetime

DATA_DIR = Path(__file__).parent / "data" / "raw"
PROCESSED_DIR = Path(__file__).parent / "data" / "processed"

COLOR_ACCENT = "#E8759A"
COLOR_TEAL = "#2A6F77"
COLOR_NAVY = "#1E2A38"
COLOR_IVORY = "#FAF7F2"
COLOR_ROSEGOLD = "#B76E79"

st.set_page_config(page_title="Breast Cancer Awareness Dashboard", layout="wide")


def country_name(code):
    """Convert an ISO-3 country code to a public-friendly country name."""
    if pd.isna(code) or not str(code).strip():
        return "Not reported"
    code = str(code).strip().upper()
    try:
        match = pycountry.countries.get(alpha_3=code)
        return match.name if match else code
    except Exception:
        return code


def clean_text(value):
    if pd.isna(value) or str(value).strip().lower() in {"", "none", "nan"}:
        return None
    return str(value).strip()


SEX_LABELS = {
    "SEX_FMLE": "Female",
    "SEX_MLE": "Male",
    "SEX_BTSX": "Both sexes",
}

st.title("Breast Cancer Awareness Dashboard")
st.write(
    "This dashboard tells one story at four levels: **public attention**, **global WHO data**, "
    "**published evidence from Nigerian cancer registries**, and **what the available data can responsibly tell us**."
)
st.caption(
    "Each section explains what its numbers mean. Public-attention data is not the same as disease incidence, "
    "and regional Nigerian registry figures are not presented as a national rate."
)

awareness_oct_avg = None
awareness_delta_pct = None
who_indicator_name = None
who_top_country = None
who_top_value = None
who_bottom_country = None
who_bottom_value = None
nigeria_ibadan_asr = None
nigeria_abuja_asr = None

tab1, tab2, tab3, tab4 = st.tabs(
    ["Awareness Trends", "Global Burden", "Nigeria Deep-Dive", "Key Findings"]
)

# -----------------------------------------------------------------------------
# 1. AWARENESS TRENDS
# -----------------------------------------------------------------------------
with tab1:
    st.subheader("Awareness Trends: what people are reading about")
    st.write(
        "This section tracks daily views of breast-cancer-related Wikipedia articles. "
        "It is a **signal of public attention**, not a count of breast cancer cases, diagnoses, or deaths."
    )

    pageviews_path = DATA_DIR / "pageviews_history.csv"
    if not pageviews_path.exists():
        st.warning("Awareness data has not been generated yet. Run `python ingest/fetch_pageviews.py`.")
    else:
        df = pd.read_csv(pageviews_path, parse_dates=["date"])
        articles = df["article"].dropna().unique().tolist()
        selected = st.multiselect("Choose the topics you want to compare", articles, default=articles)
        filtered = df[df["article"].isin(selected)]

        fig = go.Figure()
        for article in selected:
            article_df = filtered[filtered["article"] == article].sort_values("date")
            fig.add_trace(go.Scatter(
                x=article_df["date"], y=article_df["views"], mode="lines",
                name=article.replace("_", " ").replace("%27", "'")
            ))
        current_year = datetime.utcnow().year
        fig.add_vrect(
            x0=f"{current_year}-10-01", x1=f"{current_year}-10-31",
            fillcolor=COLOR_ACCENT, opacity=0.15, line_width=0,
            annotation_text="Breast Cancer Awareness Month", annotation_position="top left"
        )
        fig.update_layout(
            template="streamlit",
            title="Daily public attention to breast-cancer-related Wikipedia pages",
            xaxis_title="Date", yaxis_title="Wikipedia page views per day",
            legend_title="Wikipedia topic"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption("How to read this chart: a higher line means more Wikipedia page views on that day — not more breast cancer cases.")

        df["month"] = df["date"].dt.month
        oct_avg = df[df["month"] == 10]["views"].mean()
        rest_avg = df[df["month"] != 10]["views"].mean()
        if pd.notna(oct_avg) and pd.notna(rest_avg) and rest_avg > 0:
            delta_pct = ((oct_avg - rest_avg) / rest_avg) * 100
            st.metric(
                "Average daily Wikipedia views during October",
                f"{oct_avg:,.0f} views/day",
                f"{delta_pct:+.1f}% compared with the rest of the year"
            )
            awareness_oct_avg, awareness_delta_pct = oct_avg, delta_pct

# -----------------------------------------------------------------------------
# 2. GLOBAL WHO DATA
# -----------------------------------------------------------------------------
with tab2:
    st.subheader("Global Burden: what WHO reports across countries")
    st.write(
        "Choose a WHO breast-cancer-related indicator below. The dashboard shows the latest available year "
        "for that indicator and tells you whether the result is a number or a category such as Yes/No."
    )

    gho_path = DATA_DIR / "who_gho_breast_cancer.csv"
    if not gho_path.exists():
        st.warning("WHO data has not been generated yet. Run `python ingest/fetch_who_gho.py`.")
    else:
        df = pd.read_csv(gho_path)
        if "IndicatorName" not in df.columns:
            df["IndicatorName"] = df["IndicatorCode"]

        lookup = df[["IndicatorCode", "IndicatorName"]].drop_duplicates().copy()
        lookup["Display"] = lookup["IndicatorName"].fillna(lookup["IndicatorCode"])
        display_to_code = dict(zip(lookup["Display"], lookup["IndicatorCode"]))
        selected_label = st.selectbox("What would you like to explore?", list(display_to_code.keys()))
        selected_indicator = display_to_code[selected_label]
        indicator_df = df[df["IndicatorCode"] == selected_indicator].copy()

        indicator_df["Country"] = indicator_df["SpatialDim"].apply(country_name) if "SpatialDim" in indicator_df else "Not reported"
        if "Dim1" in indicator_df:
            indicator_df["Population group"] = indicator_df["Dim1"].map(SEX_LABELS).fillna(indicator_df["Dim1"])

        years = pd.to_numeric(indicator_df.get("TimeDim"), errors="coerce")
        latest_year = years.max()
        latest = indicator_df[years == latest_year].copy()
        numeric = pd.to_numeric(latest.get("NumericValue"), errors="coerce") if "NumericValue" in latest else pd.Series(index=latest.index, dtype=float)
        has_numeric = numeric.notna().any()

        st.markdown(f"### {selected_label}")
        if pd.notna(latest_year):
            st.caption(f"Latest year available in this dataset: **{int(latest_year)}** · Source: WHO Global Health Observatory")

        if has_numeric:
            latest["NumericValue"] = numeric
            st.info(
                "**How to read this:** the map compares the numeric value reported by WHO for this indicator. "
                "The indicator name and WHO-reported display value provide the meaning/context; the dashboard does not invent a unit when the source does not provide one."
            )
            fig = px.choropleth(
                latest.dropna(subset=["NumericValue"]),
                locations="SpatialDim", color="NumericValue",
                hover_name="Country",
                hover_data={"SpatialDim": False, "NumericValue": ":,.2f"},
                color_continuous_scale=[COLOR_IVORY, COLOR_ROSEGOLD, COLOR_NAVY],
                title=f"{selected_label} — latest available data ({int(latest_year)})" if pd.notna(latest_year) else selected_label,
                labels={"NumericValue": "WHO reported value"}
            )
            fig.update_layout(template="streamlit")
            st.plotly_chart(fig, use_container_width=True)

            ranked = latest.dropna(subset=["NumericValue"]).sort_values("NumericValue")
            if len(ranked) >= 2:
                who_indicator_name = selected_label
                who_bottom_country, who_bottom_value = ranked.iloc[0]["Country"], ranked.iloc[0]["NumericValue"]
                who_top_country, who_top_value = ranked.iloc[-1]["Country"], ranked.iloc[-1]["NumericValue"]
        else:
            st.info(
                "**How to read this:** this WHO indicator is a category, not a number. "
                "For example, a country may report Yes, No, or No data received. A numeric colour scale would be misleading, so no numeric map is shown."
            )
            if "Value" in latest:
                counts = latest["Value"].fillna("No data reported").value_counts()
                cols = st.columns(min(len(counts), 4)) if len(counts) else []
                for col, (label, count) in zip(cols, counts.items()):
                    col.metric(str(label), f"{count:,} countries")

        table = indicator_df.copy()
        table = table.rename(columns={"TimeDim": "Year", "Value": "WHO reported value", "NumericValue": "Numeric value"})
        show_cols = ["Country", "Year"]
        if "Population group" in table and table["Population group"].apply(clean_text).notna().any():
            show_cols.append("Population group")
        if has_numeric and "Numeric value" in table:
            show_cols.append("Numeric value")
        if "WHO reported value" in table and table["WHO reported value"].apply(clean_text).notna().any():
            show_cols.append("WHO reported value")

        st.markdown("#### Country details")
        st.caption("Country codes and WHO database field names are hidden here so the table can be read without technical knowledge.")
        st.dataframe(table[show_cols], use_container_width=True, hide_index=True)

# -----------------------------------------------------------------------------
# 3. NIGERIA DEEP-DIVE
# -----------------------------------------------------------------------------
with tab3:
    st.subheader("Nigeria Deep-Dive: what published regional registries show")
    st.write(
        "These figures come from **separate regional population-based cancer registry studies**. "
        "They should be read as evidence from the named locations and study periods — **not as one national Nigerian breast cancer rate**."
    )

    processed_path = PROCESSED_DIR / "nigeria_registries_clean.csv"
    raw_path = DATA_DIR / "nigeria_registries.csv"
    nigeria_path = processed_path if processed_path.exists() else raw_path

    if not nigeria_path.exists():
        st.warning("Nigeria registry data has not been prepared yet. Run `python ingest/nigeria_registry_data.py`.")
    else:
        df = pd.read_csv(nigeria_path)
        asr_df = df.dropna(subset=["breast_asr_per_100k_women"]).copy()

        st.markdown("### Breast cancer incidence reported by regional registries")
        st.write(
            "**Age-standardized incidence rate (ASR)** means the estimated number of new breast cancer cases per "
            "**100,000 women**, adjusted for differences in the age structure of populations. This makes rates from different populations more comparable."
        )
        if not asr_df.empty:
            fig = px.bar(
                asr_df, x="registry", y="breast_asr_per_100k_women",
                color_discrete_sequence=[COLOR_TEAL],
                title="Reported breast cancer incidence rate by Nigerian registry",
                labels={"registry": "Cancer registry", "breast_asr_per_100k_women": "New cases per 100,000 women (age-standardized)"},
                hover_data={"region": True, "years_covered": True}
            )
            fig.update_layout(template="streamlit")
            st.plotly_chart(fig, use_container_width=True)
            st.caption("Example: a value of 52 means an age-standardized rate of 52 new breast cancer cases per 100,000 women in that registry's population and study period.")

        public_table = df.rename(columns={
            "registry": "Cancer registry",
            "region": "Location",
            "years_covered": "Study period",
            "breast_asr_per_100k_women": "Breast cancer incidence rate (new cases per 100,000 women, age-standardized)",
            "breast_cases_n": "Breast cancer cases reported in study",
            "notes": "What this figure represents",
            "citation": "Published source",
        })
        st.markdown("#### Published registry evidence")
        st.dataframe(public_table, use_container_width=True, hide_index=True)
        st.caption(
            "Blank cells mean that the cited source did not report that particular measure. For example, the Edo-Benin source reports a case count, not an age-standardized incidence rate."
        )

        ibadan_row = df[df["registry"].str.contains("Ibadan", na=False)]
        abuja_row = df[df["registry"].str.contains("Abuja", na=False)]
        nigeria_ibadan_asr = ibadan_row["breast_asr_per_100k_women"].iloc[0] if not ibadan_row.empty else None
        nigeria_abuja_asr = abuja_row["breast_asr_per_100k_women"].iloc[0] if not abuja_row.empty else None

# -----------------------------------------------------------------------------
# 4. KEY FINDINGS
# -----------------------------------------------------------------------------
with tab4:
    st.subheader("Key Findings: what the available data can — and cannot — tell us")
    st.write(
        "This section turns the charts into plain-language findings. It only states conclusions supported by the data loaded into the dashboard and flags important limitations."
    )

    st.markdown("### Nigeria: regional registry rates differ")
    if nigeria_ibadan_asr is not None and nigeria_abuja_asr is not None:
        gap_pct = ((nigeria_abuja_asr - nigeria_ibadan_asr) / nigeria_ibadan_asr) * 100
        st.write(
            f"For the same 2009–2010 study period, Ibadan reported an age-standardized breast cancer incidence rate of "
            f"**{nigeria_ibadan_asr:.1f} new cases per 100,000 women**, while Abuja reported **{nigeria_abuja_asr:.1f} per 100,000 women**. "
            f"Abuja's reported rate was about **{gap_pct:.0f}% higher**."
        )
        st.info(
            "What we cannot conclude: this dashboard cannot tell us why the rates differ. The difference could reflect real regional variation, "
            "differences in diagnosis or reporting, or other factors. Further evidence is needed before assigning a cause."
        )
    else:
        st.info("Nigeria registry data is not loaded yet.")

    st.divider()
    st.markdown("### Awareness: does attention change during October?")
    if awareness_delta_pct is not None:
        direction = "higher" if awareness_delta_pct > 0 else "lower"
        st.write(
            f"Average daily Wikipedia attention during October was **{awareness_oct_avg:,.0f} views per day**, "
            f"which was **{abs(awareness_delta_pct):.1f}% {direction}** than the rest-of-year baseline in the available data."
        )
        st.caption("This describes online attention only. It does not measure diagnoses, incidence, mortality, screening uptake, or awareness in the whole population.")
    else:
        st.info("There is not enough pageview history yet to make a supported October-versus-rest-of-year comparison.")

    st.divider()
    st.markdown("### WHO: country comparisons depend on the indicator selected")
    if who_top_country is not None:
        st.write(
            f"For **{who_indicator_name}**, the latest numeric data loaded here ranges from **{who_bottom_value:,.1f} in {who_bottom_country}** "
            f"to **{who_top_value:,.1f} in {who_top_country}**."
        )
        st.info(
            "These are the highest and lowest reported numeric values in the loaded data for this indicator — not a ranking of health systems or an explanation of why countries differ. "
            "Interpret the values using the indicator's WHO definition and year shown in the Global Burden tab."
        )
    else:
        st.info("Select/load a numeric WHO indicator to populate this comparison. Categorical Yes/No indicators are summarized differently.")

st.divider()
st.caption(
    "Built by Favour Jokparose. Data sources: Wikimedia pageviews, WHO Global Health Observatory, and published Nigerian PBCR studies. "
    "This dashboard is for public education and data exploration; it is not medical advice or a substitute for professional care."
)
