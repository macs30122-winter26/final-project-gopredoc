# Music Sentiment Responses to COVID-19 Information Shocks: Evidence from Spotify Charts and Google Search Trends

## 📖 Project Description

### Summary
This project investigates how collective emotional expression reflected in popular music responded to the COVID-19 pandemic. Specifically, we examine whether changes in public attention to COVID-19, measured through Google search intensity, are associated with shifts in musical characteristics and lyrical sentiment in chart-topping songs.

* **Topic:** The relationship between music sentiment, music attributes, and public attention to COVID-19 during the pandemic.
* **Research Question(s):**
  1. How does the lyrical sentiment of trending music respond to increases in COVID-19 related search intensity?
  2. Do music attributes and lyrical sentiment respond differently in the United States compared to Europe?
  3. Are changes in public attention to COVID-19 associated with measurable shifts in audio features such as acousticness, danceability, and energy?

---

## 📊 Data

| Data Source | Link | Collection Method | Notes |
|---|---|---|---|
| **Spotify Top Songs Charts** | [Spotify Charts](https://charts.spotify.com/) | Web scraping | Daily chart data for the US and European countries |
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
music-sentiment-covid/
│
├── Data/
│   ├── lyrics_downloaded.zip
│   ├── spotify_daily_links.docx
│   └── processed_data/
│
├── Codes/
│   ├── Google_Trend/
│   │   └── google_trends_scraper.py
│   ├── Lyrics_Scraping/
│   │   ├── azlyrics_scraper.py
│   │   └── musixmatch_api_fallback.py
│   └── Spotify_Scraping/
│       └── spotify_chart_scraper.py
│
├── Cleansing/
│   ├── data_cleaning.ipynb
│   └── merge_datasets.ipynb
│
├── EDA/
│   └── exploratory_analysis.ipynb
│
├── Textual Analysis/
│   ├── lyrics_textual_analysis.ipynb
│   └── musixmatch_fill_lyrics.ipynb
│
├── Visualization/
│   └── figures_and_plots.ipynb
│
├── docs/
│   └── ProgressReport-check2.pdf
│
└── README.md

**Folder explanation**

- `Data/` – raw and processed datasets used in the project  
- `Codes/` – scripts used for scraping Spotify charts, lyrics data, and Google Trends data  
- `Cleansing/` – notebooks used for cleaning and merging datasets  
- `EDA/` – exploratory data analysis notebooks  
- `Textual Analysis/` – natural language processing and sentiment analysis of lyrics  
- `Visualization/` – figures and visualizations used in analysis and presentations  
- `docs/` – project documentation and progress reports  

---

# Libraries

| Library | Version |
|--------|--------|
| pandas | 2.1.0 |
| numpy | 1.26.0 |
| selenium | 4.10.0 |
| undetected-chromedriver | 3.5.0 |
| beautifulsoup4 | 4.12.2 |
| requests | 2.31.0 |
| pytrends | 4.9.2 |
| nltk | 3.8.1 |
| scikit-learn | 1.3.0 |
| transformers | 4.30.0 |
| textblob | 0.17.1 |
| langdetect | 1.0.9 |

---

# Contributions

**Li You**

- Implemented Spotify chart scraping scripts
- Implemented lyrics scraping from AZLyrics
- Designed fallback strategy using Musixmatch API for missing lyrics
- Cleaned and merged sentiment datasets
- Updated repository structure and documentation

**Tingrui Zhang**

- Implemented Google Trends API data collection scripts
- Processed COVID search frequency dataset
- Conducted regression analysis comparing US and EU datasets

**Yangshunshun (Luna) Lu**

- Built repository structure
- Conducted exploratory data analysis (EDA)
- Performed lyrics textual analysis
- Created visualizations and figures for presentation

---

# AI Usage Statement

The following AI tools were used during the project.

**ChatGPT**

- Assisted with debugging Python scripts
- Helped improve code documentation and repository structure
- Provided suggestions for data cleaning and workflow organization

**Hugging Face Transformers**

- Used for sentiment classification of song lyrics using pre-trained NLP models

**TextBlob**

- Used to compute polarity scores for lyrics sentiment analysis

All outputs generated with AI tools were reviewed and verified by the project authors.

---

# Project Links

- **Slides used in the in-class presentation**  
  Included in the repository.

- **Updated final slides (full version)**  
  Included in the repository.

- **Presentation video**  
  Link provided in the repository.
