"""
Author: Li You

Description:
This script crawls Spotify Daily Top 200 chart data month by month, including both
chart rankings and selected track metadata from the Spotify Charts website.

AI Disclosure:
AI tools (e.g., ChatGPT) were used for debugging assistance, code organization,
and documentation support. All final implementation decisions, testing, and
verification were independently completed by the author.

Usage:
    python scraper.py <country> <year> <month>

Example:
    python scraper.py global 2024 1
"""

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import os
import sys
import time
import json
import re
from datetime import datetime, timedelta
from calendar import monthrange
from config import OUTPUT_DIR, ALL_REGIONS


def get_month_dates(year, month):
    """
    Generate all valid dates in the specified month that are earlier than today.

    Inputs:
        year (int): Target year.
        month (int): Target month.

    Outputs:
        list[str]: A list of date strings in 'YYYY-MM-DD' format for the specified month.
    """
    dates = []
    days_in_month = monthrange(year, month)[1]
    today = datetime.now()

    for day in range(1, days_in_month + 1):
        d = datetime(year, month, day)
        if d < today:
            dates.append(d.strftime('%Y-%m-%d'))
    return dates


def load_progress(country, year, month):
    """
    Load previously saved crawling progress for a given country-month task.

    Inputs:
        country (str): Region code being crawled.
        year (int): Target year.
        month (int): Target month.

    Outputs:
        dict: A progress dictionary containing completed dates. If no progress file
        exists, returns a default dictionary with an empty completed list.
    """
    progress_file = os.path.join(
        OUTPUT_DIR, f'progress_{country}_{year}_{month:02d}.json'
    )
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            return json.load(f)
    return {'completed': []}


