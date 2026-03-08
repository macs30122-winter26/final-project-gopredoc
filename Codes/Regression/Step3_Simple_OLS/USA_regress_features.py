"""
Sequential regression models for COVID search intensity.

Specification expansion:

(1) COVID = β0 + β1 danceability
(2) COVID = β0 + β1 danceability + β2 energy
(3) COVID = β0 + β1 danceability + β2 energy + β3 loudness
...
until all features are included.

This produces a nested regression table similar to standard
economics empirical papers.

Tingrui Zhang
AI statement: AI is used to enhance robustness of this file.
"""

import pandas as pd
import statsmodels.api as sm

# -----------------------------
# Load data
# -----------------------------
FILE = r"C:/Users/26540/Desktop/match_output_features/cleaned/top200_weekly_means_direct/USA_top200_weekly_means_merged_trends_STD.csv"
df = pd.read_csv(FILE)

df.columns = df.columns.str.strip()

COVID = "COVID_z"

FEATURES = [
    "danceability_z",
    "energy_z",
    "loudness_z",
    "speechiness_z",
    "acousticness_z",
    "instrumentalness_z",
    "liveness_z",
    "valence_z"
]

needed = [COVID] + FEATURES
df = df.dropna(subset=needed)

# -----------------------------
# Run sequential regressions
# -----------------------------
models = []

# for each feature, build baseline and progessive model
for i in range(1, len(FEATURES) + 1):

    # include i regressors in this iteration
    regressors = FEATURES[:i]

    y = df[COVID]
    X = sm.add_constant(df[regressors])

    model = sm.OLS(y, X).fit()

    models.append(model)

    print("\n=============================")
    print(f"Model {i}")
    print("Regressors:", regressors)
    print(model.summary())

# -----------------------------
# Build regression table
# -----------------------------
table = pd.DataFrame()

variables = ["const"] + FEATURES

for idx, model in enumerate(models):

    col = []

    for var in variables:

        if var in model.params:

            # document coefficients and pvalues
            coef = model.params[var]
            pval = model.pvalues[var]

            entry = f"{coef:.3f}\n({pval:.2f})"

        else:
            entry = ""

        col.append(entry)

    table[f"({idx+1})"] = col

# rename feature column
table.index = ["Constant"] + [f.replace("_z","") for f in FEATURES]

# add R2 row
r2 = [f"{m.rsquared:.3f}" for m in models]
table.loc["R2"] = r2

# -----------------------------
# Save table
# -----------------------------
OUT = r"C:\Users\26540\OneDrive\Study\UChicago\Winter\MACS 30122\final-project-gopredoc\Regression_output\USA_nested_regressions.csv"

table.to_csv(OUT)

print("\nRegression Table:")
print(table)

print("\nSaved to:", OUT)