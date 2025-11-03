import os
import io
import time
import zipfile
import requests
import pandas as pd
import folium
from datetime import datetime, timezone

# ========== CONFIG ==========
CSV_FILE = "gdelt_fixed.csv"
OUTPUT_FILE = "threat_map_from_csv.html"
AUTO_REFRESH = True
REFRESH_MINUTES = 10

# ========== GDELT SCHEMA ==========
GDELT_COLUMNS = [
    "GLOBALEVENTID","SQLDATE","MonthYear","Year","FractionDate","Actor1Code","Actor1Name",
    "Actor1CountryCode","Actor1KnownGroupCode","Actor1EthnicCode","Actor1Religion1Code",
    "Actor1Religion2Code","Actor1Type1Code","Actor1Type2Code","Actor1Type3Code",
    "Actor2Code","Actor2Name","Actor2CountryCode","Actor2KnownGroupCode","Actor2EthnicCode",
    "Actor2Religion1Code","Actor2Religion2Code","Actor2Type1Code","Actor2Type2Code",
    "Actor2Type3Code","IsRootEvent","EventCode","EventBaseCode","EventRootCode","QuadClass",
    "GoldsteinScale","NumMentions","NumSources","NumArticles","AvgTone","Actor1Geo_Type",
    "Actor1Geo_FullName","Actor1Geo_CountryCode","Actor1Geo_ADM1Code","Actor1Geo_Lat",
    "Actor1Geo_Long","Actor1Geo_FeatureID","Actor2Geo_Type","Actor2Geo_FullName",
    "Actor2Geo_CountryCode","Actor2Geo_ADM1Code","Actor2Geo_Lat","Actor2Geo_Long",
    "Actor2Geo_FeatureID","ActionGeo_Type","ActionGeo_FullName","ActionGeo_CountryCode",
    "ActionGeo_ADM1Code","ActionGeo_Lat","ActionGeo_Long","ActionGeo_FeatureID",
    "DATEADDED","SOURCEURL"
]

# ========== REMAP ==========
QUIRK_REMAP = {
    "UK": "GB", "EI": "IE", "IS": "IL", "GM": "DE", "SP": "ES", "RS": "RU", "UP": "UA",
    "SF": "ZA", "WA": "AU", "AS": "AU", "RQ": "PR", "VQ": "VI",
    "AF": "AF", "AJ": "AZ", "AL": "AL", "AO": "AO", "AR": "AR", "BC": "BW", "BG": "BG",
    "BH": "BH", "BL": "BO", "BM": "MM", "BT": "BT", "CB": "KH", "CH": "CH", "CO": "CO",
    "DA": "DK", "DJ": "DJ", "EN": "EE", "ET": "ET", "GH": "GH", "GI": "GI", "GZ": "PS",
    "HU": "HU", "IR": "IR", "IZ": "IQ", "JA": "JM", "KE": "KE", "KN": "KW", "KS": "KR",
    "LE": "LB", "MA": "MA", "MY": "MY", "NA": "NA", "NI": "NG", "NZ": "NZ", "PE": "PE",
    "PK": "PK", "RO": "RO", "RW": "RW", "SU": "SD", "SW": "SE", "SY": "SY", "SZ": "SZ",
    "TI": "TN", "TU": "TR", "TX": "TM", "TZ": "TZ", "UG": "UG", "VE": "VE", "VM": "VN",
    "VT": "VA", "WE": "PS", "ZI": "ZW",
    "US": "US", "FR": "FR", "IN": "IN", "TH": "TH", "BE": "BE", "BF": "BF",
    "MX": "MX", "CA": "CA", "EG": "EG", "IT": "IT", "NL": "NL", "QA": "QA",
    "TR": "TR", "SA": "SA"
}

# ========== COORDINATES (same as before, shortened for space) ==========
COORDS = {
    "US": ("United States", 38.9, -77.0), "GB": ("United Kingdom", 51.5, -0.1),
    "FR": ("France", 48.8, 2.3), "DE": ("Germany", 52.5, 13.4),
    "RU": ("Russia", 55.8, 37.6), "IN": ("India", 28.6, 77.2),
    "IL": ("Israel", 31.8, 35.2), "AU": ("Australia", -35.3, 149.1),
    "ZA": ("South Africa", -26.2, 28.0), "EG": ("Egypt", 30.0, 31.2),
    "TH": ("Thailand", 13.75, 100.49), "MX": ("Mexico", 19.4, -99.1),
    "CN": ("China", 39.9, 116.4), "TR": ("Turkey", 39.9, 32.8),
    "BR": ("Brazil", -15.8, -47.9), "CA": ("Canada", 45.4, -75.7),
    "PK": ("Pakistan", 33.7, 73.0), "UA": ("Ukraine", 50.45, 30.52),
    "IQ": ("Iraq", 33.3, 44.4), "SA": ("Saudi Arabia", 24.7, 46.7),
}

