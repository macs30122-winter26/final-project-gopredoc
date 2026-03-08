'''
Using the cleaned dataset with sentiment, first standardize data and then
run progressive OLS regressions of standardized COVID search intensity on
standardized Spotify audio features and text sentiment.
This file conducts regession for USA.

Nested model design:
(1) COVID_z = β0 + β1 danceability_z + ε
(2) COVID_z = β0 + β1 danceability_z + β2 energy_z + ε
(3) COVID_z = β0 + β1 danceability_z + β2 energy_z + β3 loudness_z + ε
...
until all features and text sentiment are included.

Tingrui Zhang
AI statement: AI is used to enhance robustness of this file.
'''

import pandas as pd
import numpy as np
import statsmodels.api as sm
from pathlib import Path

# ---------- paths ----------
WEEKLY_PATH = Path(r"C:\Users\26540\Desktop\Lyrics_downloaded\lyricsFeatures_weekly_aggregated.csv")
OUT_REG_RESULTS = Path(
    r"C:\Users\26540\OneDrive\Study\UChicago\Winter\MACS 30122\final-project-gopredoc\Regression_output\USA_sentiment_progressive.csv"
)

# ---------- load ----------
weekly = pd.read_csv(WEEKLY_PATH)
weekly.columns = weekly.columns.str.strip()
weekly["date"] = pd.to_datetime(weekly["date"], errors="coerce")

# ---------- restrict to USA ----------
weekly = weekly[weekly["country"] == "USA"].copy()

# ---------- required columns ----------
required = {
    "country", "date", "COVID", "danceability", "energy", "loudness",
    "speechiness", "acousticness", "instrumentalness", "liveness",
    "valence", "text_sentiment"
}
missing = required - set(weekly.columns)
if missing:
    raise ValueError(f"Missing required columns: {missing}")

# ---------- keep usable rows ----------
regression_vars_raw = [
    "COVID", "danceability", "energy", "loudness", "speechiness",
    "acousticness", "instrumentalness", "liveness", "valence",
    "text_sentiment"
]
w = weekly.dropna(subset=regression_vars_raw).copy()
w = w.sort_values("date").copy()

def zscore(s: pd.Series) -> pd.Series:
    sd = s.std()
    if sd == 0 or np.isnan(sd):
        return pd.Series(np.nan, index=s.index)
    return (s - s.mean()) / sd

# ---------- standardize for USA sample ----------
w["COVID_z"] = zscore(w["COVID"])
w["danceability_z"] = zscore(w["danceability"])
w["energy_z"] = zscore(w["energy"])
w["loudness_z"] = zscore(w["loudness"])
w["speechiness_z"] = zscore(w["speechiness"])
w["acousticness_z"] = zscore(w["acousticness"])
w["instrumentalness_z"] = zscore(w["instrumentalness"])
w["liveness_z"] = zscore(w["liveness"])
w["valence_z"] = zscore(w["valence"])
w["text_sentiment_z"] = zscore(w["text_sentiment"])

FEATURES = [
    "danceability_z",
    "energy_z",
    "loudness_z",
    "speechiness_z",
    "acousticness_z",
    "instrumentalness_z",
    "liveness_z",
    "valence_z",
    "text_sentiment_z"
]

needed = ["COVID_z"] + FEATURES
w = w.dropna(subset=needed).copy()

# ---------- run progressive nested regressions ----------
models = []

for i in range(1, len(FEATURES) + 1):
    regressors = FEATURES[:i]

    y = w["COVID_z"]
    X = sm.add_constant(w[regressors])

    model = sm.OLS(y, X).fit()
    models.append(model)

    print("\n=============================")
    print(f"Model {i}")
    print("Regressors:", regressors)
    print(model.summary())

# ---------- build regression table with p-values ----------
table = pd.DataFrame()

variables = ["const"] + FEATURES

pretty_names = {
    "const": "Constant",
    "danceability_z": "danceability",
    "energy_z": "energy",
    "loudness_z": "loudness",
    "speechiness_z": "speechiness",
    "acousticness_z": "acousticness",
    "instrumentalness_z": "instrumentalness",
    "liveness_z": "liveness",
    "valence_z": "valence",
    "text_sentiment_z": "text_sentiment"
}

for idx, model in enumerate(models):
    col_entries = []

    for var in variables:
        if var in model.params:
            coef = model.params[var]
            pval = model.pvalues[var]
            entry = f"{coef:.3f}\n({pval:.3f})"
        else:
            entry = ""
        col_entries.append(entry)

    table[f"({idx+1})"] = col_entries

table.index = [pretty_names[v] for v in variables]

# add model fit rows
table.loc["R2"] = [f"{m.rsquared:.3f}" for m in models]
table.loc["Adj_R2"] = [f"{m.rsquared_adj:.3f}" for m in models]
table.loc["N"] = [int(m.nobs) for m in models]

# ---------- save ----------
table.to_csv(OUT_REG_RESULTS)

print("\nSaved regression table:", OUT_REG_RESULTS)
print("\nPreview:")
print(table)