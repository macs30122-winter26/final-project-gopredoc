import pytrends

from pytrends.request import TrendReq
import pandas as pd

pytrends = TrendReq(hl="en-US", tz=360)  # tz is minutes offset from UTC (e.g., 360 = UTC-6)

kw_list = ["COVID", "COVID symptoms", "COVID vaccine"]  # pick your terms
pytrends.build_payload(
    kw_list=kw_list,
    cat=0,
    timeframe="2020-01-01 2025-12-31",  # or "today 5-y", "today 12-m", etc.
    geo="US",                           # "" for worldwide; e.g. "GB", "CN" (often limited), "US-IL"
    gprop=""                            # ""=web search; "news", "images", "youtube", "froogle"
)

df = pytrends.interest_over_time()
df = df.drop(columns=["isPartial"], errors="ignore")
print(df.head())

df.to_csv("google_trends_covid_us.csv")

region = pytrends.interest_by_region(resolution="REGION", inc_low_vol=True, inc_geo_code=False)
region.to_csv("covid_trends_by_region.csv")