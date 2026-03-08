# Soundtracks of a Crisis: Cross-Regional Divergence in Musical Coping Mechanisms During COVID-19

## 📖 Project Description

### Summary
This project explores how public music consumption shifted during the COVID-19 pandemic, acting as a mirror for collective emotional stress. We analyze both the audio features (e.g., acousticness, danceability) and lyrical sentiment (via NLP) of chart-topping songs against COVID-19 search trends. If music sentiment reflects collective emotions, it could provide an early signal of societal stress or public attention.
/>


* **Topic:** The relationship between music sentiment, music attributes, and public attention to COVID-19 during the pandemic.
  
* **Research Question:**
   How does the correlation between music attributes (melody and lyrics) and COVID-19 pandemic trends differ between the US and European markets?



---

## 📊 Data

| Data Source | Link | Collection Method | Notes |
|---|---|---|---|
| **Spotify Top Songs Charts** | [Spotify Charts]([https://charts.spotify.com/](https://charts.spotify.com/charts/view/regional-us-daily/2026-02-26)) | Web scraping | Daily chart data for the US and European countries |
| **Lyrics Database (AZLyrics)** | [AZLyrics](https://www.azlyrics.com/) | Web scraping | Primary source for song lyrics |
| **Musixmatch Lyrics API** | [Musixmatch API](https://docs.musixmatch.com/lyrics-api/) | API | Used as a fallback to fill missing lyrics |
| **Spotify Music Attributes** | [Anna's Archive](https://annas-archive.pm/blog/backing-up-spotify.html) | Download | Provides audio features (acousticness, danceability, etc.) |
| **Google Trends** | [Google Trends](https://trends.google.com/trends/) | API | COVID-related search intensity collected via `pytrends` |

> **Additional Notes on Data Collection:**
> * Some songs did not have available lyrics in AZLyrics.
> * Musixmatch API was used to fill missing lyrics where possible.
> * API rate limits required a fallback scraping strategy.

---

## 🗂️ Repository Structure


```text
final-project-gopredoc/
│
├── Codes/
│   ├── Cleansing/
│   │   └── data_cleansing_EDATextAnalysis.ipynb
│   ├── EDA/
│   │   └── EDA.ipynb
│   ├── Regression/
│   │   ├── Step1_Top200-Lyric Matching/
│   │   ├── Step2_Data_processing_for_reg/
│   │   ├── Step3_Regression/
│   │   └── Step4_Robustness_check/
│   ├── Scraping/
│   │   ├── Google Trends/
│   │   │   ├── scrape_search_density_EU.py
│   │   │   └── scrape_search_density_US.py
│   │   ├── Lyrics Scraping/
│   │   │   ├── Lyric_Downloader_for sharing.ipynb
│   │   │   └── musixmatch_fill_lyrics.ipynb
│   │   └── Spotify Scraping/
│   │       ├── README.md
│   │       ├── config.py
│   │       ├── run_batch.py
│   │       └── scraper.py
│   └── Textual Analysis/
│       └── lyrics_textanalysis.ipynb
│
├── Data/
│   ├── Google Trends/
│   │   ├── covid_trends_europe.csv
│   │   └── google_trends_us_weekly.csv
│   ├── Dropbox_link_spotify.docx
│   └── top200_lyric_features_link.txt
│   └── Spotify_features_link.txt
│
├── EDAViz_result/
│   └── EDA_Viz/
│       ├── All_Countries/
│       ├── Europe/
│       ├── USA/
│       └── descriptive_stats/
│
├── Regression_output/
│   ├── COVID_robustness_features.png
│   ├── COVID_robustness_features_sentiment.png
│   ├── EU_COVID_on_features_with_trend_country.csv
│   ├── EU_COVID_on_features_with_trend_pooled.csv
│   ├── EU_feature_regressions_with_trend.csv
│   ├── EU_pooled_feature_regressions_with_trend.csv
│   ├── EU_pooled_nested_regressions.csv
│   ├── EU_sentiment_progressive.csv
│   ├── USA_COVID_feature_regressions.csv
│   ├── USA_feature_regressions_with_trend.csv
│   ├── USA_nested_regressions.csv
│   ├── USA_sentiment_progressive.csv
│   ├── sentiment_regression_results_with_melody_valence.csv
│   └── sentiment_regression_results_with_trend.csv
│
├── GoPredoc_final.pptx
├── GoPredoc_original.pptx
├── ProgressReport-check2.pdf
└── README.md
```
### 📂 Folder Explanation

* **`Codes/`** – The main directory containing all executable scripts and Jupyter Notebooks.
  * **`Cleansing/`** – Notebooks used for merging and cleaning datasets.
  * **`EDA/`** – Exploratory data analysis notebooks.
  * **`Regression/`** – Step-by-step regression modeling, from data processing to robustness checks.
  * **`Scraping/`** – Data collection scripts for Google Trends, Lyrics, and Spotify charts.
  * **`Textual Analysis/`** – Natural language processing and sentiment analysis of the extracted lyrics (`lyrics_textanalysis.ipynb`).
* **`Data/`** – Contains raw/processed data links (Dropbox) and Google Trends CSV datasets.
* **`EDAViz_result/`** – Output folders containing figures, plots, and descriptive statistics separated by region (US, Europe, All Countries).
* **`Regression_output/`** – Contains all resulting CSV tables and robustness check plots from the sentiment regression models.
* **`Root Files`** – Project presentations (`.pptx`), progress reports (`.pdf`), and the project documentation (`README.md`).

---

## 🛠️ Libraries

| Library | Version |
|---|---|
| **`pandas`** | 2.1.0 |
| **`numpy`** | 1.26.0 |
| **`selenium`** | 4.10.0 |
| **`undetected-chromedriver`** | 3.5.0 |
| **`beautifulsoup4`** | 4.12.2 |
| **`requests`** | 2.31.0 |
| **`pytrends`** | 4.9.2 |
| **`nltk`** | 3.8.1 |
| **`scikit-learn`** | 1.3.0 |
| **`transformers`** | 4.30.0 |
| **`textblob`** | 0.17.1 |
| **`langdetect`** | 1.0.9 |

---

## 👥 Contributions

* **Li You**
  * Implemented Spotify chart scraping scripts.
  * Implemented lyrics scraping from AZLyrics.
  * Designed fallback strategy using Musixmatch API for missing lyrics.
  * Cleaned and merged sentiment datasets.
  * Updated repository structure and documentation.

* **Tingrui Zhang**
  * Implemented Google Trends API data collection scripts.
  * Processed COVID search frequency dataset.
  * Conducted regression analysis comparing US and EU datasets.

* **Yangshunshun (Luna) Lu**
  * Built repository structure.
  * Conducted exploratory data analysis (EDA).
  * Performed lyrics textual analysis.
  * Created visualizations and figures for presentation.

---

## 🤖 AI Usage Statement

The following AI tools were used during the project:

* **ChatGPT:** Assisted with debugging Python scripts, helped improve code documentation and repository structure, and provided suggestions for data cleaning and workflow organization.
* **Hugging Face Transformers:** Used for sentiment classification of song lyrics using pre-trained NLP models.
* **TextBlob:** Used to compute polarity scores for lyrics sentiment analysis.

> *All outputs generated with AI tools were reviewed and verified by the project authors.*

---

## 🔗 Project Links

* **Slides used in the in-class presentation:** Included in the repository.
* **Updated final slides (full version):** Included in the repository.
* **Presentation video:** Link provided in the repository.
