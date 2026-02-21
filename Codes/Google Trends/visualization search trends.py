import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Optional seaborn (nice heatmaps / styles)
try:
    import seaborn as sns
    HAVE_SEABORN = True
except ImportError:
    HAVE_SEABORN = False


# ----------------------------
# 1) Load data
# ----------------------------
EUROPE_PATH = "covid_trends_europe.csv"
REGION_PATH = "covid_trends_by_region.csv"

eu = pd.read_csv(EUROPE_PATH)
reg = pd.read_csv(REGION_PATH)

# Drop accidental "Unnamed: 0" columns (common in CSV exports)
for df in (eu, reg):
    drop_cols = [c for c in df.columns if c.lower().startswith("unnamed")]
    if drop_cols:
        df.drop(columns=drop_cols, inplace=True)

# Parse date
eu["date"] = pd.to_datetime(eu["date"], errors="coerce")

# Make sure COVID column exists (case-insensitive fallback)
if "COVID" not in eu.columns:
    covid_col = next((c for c in eu.columns if c.lower() == "covid"), None)
    if covid_col is None:
        raise ValueError(f"Can't find COVID column in Europe data. Columns: {eu.columns.tolist()}")
    eu.rename(columns={covid_col: "COVID"}, inplace=True)

if "COVID" not in reg.columns:
    covid_col = next((c for c in reg.columns if c.lower() == "covid"), None)
    if covid_col is None:
        raise ValueError(f"Can't find COVID column in region data. Columns: {reg.columns.tolist()}")
    reg.rename(columns={covid_col: "COVID"}, inplace=True)


# ----------------------------
# 2) Plot A: Europe average time series
# ----------------------------
avg = eu.groupby("date", as_index=False)["COVID"].mean()

plt.figure(figsize=(10, 4))
plt.plot(avg["date"], avg["COVID"])
plt.title("Average COVID Search Interest Across European Countries")
plt.xlabel("Date")
plt.ylabel("Search Interest (0–100 Index)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ----------------------------
# 3) Plot B: Overlay top-N countries (by peak)
# ----------------------------
N = 3
top_countries = (
    eu.groupby("country")["COVID"].max().sort_values(ascending=False).head(N).index
)

plt.figure(figsize=(10, 4))
for c in top_countries:
    sub = eu.loc[eu["country"] == c].sort_values("date")
    plt.plot(sub["date"], sub["COVID"], label=c)

plt.title(f"COVID Search Interest: Top {N} Countries (by Peak)")
plt.xlabel("Date")
plt.ylabel("Search Interest (0–100 Index)")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# ----------------------------
# 4) Plot C: Heatmap (country × month)
# ----------------------------
# Monthly aggregation makes the heatmap readable
eu2 = eu.dropna(subset=["date"]).copy()
eu2["month"] = eu2["date"].dt.to_period("M").dt.to_timestamp()

heat = eu2.pivot_table(index="country", columns="month", values="COVID", aggfunc="mean")

plt.figure(figsize=(14, 6))
if HAVE_SEABORN:
    sns.heatmap(heat, cbar_kws={"label": "Search Interest (0–100)"})
else:
    plt.imshow(heat.values, aspect="auto")
    plt.colorbar(label="Search Interest (0–100)")
    plt.yticks(range(len(heat.index)), heat.index)
    plt.xticks(range(len(heat.columns)), [d.strftime("%Y-%m") for d in heat.columns], rotation=90)

plt.title("COVID Search Interest Heatmap (Monthly Mean)")
plt.xlabel("Month")
plt.ylabel("Country")
plt.tight_layout()
plt.show()



