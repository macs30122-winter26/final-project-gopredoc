"""
Run OLS regression of COVID search intensity on Spotify audio features
and a time trend using the standardized USA weekly panel dataset.

Tingrui Zhang
AI statement: AI is used to enhance robustness of this file.
"""


import pandas as pd
import statsmodels.api as sm

# ---- load data ----
FILE = r"C:/Users/26540/Desktop/match_output_features/cleaned/top200_weekly_means_direct/USA_top200_weekly_means_merged_trends_STD.csv"
df = pd.read_csv(FILE)

# ---- clean column names ----
df.columns = df.columns.str.strip()

FEATURES = [
    "danceability", "energy", "loudness", "speechiness",
    "acousticness", "instrumentalness", "liveness", "valence"
]

# use the *_z columns that already exist in the STD file
FEATURES_Z = [f"{c}_z" for c in FEATURES]
COVID_Z = "COVID_z"

# ---- ensure needed columns exist ----
needed = ["date", COVID_Z] + FEATURES_Z
missing = [c for c in needed if c not in df.columns]
if missing:
    raise KeyError(f"Missing columns in STD file: {missing}")

# ---- parse date + trend ----
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df.dropna(subset=["date"] + [COVID_Z] + FEATURES_Z).copy()
df = df.sort_values("date")
df["trend"] = range(len(df))  # simple linear trend (0,1,2,...)

results = []

for feature, feature_z in zip(FEATURES, FEATURES_Z):
    y = df[feature_z]  
    X = sm.add_constant(df[[COVID_Z, "trend"]])

    model = sm.OLS(y, X).fit()  # SIMPLE OLS (no robust SE)

    results.append({
        "feature": feature,
        "beta_COVID_std": float(model.params[COVID_Z]),
        "se_COVID_std": float(model.bse[COVID_Z]),
        "p_COVID": float(model.pvalues[COVID_Z]),
        "beta_trend": float(model.params["trend"]),
        "se_trend": float(model.bse["trend"]),
        "p_trend": float(model.pvalues["trend"]),
        "R_squared": float(model.rsquared),
        "N": int(model.nobs)
    })

results_df = pd.DataFrame(results)

OUT_FILE = r"C:\Users\26540\OneDrive\Study\UChicago\Winter\MACS 30122\final-project-gopredoc\Regression_output\USA_COVID_feature_regressions.csv"
results_df.to_csv(OUT_FILE, index=False)

print(results_df)
print("\nSaved to:", OUT_FILE)