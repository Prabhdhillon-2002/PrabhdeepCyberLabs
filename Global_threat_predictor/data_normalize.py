import pandas as pd
import os

# === Adjust these paths for Windows ===
input_file = r"YOUR_PATH_HERE\gdeltv2_export.csv"  # Replace with your actual path
output_file = r"#YOUR_PATH_HERE\gdelt_fixed.csv"

if not os.path.exists(input_file):
    raise SystemExit(f"[ERROR] File not found: {input_file}")

# === GDELT v2 column structure (58+ columns) ===
gdelt_columns = [
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

# === Read CSV with no header ===
print(f"[INFO] Loading {input_file} ...")
df = pd.read_csv(input_file, sep="\t", header=None, names=gdelt_columns, low_memory=False)
print(f"[OK] Loaded {len(df)} rows, {len(df.columns)} columns.")

# === Keep only relevant columns ===
fixed_df = df[["SQLDATE", "ActionGeo_CountryCode", "GoldsteinScale"]].copy()

# === Save clean version ===
fixed_df.to_csv(output_file, index=False)
print(f"[✅] Fixed CSV saved as {output_file} with {len(fixed_df)} rows and {len(fixed_df.columns)} columns.")
