# average features
import pandas as pd
from pathlib import Path

# ---- directories ----
IN_DIR = Path(r"C:\Users\26540\Desktop\match_output_features\cleaned")
OUT_DIR = IN_DIR / "top200_weekly_means_direct"
OUT_DIR.mkdir(exist_ok=True)

# ---- config ----
START = pd.Timestamp("2019-12-29")
END   = pd.Timestamp("2024-12-29")

DATE_COL = "date"
RANK_COL = "rank"

# Weekly definition: Sunday-based week (commonly matches Google Trends weekly indexing)
WEEK_COL = "week"

FEATURE_COLS = [
    "danceability", "energy", "loudness", "speechiness",
    "acousticness", "instrumentalness", "liveness", "valence"
]

files = sorted(IN_DIR.glob("*_with_lyrics_features_sentiment.csv"))
print(f"Found {len(files)} country files in {IN_DIR}")

all_country_weeks = []

for fp in files:
    country = fp.name.split("_with_")[0]
    print(f"→ Processing {country}: {fp.name}")

    df = pd.read_csv(fp, low_memory=False)

    # ---- parse date/rank ----
    df[DATE_COL] = pd.to_datetime(df[DATE_COL], errors="coerce")
    df[RANK_COL] = pd.to_numeric(df[RANK_COL], errors="coerce")

    # ---- filter date range ----
    df = df.loc[df[DATE_COL].between(START, END, inclusive="both")].copy()

    # ---- keep Top 200 each day ----
    df = df.loc[df[RANK_COL].between(1, 200, inclusive="both")].copy()

    # ---- ensure features exist + numeric ----
    missing = [c for c in FEATURE_COLS if c not in df.columns]
    if missing:
        raise KeyError(f"{fp.name} is missing feature columns: {missing}")

    for c in FEATURE_COLS:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    # ---- map to week (Sunday-based) ----
    df[WEEK_COL] = df[DATE_COL].dt.to_period("W-SUN").dt.start_time

    # ---- weekly aggregation: mean over all Top-200 daily observations in the week ----
    weekly = (
        df.groupby(WEEK_COL, as_index=False)[FEATURE_COLS]
          .mean()
          .sort_values(WEEK_COL)
    )

    # diagnostics: number of daily song observations contributing that week
    # ideally ~ 7 * 200 = 1400 if all days present
    weekly["n_obs"] = df.groupby(WEEK_COL).size().values
    weekly["country"] = country

    # save per-country file
    out_fp = OUT_DIR / f"{country}_top200_weekly_means.csv"
    weekly.to_csv(out_fp, index=False, encoding="utf-8-sig")

    all_country_weeks.append(weekly)

# ---- combined country-week panel ----
panel = pd.concat(all_country_weeks, ignore_index=True)
panel_out = OUT_DIR / "ALL_countries_top200_weekly_panel.csv"
panel.to_csv(panel_out, index=False, encoding="utf-8-sig")

print("Done.")
print(f"Combined panel saved to: {panel_out}")