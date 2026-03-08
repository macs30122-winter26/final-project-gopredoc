# Spotify Daily Top 200 Crawler


- **Author**: Li You 
- **Description**: This code collects and processes Spotify Daily Top 200 chart data, supporting automated crawling, batching, and resume-safe execution.  
- **AI Use Disclosure**: Portions of the documentation were developed with assistance from AI tools (ChatGPT) for debugging and clarity. All final implementation decisions and verification were performed by the author.



## Overview

This project crawls **Spotify Daily Top 200** chart data using **Selenium** to simulate browser access.

---

## Data Coverage

- **Date range**: 2017-01-01 to 2025-12-28  
  *(Two-year period used as an example)*

- **Countries**: global, us, gb, de, fr, jp, kr, br, mx, au etc. (73 countries in total)
  *(Temporarily limited to 10 major countries for demonstration)*

- **Chart type**: Daily Top 200

---

## Output Format

Data are saved as **CSV files** with the following fields:

- rank, uri, artist_names, track_name, source  
- peak_rank, previous_rank, weeks_on_chart, streams  
- release_date, first_entry_date, producers, song_writers  
- date, country

---

## Installation

```bash
pip install undetected-chromedriver selenium

---

## File Structure

| File | Description |
|------|-------------|
| scraper.py | Main crawler script |
| config.py | Configuration file (country list and date range) |
| run_batch.py | Batch command generator |

---


