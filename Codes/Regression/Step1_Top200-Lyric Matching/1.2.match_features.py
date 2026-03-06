'''
Used ONLY after merging with lyrics. 
Merge top200 songs (containing lyrics now) with the feature database on track URI.
Creates a list of files, each with top200 songs, lyrics, and features for one country.
Tingrui Zhang

AI statement: AI is used to enhance robustness of this file.
'''

import pandas as pd
import re
from pathlib import Path

# ---------------- config ----------------
# these files are local; please download file via link to run this code.
MATCHED_DIR = Path(r"C:\Users\26540\Desktop\match_output")
FEATURES_PATH = Path(r"C:\Users\26540\Desktop\spotify music features (240k) covered.csv")
OUT_DIR = Path(r"C:\Users\26540\Desktop\match_output_features")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# features to be matched
FEATURE_COLS = [
    "duration_ms", "time_signature", "tempo", "key", "mode",
    "danceability", "energy", "loudness", "speechiness", "acousticness",
    "instrumentalness", "liveness", "valence"
]

# ---------------- helpers ----------------
def read_csv_robust(path: Path) -> pd.DataFrame:
    '''same helper as match_lyrics.py'''
    for enc in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
        try:
            return pd.read_csv(path, encoding=enc)
        except UnicodeDecodeError:
            pass
    return pd.read_csv(path, encoding="utf-8", encoding_errors="replace")

def normalize_spotify_uri(x) -> str | None:
    '''same helper as match_lyrics.py'''
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

    # fallback: keep a normalized string (can still match if both sides have same format)
    return s.lower()

def find_uri_col(df: pd.DataFrame) -> str:
    '''same helper as match_lyrics.py'''
    candidates = ["uri_norm", "uri", "track_uri", "spotify_uri", "song_uri"]
    lower_map = {c.lower(): c for c in df.columns}
    for c in candidates:
        if c in lower_map:
            return lower_map[c]
    # fallback: any column containing 'uri'
    for c in df.columns:
        if "uri" in c.lower():
            return c
    raise KeyError(f"Could not find a URI column in columns={list(df.columns)}")

# ---------------- 1) load + prep features ----------------
feat = read_csv_robust(FEATURES_PATH)

feat_uri_col = find_uri_col(feat)
# create a normalized uri col in file
feat["uri_norm"] = feat[feat_uri_col].map(normalize_spotify_uri)

# keep only needed columns that actually exist in the file, and drop empty uri
missing = [c for c in FEATURE_COLS if c not in feat.columns]
if missing:
    print("[WARN] These requested feature columns are not in the features file:", missing)
keep_cols = ["uri_norm"] + [c for c in FEATURE_COLS if c in feat.columns]
feat_small = feat[keep_cols].dropna(subset=["uri_norm"]).copy()

# if duplicates in features, keep the first 
feat_small = feat_small.drop_duplicates(subset=["uri_norm"], keep="first")

print("Features unique tracks:", feat_small["uri_norm"].nunique())


# ---------------- 2) loop over matched lyric files ----------------
# match based on ouput of lyric merging
files = sorted(MATCHED_DIR.glob("*_with_lyrics.csv"))
print("Matched files found:", len(files))

summary = []
for f in files:
    df = read_csv_robust(f)

    uri_col = find_uri_col(df)

    # ensure we have a normalized URI key to merge on
    if "uri_norm" not in df.columns:
        df["uri_norm"] = df[uri_col].map(normalize_spotify_uri)
    else:
        # if uri_norm exists, still normalize it to be safe
        df["uri_norm"] = df["uri_norm"].map(normalize_spotify_uri)

    out = df.merge(feat_small, on="uri_norm", how="left", suffixes=("", "_featdup"))

    # diagnostics
    # calculate fraction of rows that successfully matched with Spotify features using mean; 
    # if col not found, use keep_cols to calculate
    row_match = out[FEATURE_COLS[0]].notna().mean() if FEATURE_COLS[0] in out.columns else out[keep_cols[1]].notna().mean()
    # use set here to maximize efficiency
    track_uris = set(out["uri_norm"].dropna().unique())
    feat_uris = set(feat_small["uri_norm"].unique())
    track_match = len(track_uris & feat_uris) / len(track_uris) if track_uris else 0.0

    out_path = OUT_DIR / f.name.replace("_with_lyrics.csv", "_with_lyrics_and_features.csv")
    out.to_csv(out_path, index=False)

    summary.append({
        "file": f.name,
        "rows": len(out),
        "unique_tracks": len(track_uris),
        "row_feature_match_rate": row_match,
        "track_feature_match_rate": track_match,
        "output": str(out_path),
    })

summary_df = pd.DataFrame(summary).sort_values("track_feature_match_rate", ascending=False)
print(summary_df.to_string(index=False))
print("Saved enriched files to:", OUT_DIR)