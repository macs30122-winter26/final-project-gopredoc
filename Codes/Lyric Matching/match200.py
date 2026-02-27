'''
Match daily top 200 songs to their lyrics in database through uri of each song; 
Produce one file for each country based on its top song list, 
    with one additional lyric column.
'''

import pandas as pd
import re
from pathlib import Path

# ---------- configure ----------
TOP200_DIR = Path("C:/Users/26540/Desktop/Spotify_daily_top200")  
LYRICS_PATHS = [
    Path("C:/Users/26540/Desktop/Lyrics_downloaded/covered_Li_with_lyrics_progress.csv"),
    Path("C:/Users/26540/Desktop/Lyrics_downloaded/covered_with_lyrics_progress_WX.csv"),
    Path("C:/Users/26540/Desktop/Lyrics_downloaded/covered_with_lyrics_progress_DC.csv"),
]
OUT_DIR = Path("C:/Users/26540/Desktop/match_output")
OUT_DIR.mkdir(parents=True, exist_ok=True)


# ---------- helpers ----------
def read_csv_robust(path: Path) -> pd.DataFrame:
    for enc in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
        try:
            return pd.read_csv(path, encoding=enc)
        except UnicodeDecodeError:
            pass
    return pd.read_csv(path, encoding="utf-8", encoding_errors="replace")


def pick_col(df: pd.DataFrame, candidates: list[str], contains_any: list[str]) -> str:
    cols = list(df.columns)
    norm = {c.lower().strip(): c for c in cols}
    for c in candidates:
        if c.lower().strip() in norm:
            return norm[c.lower().strip()]
    for c in cols:
        cl = c.lower()
        if any(s in cl for s in contains_any):
            return c
    raise KeyError(f"Could not find column. Candidates={candidates}, contains={contains_any}. Columns={cols}")


def normalize_spotify_uri(x) -> str | None:
    """
    Normalize to 'spotify:track:<id>' whenever possible.
    Handles:
      - spotify:track:<id>
      - https://open.spotify.com/track/<id>?...
      - raw <id> (22 chars)
    """
    if pd.isna(x):
        return None
    s = str(x).strip()

    m = re.search(r"open\.spotify\.com/track/([A-Za-z0-9]{22})", s)
    if m:
        return f"spotify:track:{m.group(1)}"

    m = re.search(r"spotify:track:([A-Za-z0-9]{22})", s)
    if m:
        return f"spotify:track:{m.group(1)}"

    m = re.search(r"\b([A-Za-z0-9]{22})\b", s)
    if m:
        return f"spotify:track:{m.group(1)}"

    return s.lower()  # fallback


# ---------- 1) build master lyrics table ----------
lyrics_parts = []
for p in LYRICS_PATHS:
    df = read_csv_robust(p)

    uri_col = pick_col(df, ["uri", "track_uri", "spotify_uri", "song_uri", "id", "track_id"], 
                       ["uri", "track", "id"])
    lyr_col = pick_col(df, ["lyrics", "lyric", "text"], ["lyric"])

    tmp = df[[uri_col, lyr_col]].copy()
    tmp.rename(columns={uri_col: "uri_any", lyr_col: "lyrics"}, inplace=True)
    tmp["uri_norm"] = tmp["uri_any"].map(normalize_spotify_uri)
    tmp = tmp.dropna(subset=["uri_norm"])
    lyrics_parts.append(tmp[["uri_norm", "lyrics"]])

lyrics_master = pd.concat(lyrics_parts, ignore_index=True)
# if duplicates, keep the most complete lyrics (longest)
lyrics_master["lyr_len"] = lyrics_master["lyrics"].astype(str).str.len()
lyrics_master = (lyrics_master.sort_values("lyr_len", ascending=False)
                             .drop_duplicates("uri_norm", keep="first")
                             .drop(columns="lyr_len"))
lyr_uris = set(lyrics_master["uri_norm"].dropna().unique())

print("Master lyrics unique tracks:", lyrics_master["uri_norm"].nunique())


# ---------- 2) loop over all Top-200 country files ----------
csv_files = sorted(TOP200_DIR.glob("*.csv"))
print("Top-200 files found:", len(csv_files))

summary = []
for f in csv_files:
    top = read_csv_robust(f)

    # find the column that holds the URI/ID
    top_uri_col = pick_col(top, ["uri", "track_uri", "spotify_uri", "song_uri", "id", "track_id"], ["uri", "track", "id"])
    top["uri_norm"] = top[top_uri_col].map(normalize_spotify_uri)

    merged = top.merge(lyrics_master, on="uri_norm", how="left")

    row_cov = merged["lyrics"].notna().mean()
    # EXACT diagnostic-style track match rate:
    top_uris = set(top["uri_norm"].dropna().unique())
    
    intersection = top_uris & lyr_uris

    track_cov = len(intersection) / len(top_uris) if len(top_uris) else 0.0

    out_path = OUT_DIR / f"{f.stem}_with_lyrics.csv"
    merged.to_csv(out_path, index=False)

    summary.append({
        "file": f.name,
        "rows": len(merged),
        "unique_tracks": len(top_uris),
        "row_match_rate": row_cov,
        "track_match_rate": track_cov,
        "output": str(out_path),
    })

summary_df = pd.DataFrame(summary).sort_values("track_match_rate", ascending=False)
print(summary_df.to_string(index=False))
print("Outputs saved to:", OUT_DIR)


# export summary to a csv file and an excel file
import os
num_cols = ["rows", "unique_tracks", "row_match_rate", "track_match_rate"]
summary_df[num_cols] = summary_df[num_cols].apply(pd.to_numeric, errors="coerce")

# ---------- Compute global metrics ----------
weighted_track_coverage = (
    (summary_df["unique_tracks"] * summary_df["track_match_rate"]).sum()
    / summary_df["unique_tracks"].sum()
)

weighted_row_coverage = (
    (summary_df["rows"] * summary_df["row_match_rate"]).sum()
    / summary_df["rows"].sum()
)

global_stats = pd.DataFrame({
    "metric": [
        "countries_processed",
        "total_rows",
        "total_unique_tracks",
        "average_track_match_rate",
        "median_track_match_rate",
        "weighted_track_match_rate",
        "average_row_match_rate",
        "weighted_row_match_rate"
    ],
    "value": [
        len(summary_df),
        summary_df["rows"].sum(),
        summary_df["unique_tracks"].sum(),
        summary_df["track_match_rate"].mean(),
        summary_df["track_match_rate"].median(),
        weighted_track_coverage,
        summary_df["row_match_rate"].mean(),
        weighted_row_coverage
    ]
})

# ---------- Sort country table ----------
country_table = summary_df.sort_values("track_match_rate", ascending=False)

# ---------- Save files ----------
output_dir = r"C:\Users\26540\Desktop\match_output"
csv_path = os.path.join(output_dir, "matching_summary.csv")
excel_path = os.path.join(output_dir, "matching_summary.xlsx")

country_table.to_csv(csv_path, index=False)

with pd.ExcelWriter(excel_path) as writer:
    country_table.to_excel(writer, sheet_name="Country_Level", index=False)
    global_stats.to_excel(writer, sheet_name="Global_Summary", index=False)

print("Saved:")
print(" -", csv_path)
print(" -", excel_path)