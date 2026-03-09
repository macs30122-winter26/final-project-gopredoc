"""
Calculate weekly average features from the original daily feature file
to match the weekly trend data to be merged later. 
Writes modified versions to a subdirectory named 'top200_weekly_means_direct'.

Tingrui Zhang
AI statement: AI is used to enhance robustness of this file.
"""

import pandas as pd
from pathlib import Path

# ---- directories ----
IN_DIR = Path(r"C:\Users\26540\Desktop\match_output_features\cleaned")
OUT_DIR = IN_DIR / "top200_weekly_means_direct"
OUT_DIR.mkdir(exist_ok=True)

# ---- config ----
DATE_COL = "date"
WEEK_COL = "week"

FEATURE_COLS = [
    "danceability", "energy", "loudness", "speechiness",
    "acousticness", "instrumentalness", "liveness", "valence"
]

# collect all cleaned country files
files = sorted(IN_DIR.glob("*_with_lyrics_and_features.csv"))
print(f"Found {len(files)} country files in {IN_DIR}")

all_country_weeks = []

for fp in files:
    # infer country name from filename prefix
    country = fp.name.split("_with_")[0]
    print(f"→ Processing {country}: {fp.name}")

    # load cleaned daily file
    df = pd.read_csv(fp, low_memory=False)

    # enforce dtype for date and rank columns
    df[DATE_COL] = pd.to_datetime(df[DATE_COL], errors="coerce")

    # ensure all required feature columns exist
    missing = [c for c in FEATURE_COLS if c not in df.columns]
    if missing:
        raise KeyError(f"{fp.name} is missing feature columns: {missing}")

    # force feature columns to numeric
    for c in FEATURE_COLS:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    # map each daily observation to the start of its Sunday-based week
    # 2020-03-10 -> 2020-03-09 / 2020-03-15 -> 2020-03-09
    df[WEEK_COL] = df[DATE_COL].dt.to_period("W-SUN").dt.start_time

    # compute weekly mean features across all daily Top-200 observations
    weekly = (
        df.groupby(WEEK_COL, as_index=False)[FEATURE_COLS]
          .mean()
          .sort_values(WEEK_COL)
    )

    # number of daily song observations contributing to each country-week
    weekly["n_obs"] = df.groupby(WEEK_COL).size().values
    weekly["country"] = country

    # Save per-country weekly file
    out_fp = OUT_DIR / f"{country}_top200_weekly_means.csv"
    weekly.to_csv(out_fp, index=False, encoding="utf-8-sig")

    all_country_weeks.append(weekly)

# Combine all country-week files into one panel
panel = pd.concat(all_country_weeks, ignore_index=True)
panel_out = OUT_DIR / "ALL_countries_top200_weekly_panel.csv"
panel.to_csv(panel_out, index=False, encoding="utf-8-sig")

print("Done.")
print(f"Combined panel saved to: {panel_out}")
