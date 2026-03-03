import pandas as pd
from pathlib import Path

# ---------- paths ----------
EU_FEATURE_DIR = Path(r"C:\Users\26540\Desktop\match_output_features\cleaned\top200_weekly_means_direct")
EU_TRENDS_FILE = Path(r"C:\Users\26540\OneDrive\Study\UChicago\Winter\MACS 30122\final-project-gopredoc\Data\Google Trends\covid_trends_europe.csv")  # uploaded here; replace with your local path if needed

OUT_MERGED = EU_FEATURE_DIR / "EU_top200_weekly_means_merged_trends.csv"
OUT_STD    = EU_FEATURE_DIR / "EU_top200_weekly_means_merged_trends_STD.csv"

# ---------- columns to standardize ----------
FEATURE_COLS = [
    "danceability", "energy", "loudness", "speechiness",
    "acousticness", "instrumentalness", "liveness", "valence"
]
COVID_COL = "COVID"  # rename in trends if necessary

# ---------- load trends ----------
tr = pd.read_csv(EU_TRENDS_FILE, low_memory=False)
tr.columns = tr.columns.str.strip()

# If your trends file uses different column names, rename here:
# tr = tr.rename(columns={"Country": "country", "Week": "date", "covid": "COVID"})

if "country" not in tr.columns or "date" not in tr.columns:
    raise KeyError(f"Trends file must have ['country','date']. Found: {list(tr.columns)}")

tr["country"] = tr["country"].astype(str).str.strip()
tr["date"] = pd.to_datetime(tr["date"], errors="coerce").dt.to_period("W-SUN").dt.start_time

# ---------- load & stack all feature files ----------
feature_files = sorted(EU_FEATURE_DIR.glob("*_top200_weekly_means.csv"))
print(f"Found {len(feature_files)} feature files.")

panels = []
for fp in feature_files:
    df = pd.read_csv(fp, low_memory=False)
    df.columns = df.columns.str.strip()

    # standardize date col name
    if "date" not in df.columns and "week" in df.columns:
        df = df.rename(columns={"week": "date"})
    if "date" not in df.columns:
        raise KeyError(f"{fp.name} missing 'date' (or 'week'). Columns: {list(df.columns)}")

    # add country from filename if missing
    if "country" not in df.columns:
        df["country"] = fp.name.replace("_top200_weekly_means.csv", "")
    df["country"] = df["country"].astype(str).str.strip()

    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.to_period("W-SUN").dt.start_time

    panels.append(df)

feat = pd.concat(panels, ignore_index=True)

# ---------- (optional) country name harmonization ----------
country_map = {
    "UK": "United Kingdom",
    "Czechia": "Czech Republic",
}
feat["country"] = feat["country"].replace(country_map)
tr["country"]   = tr["country"].replace(country_map)

# ---------- merge ----------
merged = feat.merge(tr, on=["country", "date"], how="left")
merged.to_csv(OUT_MERGED, index=False, encoding="utf-8-sig")
print(f"Saved merged panel: {OUT_MERGED}")

# ---------- ensure numeric for standardization ----------
cols_to_z = [c for c in FEATURE_COLS if c in merged.columns]
if COVID_COL in merged.columns:
    cols_to_z.append(COVID_COL)
else:
    raise KeyError(f"Could not find '{COVID_COL}' in merged data. Trends columns: {list(tr.columns)}")

for c in cols_to_z:
    merged[c] = pd.to_numeric(merged[c], errors="coerce")

# drop rows missing any variables we standardize (keeps zscores well-defined)
std_df = merged.dropna(subset=cols_to_z).copy()

# ---------- GLOBAL standardization (like US) ----------
# Within-country z-scores
for c in cols_to_z:
    std_df[c + "_z_within_country"] = std_df.groupby("country")[c].transform(
        lambda s: (s - s.mean()) / s.std()
    )
std_df.to_csv(OUT_STD, index=False, encoding="utf-8-sig")
print(f"Saved standardized panel (global z): {OUT_STD}")