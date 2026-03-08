"""
Assess the temporal robustness of the relationship between COVID search intensity,
Spotify audio features, and lyric sentiment using a lead specification and the
restricted database provided by Luna.

Model specification:

    COVID_{t+L} = β0 + β1 Feature1_t + ... + βk Featurek_t + β_sent Sentiment_t + ε_t

where:
    L = number of weeks ahead (LAG_WEEKS)

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

FILE = r"C:\Users\26540\Desktop\Lyrics_downloaded\lyricsFeatures_weekly_aggregated.csv"
df = pd.read_csv(FILE)

df.columns = df.columns.str.strip()
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# restrict to USA only
df = df[df["country"] == "USA"].copy()
df = df.sort_values("date")

COVID = "COVID_z"

# audio features plus lyric sentiment
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

# -----------------------------
# Lead specification
# -----------------------------
LAG_WEEKS = 3
df["COVID_future"] = df[COVID].shift(-LAG_WEEKS)
df = df.dropna(subset=["COVID_future"] + FEATURES)

# -----------------------------
# Split sample for temporal robustness
# -----------------------------
early_period = df[(df["date"] >= "2020-01-01") & (df["date"] <= "2021-07-01")].copy()
later_period = df[(df["date"] > "2021-07-01") & (df["date"] <= "2022-01-01")].copy()

# -----------------------------
# Estimate model on earlier subsample
# -----------------------------
y_early = early_period["COVID_future"]
X_early = sm.add_constant(early_period[FEATURES])
model = sm.OLS(y_early, X_early).fit()

print(f"\nOLS summary using earlier subsample (USA only, lead = {LAG_WEEKS} weeks):")
print(model.summary())

# -----------------------------
# Fitted values in earlier subsample
# -----------------------------
early_period["fitted_future"] = model.predict(X_early)

# -----------------------------
# Implied values in later subsample
# -----------------------------
X_later = sm.add_constant(later_period[FEATURES])
later_period["implied_future"] = model.predict(X_later)

# -----------------------------
# Evaluate temporal robustness
# -----------------------------
rmse = np.sqrt(mean_squared_error(later_period["COVID_future"], later_period["implied_future"]))
r2_out = r2_score(later_period["COVID_future"], later_period["implied_future"])

print("\nTemporal robustness check (later subsample):")
print("RMSE:", rmse)
print("R2 in later subsample:", r2_out)

# -----------------------------
# Plot
# -----------------------------
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

# fitted values in earlier period
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

# vertical line separating subsamples
plt.axvline(
    pd.Timestamp("2021-07-01"),
    color="black",
    linestyle=":",
    linewidth=2
)

plt.title("USA: Temporal Robustness Check with Audio Features and Lyric Sentiment")
plt.xlabel("Date")
plt.ylabel("COVID search intensity (standardized)")
plt.legend()
plt.tight_layout()
plt.show()