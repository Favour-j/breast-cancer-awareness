# Key Findings and Recommendations

This is the analysis layer the dashboard itself doesn't state out loud. A
chart shows data, this section says what it means and what to do about it.

---

## Finding 1: Nigeria's two largest registries show a real, unexplained gap (real data, already confirmed)

Ibadan's age-standardized breast cancer incidence rate is 52.0 per 100,000
women. Abuja's is 64.6 per 100,000 women, about 24% higher, from the same
study period (2009-2010).

**What this could mean:** either a genuine regional difference in breast
cancer incidence between Southwest and North Central Nigeria, or a
difference in diagnostic capture and reporting completeness between the two
registries. The data alone can't distinguish between these two
explanations, and that ambiguity is worth stating directly rather than
picking whichever explanation sounds more interesting.

**Recommendation:** before treating this gap as a real epidemiological
signal, a health researcher would need to check whether Abuja's registry
had better hospital reporting infrastructure in that period, that's a
confound that would fully explain the gap without any real incidence
difference. This is a testable next step, not a conclusion.

**Why this finding matters for the project:** it demonstrates the habit of
not overclaiming from two data points, exactly the discipline the Jos
exclusion already showed.

---

## Finding 2: Awareness Trends, template to fill in once real data exists

Once `fetch_pageviews.py` has been running long enough to show a real
October, replace this section with your actual numbers. The shape to look
for:

- **Compare October's average daily views to the rest of the year's
  average.** The dashboard already computes this delta automatically (see
  the metric under the Awareness Trends chart).
- **State the real percentage**, not a guess: "October attention was X%
  higher than the yearly baseline."
- **Look at how fast it decays.** Does attention spike and hold, or spike
  and crash within days? This is the more interesting finding, campaigns
  usually care more about sustained engagement than a single-day peak.
- **A defensible recommendation once you have the real shape:** if
  attention decays fast after October 1st-3rd, the recommendation is that
  campaigns front-load messaging earlier in September rather than
  concentrating it on October 1st, since the audience's attention window is
  shorter than the awareness month itself.

Do not publish a percentage or a decay claim until the real data shows it.
A placeholder finding with invented numbers would be a worse look than no
finding at all.

---

## Finding 3: Global Burden (WHO), template to fill in once real data exists

Once `fetch_who_gho.py` has pulled real indicator data, look for:

- **Which countries have the highest and lowest incidence, and whether
  that correlates with screening infrastructure** (WHO's indicator list
  includes screening program existence, worth pulling as a second
  indicator to compare against).
- **Nigeria's own position on the global map**, compared to peer countries
  in West Africa, not just high-income countries. That comparison is more
  relevant to your audience than a Nigeria-vs-USA framing would be.
- **A defensible recommendation once you have the real numbers:** if
  Nigeria's incidence estimate is lower than comparable countries but its
  mortality-to-incidence ratio is higher, that combination usually signals
  a detection and treatment-access problem rather than a genuinely lower
  disease burden, worth flagging explicitly as the more useful reading of
  the data over the surface-level number.

---

## Where this goes

This is now built directly into the dashboard as a fourth "Key Findings"
tab in `dashboard.py`. Each finding computes live from whatever real data
is loaded, showing an honest "not enough data yet" message for the two
tiers still awaiting their first real ingestion run. Once
`fetch_pageviews.py` and `fetch_who_gho.py` have real history to work
with, the Awareness Trends and Global Burden findings above will populate
automatically, no code changes needed. In an interview, this tab is the
one to walk through first, it's the difference between describing what
you built and describing what you concluded.
