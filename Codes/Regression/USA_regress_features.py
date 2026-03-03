import pandas as pd
import statsmodels.api as sm

# ---- load data ----
FILE = r"C:/Users/26540/Desktop/match_output_lyrics_features_sentiment/cleaned/top200_weekly_means_direct/USA_top200_weekly_means_merged_trends.csv"
df = pd.read_csv(FILE)

# ---- clean column names ----
df.columns = df.columns.str.strip()

FEATURES = [
    "danceability", "energy", "loudness", "speechiness",
    "acousticness", "instrumentalness", "liveness", "valence","text_sentiment"
]

# ---- numeric ----
for col in FEATURES + ["COVID"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=FEATURES + ["COVID"]).copy()

# ---- sort by date and create trend ----
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")
df["trend"] = range(len(df))

# ---- standardize ----
for col in FEATURES + ["COVID"]:
    df[col + "_z"] = (df[col] - df[col].mean()) / df[col].std()

results = []

for feature in FEATURES:
    y = df[feature + "_z"]
    X = sm.add_constant(df[["COVID_z", "trend"]])

    model = sm.OLS(y, X).fit()

    results.append({
        "feature": feature,
        "beta_COVID_std": model.params["COVID_z"],
        "p_COVID": model.pvalues["COVID_z"],
        "beta_trend": model.params["trend"],
        "p_trend": model.pvalues["trend"],
        "R_squared": model.rsquared,
        "N": int(model.nobs)
    })

results_df = pd.DataFrame(results)

OUT_FILE = r"C:\Users\26540\OneDrive\Study\UChicago\Winter\MACS 30122\final-project-gopredoc\Regression_output\USA_feature_regressions_with_trend.csv"
results_df.to_csv(OUT_FILE, index=False)

print(results_df)
print("\nSaved to:", OUT_FILE)