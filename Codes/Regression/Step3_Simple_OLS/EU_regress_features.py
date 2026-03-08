"""
Run pooled Europe OLS regressions of COVID search intensity on Spotify audio features
using the standardized EU weekly panel dataset.

Nested model design:
(1) COVID = β0 + β1 danceability + ε
(2) COVID = β0 + β1 danceability + β2 energy + ε
(3) COVID = β0 + β1 danceability + β2 energy + β3 loudness + ε
...
until all features are included.

This script keeps pooled Europe regressions only and exports a nested
regression table with coefficients and p-values in parentheses.

Tingrui Zhang
AI statement: AI is used to enhance robustness of this file.
"""

import pandas as pd
import statsmodels.api as sm

# -----------------------------
# Load standardized EU panel
# -----------------------------
FILE = r"C:\Users\26540\Desktop\match_output_features\cleaned\top200_weekly_means_direct\EU_top200_weekly_means_merged_trends_STD.csv"
df = pd.read_csv(FILE)

df.columns = df.columns.str.strip()

COUNTRY_COL = "country"
DATE_COL = "date"
COVID_COL = "COVID_z_within_country"

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

# -----------------------------
# Clean data to ensure format
# -----------------------------
df[DATE_COL] = pd.to_datetime(df[DATE_COL], errors="coerce")

for col in FEATURES + [COVID_COL]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=[COUNTRY_COL, DATE_COL, COVID_COL] + FEATURES).copy()
df = df.sort_values(DATE_COL).copy()

# -----------------------------
# Run pooled nested regressions
# -----------------------------
models = []

for i in range(1, len(FEATURES) + 1):
    regressors = FEATURES[:i]

    y = df[COVID_COL]
    X = sm.add_constant(df[regressors])

    model = sm.OLS(y, X).fit()
    models.append(model)

    print("\n=============================")
    print(f"Model {i}")
    print("Regressors:", regressors)
    print(model.summary())

# -----------------------------
# Build regression table
# coefficients with p-values
# -----------------------------
table = pd.DataFrame()

variables = ["const"] + FEATURES

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

table.index = [
    "Constant",
    "danceability",
    "energy",
    "loudness",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
]

# add R2 row
table.loc["R2"] = [f"{m.rsquared:.3f}" for m in models]

# add N row
table.loc["N"] = [int(m.nobs) for m in models]

# -----------------------------
# Save output
# -----------------------------
OUT_EUROPE = r"C:\Users\26540\OneDrive\Study\UChicago\Winter\MACS 30122\final-project-gopredoc\Regression_output\EU_pooled_nested_regressions.csv"
table.to_csv(OUT_EUROPE)

print("\nNested pooled Europe regression table:")
print(table)
print("\nSaved pooled Europe regressions to:", OUT_EUROPE)