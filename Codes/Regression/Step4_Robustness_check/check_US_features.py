"""
Assess the temporal robustness of the relationship between COVID search intensity
and Spotify audio features using a lead specification.

Model specification:

    COVID_{t+L} = β0 + β1 Feature1_t + ... + βk Featurek_t + ε_t

where:
    L = number of weeks ahead (LAG_WEEKS)

Purpose of this file:
    The goal is to examine whether the contemporaneous relationship between
    music features and COVID search intensity remains informative when the
    dependent variable is shifted forward in time, and whether the estimated
    relationship is stable across subperiods.

Outputs:
    1. OLS regression summary for the earlier subsample
    2. Fit statistics for the later subsample as a temporal stability check
    3. Visualization comparing observed and model-implied values

Tingrui Zhang
AI statement: AI is used to enhance robustness of this file.
"""

import pandas as pd
import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score

FILE = r"C:\Users\26540\Desktop\match_output_features\cleaned\top200_weekly_means_direct\USA_top200_weekly_means_merged_trends_STD.csv"
df = pd.read_csv(FILE)

# enforce dtype and sort
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

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

# lead specification: 3 weeks ahead
LAG_WEEKS = 3

# construct lead of COVID search intensity
df["COVID_future"] = df[COVID].shift(-LAG_WEEKS)

# Drop rows where future value is missing
df = df.dropna(subset=["COVID_future"] + FEATURES)

# ---- split sample for temporal stability / robustness ----
early_period = df[(df["date"] >= "2020-01-01") & (df["date"] <= "2021-07-01")].copy()
later_period = df[(df["date"] > "2021-07-01") & (df["date"] <= "2022-01-01")].copy()

# =========================================================
# Estimate model on earlier subsample
# =========================================================
y_early = early_period["COVID_future"]
X_early = sm.add_constant(early_period[FEATURES])
model = sm.OLS(y_early, X_early).fit()

print(f"OLS summary using earlier subsample (lead = {LAG_WEEKS} weeks):")
print(model.summary())

# ---- fitted values in early period ----
early_period["fitted_future"] = model.predict(X_early)

# ---- implied values in later period ----
X_later = sm.add_constant(later_period[FEATURES])
later_period["implied_future"] = model.predict(X_later)

# ---- evaluate temporal stability ----
rmse = np.sqrt(mean_squared_error(later_period["COVID_future"], later_period["implied_future"]))
r2_out = r2_score(later_period["COVID_future"], later_period["implied_future"])

print("\nTemporal robustness check (later subsample):")
print("RMSE:", rmse)
print("R2 in later subsample:", r2_out)

# =========================================================
# Plot
# =========================================================
plot_df = df[(df["date"] >= "2020-01-01") &
             (df["date"] <= "2022-01-01")].copy()

plt.figure(figsize=(12, 6))

# observed lead COVID series
plt.plot(
    plot_df["date"],
    plot_df["COVID_future"],
    label=f"Observed COVID (t+{LAG_WEEKS})",
    linewidth=2
)

# fitted values in early period
plt.plot(
    early_period["date"],
    early_period["fitted_future"],
    linestyle="--",
    label="Fitted values (earlier subsample)"
)

# implied values in later period
plt.plot(
    later_period["date"],
    later_period["implied_future"],
    linestyle="--",
    label="Implied values (later subsample)"
)

# reference line between periods
plt.axvline(
    pd.Timestamp("2021-07-01"),
    color="black",
    linestyle=":",
    linewidth=2
)

plt.title(f"Temporal Robustness Check: Lead COVID Search Intensity and Music Features")
plt.xlabel("Date")
plt.ylabel("COVID search intensity (standardized)")
plt.legend()
plt.tight_layout()
plt.show()
