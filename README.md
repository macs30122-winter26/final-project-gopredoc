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
