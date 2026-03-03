EU_COUNTRIES = {
    "Germany": "DE",
    "France": "FR",
    "United Kingdom": "GB",
    "Italy": "IT",
    "Spain": "ES",
    "Netherlands": "NL",
    "Belgium": "BE",
    "Sweden": "SE",
    "Norway": "NO",
    "Denmark": "DK",
    "Finland": "FI",
    "Ireland": "IE",
    "Austria": "AT",
    "Switzerland": "CH",
    "Portugal": "PT",
    "Poland": "PL",
    "Czech Republic": "CZ",
}


from pytrends.request import TrendReq
import pandas as pd
import time

pytrends = TrendReq(hl="en-US", tz=360)

query = ["COVID"]
timeframe = "2020-01-01 2024-12-31"

all_data = []

for country, code in EU_COUNTRIES.items():
    pytrends.build_payload(
        kw_list=query,
        timeframe=timeframe,
        geo=code
    )
    df = pytrends.interest_over_time()

    if not df.empty:
        df = df.reset_index()
        df["country"] = country
        all_data.append(df[["date", "COVID", "country"]])

    time.sleep(2)  # avoid Google rate limits

eu_covid = pd.concat(all_data, ignore_index=True)
eu_covid.to_csv("covid_trends_europe.csv", index=False)
