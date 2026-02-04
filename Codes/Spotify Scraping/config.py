"""
Spotify Charts crawler configuration
"""

# Global chart
GLOBAL = 'global'

# All country/region codes (around 70)
COUNTRIES = [
    # North America
    'us', 'ca', 'mx',
    # South America
    'br', 'ar', 'cl', 'co', 'pe', 'ec', 'uy', 'py', 'bo', 've', 'cr', 'pa', 'do', 'gt', 'hn', 'sv', 'ni',
    # Europe
    'gb', 'de', 'fr', 'es', 'it', 'nl', 'be', 'at', 'ch', 'se', 'no', 'dk', 'fi', 'ie', 'pt', 'pl', 'cz', 'sk', 'hu', 'ro', 'bg', 'gr', 'tr', 'ua', 'ru', 'lt', 'lv', 'ee', 'is', 'lu',
    # Asia-Pacific
    'jp', 'kr', 'au', 'nz', 'in', 'id', 'my', 'ph', 'sg', 'th', 'vn', 'tw', 'hk',
    # Middle East / Africa
    'il', 'ae', 'sa', 'eg', 'za', 'ma', 'ng',
]

# All regions (including global)
ALL_REGIONS = [GLOBAL] + COUNTRIES

# Date range
START_YEAR = 2017
START_MONTH = 1
END_YEAR = 2025
END_MONTH = 12

# Output directory
OUTPUT_DIR = 'spotify_data'
PROGRESS_FILE = 'progress.json'
