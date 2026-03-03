import pandas as pd
from pathlib import Path

# ---- paths ----
FEATURES_FILE = Path(r"C:\Users\26540\Desktop\match_output_features\cleaned\top200_weekly_means_direct\USA_top200_weekly_means.csv")
TRENDS_FILE   = Path(r"C:\Users\26540\OneDrive\Study\UChicago\Winter\MACS 30122\final-project-gopredoc\Data\Google Trends\google_trends_us_weekly.csv")

OUT_FILE = FEATURES_FILE.parent / "USA_top200_weekly_means_merged_trends.csv"

# ---- load ----
feat = pd.read_csv(FEATURES_FILE, low_memory=False)
tr   = pd.read_csv(TRENDS_FILE, low_memory=False)

# ---- standardize date column names ----
# features have "week" not "date"
if "date" not in feat.columns and "week" in feat.columns:
    feat = feat.rename(columns={"week": "date"})
elif "date" not in feat.columns:
    raise KeyError(f"Features file missing a weekly date column. Found columns: {list(feat.columns)}")

# trends file should have "date" (if not, adjust here)
if "date" not in tr.columns:
    raise KeyError(f"Trends file missing 'date'. Found columns: {list(tr.columns)}")

# ---- parse dates ----
feat["date"] = pd.to_datetime(feat["date"], errors="coerce")
tr["date"]   = pd.to_datetime(tr["date"], errors="coerce")

# ---- align weekly indexing (Sunday-based week start) ----
# This prevents merge failures when one file uses week-start vs week-end labels.
feat["date"] = feat["date"].dt.to_period("W-SUN").dt.start_time
tr["date"]   = tr["date"].dt.to_period("W-SUN").dt.start_time

# ---- optional: clean trend column names ----
tr = tr.rename(columns=lambda c: c.strip())

# ---- merge ----
merged = feat.merge(tr, on="date", how="left", validate="one_to_one")

# ---- diagnostics ----
trend_cols = [c for c in tr.columns if c != "date"]
missing_rate = merged[trend_cols].isna().mean().sort_values(ascending=False)
print("Missing rate by trend column (top 10):")
print(missing_rate.head(10))

# ---- save ----
merged.to_csv(OUT_FILE, index=False, encoding="utf-8-sig")
print(f"Saved merged file to:\n{OUT_FILE}")
