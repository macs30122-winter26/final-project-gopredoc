import pandas as pd
import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score

FILE = r"C:\Users\26540\Desktop\match_output_features\cleaned\top200_weekly_means_direct\USA_top200_weekly_means_merged_trends_STD.csv"
df = pd.read_csv(FILE)

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

# ==========================================
# CREATE FORWARD LAG: predict COVID_{t+4}
# ==========================================
LAG_WEEKS = 3

df["COVID_future"] = df[COVID].shift(-LAG_WEEKS)

# Drop rows where future value is missing
df = df.dropna(subset=["COVID_future"] + FEATURES)

# ---- split sample ----
train = df[(df["date"] >= "2020-01-01") & (df["date"] <= "2021-7-1")].copy()
test  = df[(df["date"] >  "2021-7-1") & (df["date"] <= "2022-1-1")].copy()

# ==========================================
# FIT: COVID_{t+4} ~ features_t
# ==========================================
y_train = train["COVID_future"]
X_train = sm.add_constant(train[FEATURES])
model = sm.OLS(y_train, X_train).fit()

print(f"Training summary (Predict COVID +{LAG_WEEKS} weeks):")
print(model.summary())

# ---- fitted (train) ----
train["fitted_future"] = model.predict(X_train)

# ---- forecast (test) ----
X_test = sm.add_constant(test[FEATURES])
test["forecast_future"] = model.predict(X_test)

# ---- evaluate ----
rmse = np.sqrt(mean_squared_error(test["COVID_future"], test["forecast_future"]))
r2_out = r2_score(test["COVID_future"], test["forecast_future"])

print("\nOut-of-sample performance (lag model):")
print("RMSE:", rmse)
print("Out-of-sample R2:", r2_out)

# ==========================================
# PLOT
# ==========================================
plot_df = df[(df["date"] >= "2020-01-01") &
             (df["date"] <= "2022-1-1")].copy()

plt.figure(figsize=(12,6))

# Actual future COVID
plt.plot(plot_df["date"], plot_df["COVID_future"],
         label=f"Actual COVID (t+{LAG_WEEKS})", linewidth=2)

# Fitted train
plt.plot(train["date"], train["fitted_future"],
         linestyle="--", label="Fitted (Train 2020)")

# Forecast test
plt.plot(test["date"], test["forecast_future"],
         linestyle="--", label="Forecast (Test 2021)")

plt.axvline(pd.Timestamp("2021-7-1"),
            color="black", linestyle=":", linewidth=2)

plt.title(f"Predicting COVID_z {LAG_WEEKS} Weeks Ahead from Music Features")
plt.xlabel("Date")
plt.ylabel("COVID search intensity (standardized)")
plt.legend()
plt.tight_layout()
plt.show()