# ========== NORMALIZE FUNCTION ==========
def normalize_gdelt(df: pd.DataFrame) -> pd.DataFrame:
    """Extract only relevant columns and normalize GDELT region codes."""
    if not set(["SQLDATE", "ActionGeo_CountryCode", "GoldsteinScale"]).issubset(df.columns):
        print("[ERROR] Missing expected GDELT columns; normalization skipped.")
        return df

    df = df[["SQLDATE", "ActionGeo_CountryCode", "GoldsteinScale"]].copy()
    df.columns = ["date", "country", "severity"]
    df["country"] = df["country"].astype(str).str.strip().str.upper().str[:2]
    df["country"] = df["country"].map(lambda c: QUIRK_REMAP.get(c, c))
    df["severity"] = pd.to_numeric(df["severity"], errors="coerce").fillna(0)
    df = df[df["severity"].abs() > 0]
    return df

# ========== FETCH ==========
def fetch_latest_gdelt():
    """Fetch and normalize the latest GDELT export CSV."""
    print("\n[INFO] Checking GDELT lastupdate.txt ...")
    try:
        r = requests.get("http://data.gdeltproject.org/gdeltv2/lastupdate.txt", timeout=20)
        r.raise_for_status()
        latest_url = None
        for line in r.text.splitlines():
            if ".export.CSV.zip" in line:
                latest_url = line.split()[-1].strip()
                break
        if not latest_url:
            raise Exception("No export.CSV.zip found.")

        print(f"[INFO] Latest dataset: {latest_url}")
        resp = requests.get(latest_url, timeout=60)
        resp.raise_for_status()

        with zipfile.ZipFile(io.BytesIO(resp.content)) as z:
            file_name = z.namelist()[0]
            with z.open(file_name) as f:
                df = pd.read_csv(f, sep="\t", header=None, names=GDELT_COLUMNS, low_memory=False)

        print(f"[INFO] Downloaded {len(df)} rows. Normalizing ...")
        df = normalize_gdelt(df)
        df.to_csv(CSV_FILE, index=False)
        print(f"[OK] Saved normalized data → {CSV_FILE}")

    except Exception as e:
        print(f"[ERROR] Failed to fetch new data: {e}")
        if os.path.exists(CSV_FILE):
            print("[WARN] Using cached gdelt_fixed.csv")
        else:
            raise SystemExit("[FATAL] No data available.")

# ========== LOAD ==========
def load_gdelt():
    if not os.path.exists(CSV_FILE):
        raise SystemExit("[ERROR] No CSV found.")
    df = pd.read_csv(CSV_FILE, low_memory=False)
    print(f"[OK] Loaded {len(df)} rows.")
    return df

# ========== PROCESS ==========
def process_data(df):
    print("[INFO] Processing normalized dataset ...")
    if not {"country", "severity"}.issubset(df.columns):
        raise SystemExit("[ERROR] CSV not normalized properly.")
    scores = df.groupby("country", as_index=False)["severity"].mean()
    def risk(x):
        if x >= 8: return "CRITICAL"
        elif x >= 4: return "HIGH"
        elif x >= 2: return "MEDIUM"
        else: return "LOW"
    scores["risk_label"] = scores["severity"].apply(risk)
    print(f"[OK] Computed threat scores for {len(scores)} countries.")
    return scores

# ========== MAP ==========
def generate_map(scores):
    print("[INFO] Generating map ...")
    m = folium.Map(location=[20, 0], zoom_start=2)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    for _, row in scores.iterrows():
        code = row["country"]
        if code not in COORDS:
            continue
        name, lat, lon = COORDS[code]
        color = {"LOW":"green","MEDIUM":"orange","HIGH":"red","CRITICAL":"darkred"}[row["risk_label"]]
        folium.CircleMarker(
            location=(lat, lon), radius=10, color=color,
            fill=True, fill_color=color, fill_opacity=0.6,
            popup=f"{name}: {row['risk_label']} ({row['severity']:.2f})"
        ).add_to(m)
    legend = f"""
    <div style="position: fixed; bottom: 30px; left: 30px; width: 220px;
                background-color: white; border: 2px solid grey; z-index:9999;
                font-size: 14px; padding: 10px;">
      <b>🌍 Global Threat Map</b><br>
      <b>Updated:</b> {ts}<br><hr>
      <span style="color:green;">●</span> Low<br>
      <span style="color:orange;">●</span> Medium<br>
      <span style="color:red;">●</span> High<br>
      <span style="color:darkred;">●</span> Critical
    </div>"""
    m.get_root().html.add_child(folium.Element(legend))
    m.save(OUTPUT_FILE)
    print(f"[✅] Map saved → {OUTPUT_FILE}\n")

# ========== MAIN LOOP ==========
if __name__ == "__main__":
    while True:
        fetch_latest_gdelt()
        df = load_gdelt()
        scores = process_data(df)
        generate_map(scores)
        if not AUTO_REFRESH:
            break
        print(f"[SLEEP] Waiting {REFRESH_MINUTES} minutes before next update...\n")
        time.sleep(REFRESH_MINUTES * 60)
