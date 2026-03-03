import pandas as pd
import statsmodels.api as sm

# ---- load standardized EU panel ----
FILE = r"C:\Users\26540\Desktop\match_output_features\cleaned\top200_weekly_means_direct\EU_top200_weekly_means_merged_trends_STD.csv"
df = pd.read_csv(FILE)

df.columns = df.columns.str.strip()

COUNTRY_COL = "country"
DATE_COL = "date"

FEATURES = [
    "danceability_z_within_country", "energy_z_within_country", "loudness_z_within_country",
    "speechiness_z_within_country", "acousticness_z_within_country",
    "instrumentalness_z_within_country", "liveness_z_within_country", "valence_z_within_country"
]

COVID_COL = "COVID_z_within_country"

# ---- parse date ----
df[DATE_COL] = pd.to_datetime(df[DATE_COL], errors="coerce")

# ---- ensure numeric ----
for col in FEATURES + [COVID_COL]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=[COUNTRY_COL, DATE_COL, COVID_COL] + FEATURES).copy()

# ============================================================
# 1️⃣ PER-COUNTRY REGRESSIONS
# ============================================================

country_results = []

for country, sub in df.groupby(COUNTRY_COL, sort=False):
    sub = sub.sort_values(DATE_COL).copy()
    sub["t"] = (sub[DATE_COL] - sub[DATE_COL].min()).dt.days / 7

    if len(sub) < 20:
        continue

    for feature in FEATURES:
        y = sub[feature]
        X = sm.add_constant(sub[[COVID_COL, "t"]])
        model = sm.OLS(y, X).fit()

        country_results.append({
            "country": country,
            "feature": feature.replace("_z_within_country", ""),
            "beta_COVID_std": model.params[COVID_COL],
            "se_COVID": model.bse[COVID_COL],
            "p_COVID": model.pvalues[COVID_COL],
            "beta_trend": model.params["t"],
            "se_trend": model.bse["t"],
            "p_trend": model.pvalues["t"],
            "R_squared": model.rsquared,
            "N": int(model.nobs)
        })

country_results_df = pd.DataFrame(country_results)

OUT_COUNTRY = r"C:\Users\26540\OneDrive\Study\UChicago\Winter\MACS 30122\final-project-gopredoc\Regression_output\EU_feature_regressions_with_trend.csv"
country_results_df.to_csv(OUT_COUNTRY, index=False)

print("Saved country-level regressions to:", OUT_COUNTRY)


# ============================================================
# 2️⃣ POOLED EUROPE REGRESSIONS
# ============================================================

# Create pooled Europe time trend
df = df.sort_values(DATE_COL).copy()
df["t_europe"] = (df[DATE_COL] - df[DATE_COL].min()).dt.days / 7

europe_results = []

for feature in FEATURES:
    y = df[feature]
    X = sm.add_constant(df[[COVID_COL, "t_europe"]])
    model = sm.OLS(y, X).fit()

    europe_results.append({
        "feature": feature.replace("_z_within_country", ""),
        "beta_COVID_std": model.params[COVID_COL],
        "se_COVID": model.bse[COVID_COL],
        "p_COVID": model.pvalues[COVID_COL],
        "beta_trend": model.params["t_europe"],
        "se_trend": model.bse["t_europe"],
        "p_trend": model.pvalues["t_europe"],
        "R_squared": model.rsquared,
        "N": int(model.nobs)
    })

europe_results_df = pd.DataFrame(europe_results)

OUT_EUROPE = r"C:\Users\26540\OneDrive\Study\UChicago\Winter\MACS 30122\final-project-gopredoc\Regression_output\EU_pooled_feature_regressions_with_trend.csv"
europe_results_df.to_csv(OUT_EUROPE, index=False)

print("Saved pooled Europe regressions to:", OUT_EUROPE)

print("\nPreview pooled results:")
print(europe_results_df.head())