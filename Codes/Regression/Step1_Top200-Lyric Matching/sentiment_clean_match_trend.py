# Clean + merge COVID only + weekly aggregation (country-week)

import pandas as pd
from pathlib import Path

# ---------- paths ----------
LYRICS_PATH   = Path(r"C:\Users\26540\Desktop\Lyrics_downloaded\lyricsFeatures_mergeERUS_clean_enonly_token_pos_ldaTfidf.csv")
EU_TRENDS_PATH = Path(r"C:\Users\26540\OneDrive\Study\UChicago\Winter\MACS 30122\final-project-gopredoc\Data\Google Trends\covid_trends_europe.csv")
US_TRENDS_PATH = Path(r"C:\Users\26540\OneDrive\Study\UChicago\Winter\MACS 30122\final-project-gopredoc\Data\Google Trends\google_trends_us_weekly.csv")

OUT_WEEKLY = Path(r"C:\Users\26540\Desktop\Lyrics_downloaded\lyricsFeatures_weekly_aggregated.csv")

# ---------- config ----------
start = pd.to_datetime("2019-12-29")
end   = pd.to_datetime("2024-12-29")

# ---------- load ----------
df = pd.read_csv(LYRICS_PATH)
eu = pd.read_csv(EU_TRENDS_PATH)
us = pd.read_csv(US_TRENDS_PATH)

# ---------- parse dates ----------
df["date"] = pd.to_datetime(df["date"])
eu["date"] = pd.to_datetime(eu["date"])
us["date"] = pd.to_datetime(us["date"])

# ---------- map song daily dates -> Sunday week dates ----------
# pandas weekday: Mon=0 ... Sun=6; days_since_sun = (weekday+1)%7 -> 0 on Sunday
days_since_sun = (df["date"].dt.weekday + 1) % 7
df["week_date"] = df["date"] - pd.to_timedelta(days_since_sun, unit="D")

# keep only within [start, end] on both daily and week date
df = df[(df["date"] >= start) & (df["date"] <= end)].copy()
df = df[(df["week_date"] >= start) & (df["week_date"] <= end)].copy()

# keep original daily date as chart_date; use week_date as date for merging
df = df.rename(columns={"date": "chart_date"})
df["date"] = df["week_date"]
df = df.drop(columns=["week_date"])

# ---------- trends: keep ONLY COVID ----------
eu_covid = eu[["date", "country", "COVID"]].copy()
us_covid = us[["date", "COVID"]].copy()
us_covid["country"] = "USA"

trends = pd.concat([eu_covid, us_covid[["date", "country", "COVID"]]], ignore_index=True)
trends = trends[(trends["date"] >= start) & (trends["date"] <= end)].copy()

# ---------- merge COVID into song-level ----------
df = df.merge(trends, on=["country", "date"], how="left", validate="m:1")

# ---------- weekly aggregation ----------
numeric_cols = df.select_dtypes(include="number").columns.tolist()
numeric_feature_cols = [c for c in numeric_cols if c != "COVID"]

agg = {c: "mean" for c in numeric_feature_cols}
agg["COVID"] = "first"  # constant within country-week

weekly = (
    df.groupby(["country", "date"], as_index=False)
      .agg(agg)
)

# ---------- standardize (z-score) within country ----------
# columns to standardize = all numeric columns except the date key
num_cols_weekly = weekly.select_dtypes(include="number").columns.tolist()

def zscore(s: pd.Series) -> pd.Series:
    sd = s.std(ddof=0)
    if sd == 0 or pd.isna(sd):
        return pd.Series(pd.NA, index=s.index)
    return (s - s.mean()) / sd

for c in num_cols_weekly:
    weekly[f"{c}_z"] = weekly.groupby("country")[c].transform(zscore)


# ---------- save ----------
weekly.to_csv(OUT_WEEKLY, index=False)
print("Saved weekly dataset:", OUT_WEEKLY)
print("Shape:", weekly.shape)
print(weekly.head())