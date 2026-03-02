from pytrends.request import TrendReq
import pandas as pd

# 1) Connect
pytrends = TrendReq(hl="en-US", tz=360)

# 2) Parameters
kw_list = ["COVID", "COVID symptoms", "COVID vaccine"]
geo = "US"
timeframe = "2020-01-01 2024-12-31"   # multi-year => weekly data from Google Trends
gprop = ""                            # web search; or "news", "youtube", etc.

# 3) Weekly interest over time
pytrends.build_payload(
    kw_list=kw_list,
    cat=0,
    timeframe=timeframe,
    geo=geo,
    gprop=gprop
)

weekly = pytrends.interest_over_time()
weekly = weekly.drop(columns=["isPartial"], errors="ignore")

# Make sure date is a column (useful for merges)
weekly = weekly.reset_index()  # columns: date, <kw1>, <kw2>, ...

weekly.to_csv("google_trends_us_weekly.csv", index=False)
print("Saved:", "google_trends_us_weekly.csv")
print(weekly.head())

