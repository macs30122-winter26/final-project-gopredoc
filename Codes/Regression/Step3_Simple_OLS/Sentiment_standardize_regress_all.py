'''
Using the cleaned dataset with sentiment, first standardize data and then
run per-country simple OLS:
z(text_sentiment) on z(COVID) + z(MelodyValence)

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
    r"C:\Users\26540\OneDrive\Study\UChicago\Winter\MACS 30122\final-project-gopredoc\Regression_output\sentiment_regression_results_with_melody_valence.csv"
)

# ---------- load ----------
weekly = pd.read_csv(WEEKLY_PATH)
weekly["date"] = pd.to_datetime(weekly["date"])

# ---- required columns (match equation) ----
required = {"country", "date", "COVID", "text_sentiment", "valence"}
missing = required - set(weekly.columns)
if missing:
    raise ValueError(f"Missing required columns: {missing}")

# drop missing
w = weekly.dropna(subset=["text_sentiment", "COVID", "valence"]).copy()

def zscore(s: pd.Series) -> pd.Series:
    sd = s.std()
    if sd == 0 or np.isnan(sd):
        return pd.Series(np.nan, index=s.index)
    return (s - s.mean()) / sd

results = []

for country, sub in w.groupby("country", sort=False):
    sub = sub.sort_values("date").copy()

    if len(sub) < 20:
        continue

    # -------- standardize within country --------
    sub["sentiment_z"] = zscore(sub["text_sentiment"])
    sub["COVID_z"] = zscore(sub["COVID"])
    sub["valence_z"] = zscore(sub["valence"])

    sub = sub.dropna(subset=["sentiment_z", "COVID_z", "valence_z"]).copy()
    if len(sub) < 20:
        continue

    y = sub["sentiment_z"]
    X = sm.add_constant(sub[["COVID_z", "valence_z"]])  # include intercept

    model = sm.OLS(y, X).fit()   # SIMPLE OLS (no robust SE)

    results.append({
        "country": country,
        "N": int(model.nobs),

        "beta_COVID_std": float(model.params["COVID_z"]),
        "se_COVID_std": float(model.bse["COVID_z"]),
        "p_COVID_std": float(model.pvalues["COVID_z"]),

        "beta_MelodyValence_std": float(model.params["valence_z"]),
        "se_MelodyValence_std": float(model.bse["valence_z"]),
        "p_MelodyValence_std": float(model.pvalues["valence_z"]),

        "R2": float(model.rsquared),
    })

results_df = pd.DataFrame(results).sort_values("beta_COVID_std")
results_df.to_csv(OUT_REG_RESULTS, index=False)

print("Saved regression results:", OUT_REG_RESULTS)
print("Countries estimated:", results_df.shape[0])
print(results_df.head(10))
