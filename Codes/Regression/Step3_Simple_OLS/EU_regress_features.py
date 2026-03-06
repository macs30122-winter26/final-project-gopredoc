"""
Run OLS regressions of COVID search intensity on Spotify audio features and a 
time trend using the standardized EU weekly panel dataset.

This script performs two analyses:
1. Country-level regressions
2. Pooled Europe regressions

Tingrui Zhang
AI statement: AI is used to enhance robustness of this file.
"""

import pandas as pd
import statsmodels.api as sm

# ---- load standardized EU panel ----
"""Load the EU country-week panel dataset with standardized variables."""
FILE = r"C:\Users\26540\Desktop\match_output_features\cleaned\top200_weekly_means_direct\EU_top200_weekly_means_merged_trends_STD.csv"
df = pd.read_csv(FILE)

df.columns = df.columns.str.strip()

COUNTRY_COL = "country"
DATE_COL = "date"

# Standardized Spotify features used as explanatory variables
FEATURES = [
    "danceability_z_within_country",
    "energy_z_within_country",
    "loudness_z_within_country",
    "speechiness_z_within_country",
    "acousticness_z_within_country",
    "instrumentalness_z_within_country",
    "liveness_z_within_country",
    "valence_z_within_country",
]

# Standardized COVID search intensity
COVID_COL = "COVID_z_within_country"

# convert date column to datetime format
df[DATE_COL] = pd.to_datetime(df[DATE_COL], errors="coerce")

# ensure numeric
for col in FEATURES + [COVID_COL]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Drop rows with missing values in regression variables
df = df.dropna(subset=[COUNTRY_COL, DATE_COL, COVID_COL] + FEATURES).copy()


# PER-COUNTRY REGRESSIONS

country_results = []

for country, sub in df.groupby(COUNTRY_COL, sort=False):
    # sort by date and create weekly time trend
    sub = sub.sort_values(DATE_COL).copy()
    # create trend t: linear weekly time index for each country
    sub["t"] = (sub[DATE_COL] - sub[DATE_COL].min()).dt.days / 7

    # Skip countries with too few observations
    if len(sub) < 20:
        continue

    for feature in FEATURES:

        # Dependent variable
        y = sub[COVID_COL]

        # Independent variables (feature + time trend)
        X = sm.add_constant(sub[[feature, "t"]])

        # Estimate OLS model
        model = sm.OLS(y, X).fit()

        # Store regression results
        country_results.append({
            "country": country,
            "feature": feature.replace("_z_within_country", ""),
            "beta_feature_std": model.params[feature],
            "se_feature": model.bse[feature],
            "p_feature": model.pvalues[feature],
            "beta_trend": model.params["t"],
            "se_trend": model.bse["t"],
            "p_trend": model.pvalues["t"],
            "R_squared": model.rsquared,
            "N": int(model.nobs)
        })

country_results_df = pd.DataFrame(country_results)

OUT_COUNTRY = r"C:\Users\26540\OneDrive\Study\UChicago\Winter\MACS 30122\final-project-gopredoc\Regression_output\EU_COVID_on_features_with_trend_country.csv"

country_results_df.to_csv(OUT_COUNTRY, index=False)

print("Saved country-level regressions to:", OUT_COUNTRY)



# POOLED EUROPE REGRESSIONS

df = df.sort_values(DATE_COL).copy()

# Create Europe-wide time trend
df["t_europe"] = (df[DATE_COL] - df[DATE_COL].min()).dt.days / 7

europe_results = []

for feature in FEATURES:

    y = df[COVID_COL]
    X = sm.add_constant(df[[feature, "t_europe"]])

    model = sm.OLS(y, X).fit()

    europe_results.append({
        "feature": feature.replace("_z_within_country", ""),
        "beta_feature_std": model.params[feature],
        "se_feature": model.bse[feature],
        "p_feature": model.pvalues[feature],
        "beta_trend": model.params["t_europe"],
        "se_trend": model.bse["t_europe"],
        "p_trend": model.pvalues["t_europe"],
        "R_squared": model.rsquared,
        "N": int(model.nobs)
    })

europe_results_df = pd.DataFrame(europe_results)

OUT_EUROPE = r"C:\Users\26540\OneDrive\Study\UChicago\Winter\MACS 30122\final-project-gopredoc\Regression_output\EU_COVID_on_features_with_trend_pooled.csv"

europe_results_df.to_csv(OUT_EUROPE, index=False)

print("Saved pooled Europe regressions to:", OUT_EUROPE)

print("\nPreview pooled results:")
print(europe_results_df.head())