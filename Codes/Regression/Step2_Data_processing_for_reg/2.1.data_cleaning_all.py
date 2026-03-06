"""
Clean top song files with lyrics and audio features for the US and selected
European countries, and write cleaned versions to a subdirectory named
'cleaned'.

Cleaning includes:
1. Keep only files for the USA and EU countries.
2. Keep only observations whose date falls within the sample window.
3. Drop columns that are not needed for downstream analysis.

Tingrui Zhang
AI statement: AI is used to enhance robustness of this file.
"""

import pandas as pd
from pathlib import Path

# ---- config ----
IN_DIR = Path(r"C:\Users\26540\Desktop\match_output_features")

OUT_DIR = IN_DIR / "cleaned"
OUT_DIR.mkdir(parents=True, exist_ok=True)

DATE_COL = "date"
RANK_COL = "rank"

# Sample window for the analysis
START = pd.Timestamp("2019-12-29")
END = pd.Timestamp("2024-12-29")

# Keep only US + selected European countries
KEEP_COUNTRIES = {
    "USA",
    "Germany",
    "France",
    "United Kingdom",
    "Italy",
    "Spain",
    "Netherlands",
    "Belgium",
    "Sweden",
    "Norway",
    "Denmark",
    "Finland",
    "Ireland",
    "Austria",
    "Switzerland",
    "Portugal",
    "Poland",
    "Czech Republic",
}

# Columns to remove from the dataset
DROP_COLS = [
    "artist_name", "track_name", "source", "peak_rank", "previous_rank",
    "days_on_chart", "streams", "release_date", "first_entry_date",
    "first_entry_position", "total_days_on_chart", "producers", "songwriter",
]

# Collect all CSV files in the input directory
csv_files = sorted(IN_DIR.glob("*.csv"))
print(f"Found {len(csv_files)} CSV files.")

for fp in csv_files:
    try:
        # Infer country from filename, e.g.
        # "France_with_lyrics_features_sentiment.csv" -> "France"
        country = fp.name.split("_with_")[0].strip()

        # Skip files outside the selected country list
        if country not in KEEP_COUNTRIES:
            print(f"↷ Skipped {fp.name}: country '{country}' not in keep list")
            continue

        df = pd.read_csv(fp, low_memory=False)

        # Convert invalid date strings to NaT instead of raising an error
        df[DATE_COL] = pd.to_datetime(df[DATE_COL], errors="coerce")

        # Keep observations within the sample window
        df = df.loc[df[DATE_COL].between(START, END, inclusive="both")].copy()

        # Ensure rank is numeric, if present
        if RANK_COL in df.columns:
            df[RANK_COL] = pd.to_numeric(df[RANK_COL], errors="coerce")

        # Drop unwanted columns
        df = df.drop(columns=DROP_COLS, errors="ignore")

        # Save cleaned result
        out_fp = OUT_DIR / fp.name
        df.to_csv(out_fp, index=False, encoding="utf-8-sig")
        print(f"✓ {fp.name}: {len(df):,} rows saved")

    except Exception as e:
        print(f"✗ {fp.name}: FAILED -> {e}")