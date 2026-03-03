import pandas as pd
import numpy as np
from pathlib import Path

# ---- paths ----
FEATURES_FILE = Path(r"C:\Users\26540\Desktop\match_output_features\cleaned\top200_weekly_means_direct\USA_top200_weekly_means.csv")
TRENDS_FILE   = Path(r"C:\Users\26540\OneDrive\Study\UChicago\Winter\MACS 30122\final-project-gopredoc\Data\Google Trends\google_trends_us_weekly.csv")

OUT_FILE = FEATURES_FILE.parent / "USA_top200_weekly_means_merged_trends_STD.csv"

# ---- load ----
feat = pd.read_csv(FEATURES_FILE, low_memory=False)
tr   = pd.read_csv(TRENDS_FILE, low_memory=False)

# ---- rename week → date if needed ----
if "date" not in feat.columns and "week" in feat.columns:
    feat = feat.rename(columns={"week": "date"})
elif "date" not in feat.columns:
    raise KeyError(f"Features file missing weekly date column. Found: {list(feat.columns)}")

if "date" not in tr.columns:
    raise KeyError(f"Trends file missing 'date'. Found: {list(tr.columns)}")

# ---- parse dates ----
feat["date"] = pd.to_datetime(feat["date"], errors="coerce")
tr["date"]   = pd.to_datetime(tr["date"], errors="coerce")

# ---- align to Sunday-based week ----
feat["date"] = feat["date"].dt.to_period("W-SUN").dt.start_time
tr["date"]   = tr["date"].dt.to_period("W-SUN").dt.start_time

# ---- clean trend column names ----
tr = tr.rename(columns=lambda c: c.strip())

# ---- merge ----
merged = feat.merge(tr, on="date", how="left", validate="one_to_one")

# =====================================================
# -------- STANDARDIZATION SECTION --------------------
# =====================================================

FEATURE_COLS = [
    "danceability", "energy", "loudness", "speechiness",
    "acousticness", "instrumentalness", "liveness", "valence"
]

# Ensure numeric
for c in FEATURE_COLS:
    merged[c] = pd.to_numeric(merged[c], errors="coerce")

# Identify COVID column (assuming named "COVID")
if "COVID" not in merged.columns:
    raise KeyError("COVID column not found after merge.")

# Z-score function
def zscore(s):
    sd = s.std()
    if sd == 0 or np.isnan(sd):
        return np.nan
    return (s - s.mean()) / sd

# Standardize features
for c in FEATURE_COLS:
    merged[c + "_z"] = zscore(merged[c])

# Standardize COVID
merged["COVID_z"] = zscore(merged["COVID"])

# =====================================================

# ---- diagnostics ----
trend_cols = [c for c in tr.columns if c != "date"]
missing_rate = merged[trend_cols].isna().mean().sort_values(ascending=False)
print("Missing rate by trend column (top 10):")
print(missing_rate.head(10))

# ---- save ----
merged.to_csv(OUT_FILE, index=False, encoding="utf-8-sig")
print(f"Saved standardized merged file to:\n{OUT_FILE}")