'''
Scrape weekly Google search intensity data
for words "COVID", "COVID symptoms", "COVID vaccine"
from 2020-01-01 2024-12-31
in United States.

Tingrui Zhang
AI statement: AI is used to improve robustness of this code.
'''

from pytrends.request import TrendReq
import pandas as pd

# 1) create connect object
pytrends = TrendReq(hl="en-US", tz=360) # Interface language and time

# 2) Parameters
kw_list = ["COVID", "COVID symptoms", "COVID vaccine"]
geo = "US"
timeframe = "2020-01-01 2024-12-31"   # < 5 year, weekly data from Google Trends
gprop = ""                            # web search

# 3) Weekly interest over time
pytrends.build_payload(
    kw_list=kw_list,
    cat=0, # all categories
    timeframe=timeframe,
    geo=geo,
    gprop=gprop
)

# Download data frame, remove incomplete weeks
weekly = pytrends.interest_over_time()
weekly = weekly.drop(columns=["isPartial"], errors="ignore")

# Make sure date is a column
weekly = weekly.reset_index()  

weekly.to_csv(r"C:\Users\26540\OneDrive\Study\UChicago\Winter\MACS 30122\final-project-gopredoc\Data\Google Trends\google_trends_US_weekly.csv", index=False)
print("Saved:", "google_trends_us_weekly.csv")
print(weekly.head())