def save_progress(country, year, month, progress):
    """
    Save crawling progress to a JSON file for resume-safe execution.

    Inputs:
        country (str): Region code being crawled.
        year (int): Target year.
        month (int): Target month.
        progress (dict): Progress dictionary to save.

    Outputs:
        None
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    progress_file = os.path.join(
        OUTPUT_DIR, f'progress_{country}_{year}_{month:02d}.json'
    )
    with open(progress_file, 'w') as f:
        json.dump(progress, f)


def scrape_page(driver, country, date):
    """
    Scrape chart entries from a single Spotify Charts page for one country-date pair.

    Inputs:
        driver: Selenium WebDriver instance.
        country (str): Region code being crawled.
        date (str): Target date in 'YYYY-MM-DD' format.

    Outputs:
        list[dict]: A list of parsed chart entries for the specified page.
        Returns an empty list if scraping fails after retries.
    """
    url = f'https://charts.spotify.com/charts/view/regional-{country}-daily/{date}'

    # Retry page loading a few times in case of transient failures
    for attempt in range(3):
        try:
            driver.get(url)
            time.sleep(3)

            # Wait until chart rows are visible in the table
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'tbody tr'))
            )
            time.sleep(2)

            entries = []
            rows = driver.find_elements(By.CSS_SELECTOR, 'tbody tr')
            row_count = len(rows)

            # Parse each row one by one
            for i in range(row_count):
                for retry in range(3):
                    try:
                        rows = driver.find_elements(By.CSS_SELECTOR, 'tbody tr')
                        if i >= len(rows):
                            break
                        row = rows[i]

                        entry = parse_row_with_detail(driver, row, country, date)
                        if entry and entry.get('rank'):
                            entries.append(entry)
                        break
                    except Exception:
                        if retry < 2:
                            time.sleep(0.5)
                        continue

            if entries:
                return entries

        except Exception:
            if attempt < 2:
                time.sleep(3)
                continue
            return []

    return []


def parse_row_with_detail(driver, row, country, date):
    """
    Parse one chart row and extract both basic fields and expandable detail metadata.

    Inputs:
        driver: Selenium WebDriver instance.
        row: Selenium WebElement corresponding to one chart table row.
        country (str): Region code being crawled.
        date (str): Target date in 'YYYY-MM-DD' format.

    Outputs:
        dict or None: A dictionary containing parsed fields for the row if successful;
        otherwise returns None.
    """
    entry = {
        'rank': '', 'uri': '', 'artist_names': '', 'track_name': '',
        'source': '', 'peak_rank': '', 'previous_rank': '', 'weeks_on_chart': '',
        'streams': '', 'release date': '', 'first entry date': '',
        'producers': '', 'song writers': '', 'date': date, 'country': country,
    }

    try:
        cells = row.find_elements(By.TAG_NAME, 'td')
        if len(cells) < 7:
            return None

        # Extract rank from the ranking cell
        rank_text = cells[1].text.strip().split('\n')[0]
        rank_match = re.search(r'^(\d+)', rank_text)
        if rank_match:
            entry['rank'] = rank_match.group(1)
        else:
            return None

        # Extract track URI, track name, and artist names from hyperlinks
        track_cell = cells[2]
        links = track_cell.find_elements(By.TAG_NAME, 'a')

        artist_names = []
        for link in links:
            href = link.get_attribute('href') or ''
            text = link.text.strip()
            if '/track/' in href and text:
                track_id = href.split('/track/')[-1].split('?')[0]
                entry['uri'] = f'spotify:track:{track_id}'
                entry['track_name'] = text
            elif '/artist/' in href and text:
                artist_names.append(text)

        entry['artist_names'] = ', '.join(artist_names)
        entry['peak_rank'] = cells[3].text.strip()
        entry['previous_rank'] = cells[4].text.strip()
        entry['weeks_on_chart'] = cells[5].text.strip()
        entry['streams'] = cells[6].text.strip().replace(',', '')

        # Click the expandable "More" button to retrieve additional metadata
        try:
            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", row
            )
            time.sleep(0.3)

            more_btn = row.find_element(By.CSS_SELECTOR, 'button.view-more-button')
            driver.execute_script("arguments[0].click();", more_btn)
            time.sleep(1)

            detail_text = ''
            detail_rows = driver.find_elements(By.CSS_SELECTOR, 'tbody tr')
            for dr in detail_rows:
                text = dr.text
                if 'Release Date' in text or 'Producer' in text or 'Songwriter' in text:
                    detail_text = text
                    break

            # Fallback: use the full table body text if a targeted detail block is not found
            if not detail_text:
                detail_text = driver.find_element(By.CSS_SELECTOR, 'tbody').text

            # Extract selected detail fields using regular expressions
            m = re.search(
                r'Release Date\s*\n?\s*([A-Za-z]+\s+\d{1,2},?\s+\d{4})',
                detail_text
            )
            if m:
                entry['release date'] = m.group(1)

            m = re.search(
                r'First entry date\s*\n?\s*([A-Za-z]+\s+\d{1,2},?\s+\d{4})',
                detail_text
            )
            if m:
                entry['first entry date'] = m.group(1)

            m = re.search(
                r'Source\s*\n?\s*([A-Za-z0-9\s\-/]+?)(?:\s*Share|\s*\n|$)',
                detail_text
            )
            if m:
                entry['source'] = m.group(1).strip()

            m = re.search(
                r'Producers?\s*\n([\s\S]+?)(?=Songwriters?|Source|Share|$)',
                detail_text
            )
            if m:
                entry['producers'] = re.sub(
                    r'\s*\n\s*', ', ', m.group(1).strip()
                ).strip(', ')

            m = re.search(
                r'Songwriters?\s*\n([\s\S]+?)(?=Source|Share|$)',
                detail_text
            )
            if m:
                entry['song writers'] = re.sub(
                    r'\s*\n\s*', ', ', m.group(1).strip()
                ).strip(', ')

            # Try to close the detail view after extraction
            try:
                more_btn = row.find_element(By.CSS_SELECTOR, 'button.view-more-button')
                driver.execute_script("arguments[0].click();", more_btn)
                time.sleep(0.3)
            except Exception:
                pass

        except Exception:
            pass

        return entry

    except Exception:
        return None


def save_data(country, year, month, data):
    """
    Save scraped chart data to a monthly CSV file.

    Inputs:
        country (str): Region code being crawled.
        year (int): Target year.
        month (int): Target month.
        data (list[dict]): Parsed chart entries to write.

    Outputs:
        None
    """
    if not data:
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = os.path.join(
        OUTPUT_DIR, f'regional-{country}-daily-{year}-{month:02d}.csv'
    )

    fieldnames = [
        'rank', 'uri', 'artist_names', 'track_name', 'source',
        'peak_rank', 'previous_rank', 'weeks_on_chart', 'streams',
        'release date', 'first entry date', 'producers', 'song writers',
        'date', 'country'
    ]

    # Append to an existing file if present; otherwise write a new file with header
    file_exists = os.path.exists(filename)
    with open(filename, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerows(data)


def main():
    """
    Run the monthly Spotify Charts crawling workflow from command-line arguments.

    Inputs:
        None directly. The function reads command-line arguments in the form:
        python scraper.py <country> <year> <month>

    Outputs:
        None
    """
    if len(sys.argv) != 4:
        print("Usage: python scraper.py <country> <year> <month>")
        print("Example: python scraper.py global 2024 1")
        print(f"\nAvailable regions: {', '.join(ALL_REGIONS[:20])}...")
        return

    country = sys.argv[1].lower()
    year = int(sys.argv[2])
    month = int(sys.argv[3])

    # Validate the region code before launching the crawler
    if country not in ALL_REGIONS:
        print(f"Error: unknown region '{country}'")
        print(f"Available: global, {', '.join(ALL_REGIONS[1:20])}...")
        return

    print(f"Crawling: {country.upper()} {year}-{month:02d}")

    dates = get_month_dates(year, month)
    if not dates:
        print("No dates available for crawling")
        return

    # Load progress so the script can resume incomplete monthly tasks
    progress = load_progress(country, year, month)
    completed = set(progress['completed'])
    pending = [d for d in dates if d not in completed]

    if not pending:
        print("This month has already been fully completed!")
        return

    print(f"Pending days: {len(pending)}")
    print("\nLaunching browser...")

    user_data_dir = os.path.join(os.getcwd(), 'chrome_profile')
    os.makedirs(user_data_dir, exist_ok=True)

    options = uc.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument(f'--user-data-dir={user_data_dir}')

    driver = uc.Chrome(
        options=options,
        use_subprocess=True,
        version_main=144
    )

    try:
        driver.get(
            f"https://charts.spotify.com/charts/view/regional-{country}-daily/{dates[0]}"
        )
        time.sleep(5)

        # Reuse the browser profile if already logged in; otherwise wait for manual login
        try:
            driver.find_element(By.CSS_SELECTOR, 'tbody tr')
            print("Already logged in. Starting crawl...")
        except Exception:
            print("\nPlease log in to Spotify. Press Enter after login...")
            input()

        data = []
        start_time = time.time()

        # Process each pending date and periodically save intermediate results
        for i, date in enumerate(pending):
            print(f"\r[{i + 1}/{len(pending)}] {date}", end="", flush=True)

            entries = scrape_page(driver, country, date)

            if entries:
                data.extend(entries)
                progress['completed'].append(date)

            if (i + 1) % 5 == 0:
                save_data(country, year, month, data)
                save_progress(country, year, month, progress)
                elapsed = time.time() - start_time
                avg = elapsed / (i + 1)
                remaining = avg * (len(pending) - i - 1)
                print(f" | ~{remaining / 60:.0f} minutes remaining")
                data = []

        # Save any final unsaved results after the loop ends
        if data:
            save_data(country, year, month, data)
            save_progress(country, year, month, progress)

        print(
            f"\n\nDone! File: spotify_data/regional-{country}-daily-{year}-{month:02d}.csv"
        )

    finally:
        driver.quit()


if __name__ == '__main__':
    main()