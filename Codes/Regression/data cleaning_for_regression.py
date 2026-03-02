import pandas as pd
from pathlib import Path

# ---- config ----
IN_DIR  = Path(r"C:\Users\26540\Desktop\match_output_features")
OUT_DIR = IN_DIR / "cleaned"
OUT_DIR.mkdir(parents=True, exist_ok=True)

DATE_COL = "date"
RANK_COL = "rank"

START = pd.Timestamp("2019-12-29")
END   = pd.Timestamp("2024-12-29")

DROP_COLS = [
    "artist_name", "track_name", "source", "peak_rank", "previous_rank",
    "days_on_chart", "streams", "release_date", "first_entry_date",
    "first_entry_position", "total_days_on_chart", "producers", "songwriter",
]

# ---- run ----
csv_files = sorted(IN_DIR.glob("*.csv"))
print(f"Found {len(csv_files)} CSV files.")

for fp in csv_files:
    try:
        df = pd.read_csv(fp, low_memory=False)

        # ---- parse date ----
        df[DATE_COL] = pd.to_datetime(df[DATE_COL], errors="coerce")

        # ---- keep date range ----
        df = df.loc[df[DATE_COL].between(START, END, inclusive="both")].copy()

        # ---- ensure rank numeric ----
        df[RANK_COL] = pd.to_numeric(df[RANK_COL], errors="coerce")

        # ---- drop unwanted columns ----
        df = df.drop(columns=DROP_COLS, errors="ignore")

        out_fp = OUT_DIR / fp.name
        df.to_csv(out_fp, index=False, encoding="utf-8-sig")

        print(f"✓ {fp.name}: {len(df):,} rows saved")

    except Exception as e:
        print(f"✗ {fp.name}: FAILED -> {e}")