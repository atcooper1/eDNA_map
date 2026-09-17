import pandas as pd
import json
from pathlib import Path

# -----------------------------
# SETTINGS
# -----------------------------

# Folder containing this Python script
script_folder = Path(__file__).parent

# GitHub project folder (one level above "convert")
project_folder = script_folder.parent

# Input CSV
input_csv = script_folder / "Sites_RLSeDNA_september_update.csv"

# Output GeoJSON
output_geojson = project_folder / "eDNA_sites_september_update.geojson"

# CSV column names
latitude_column = "latitude"
longitude_column = "longitude"


# -----------------------------
# READ CSV
# -----------------------------

print(f"Reading CSV:")
print(input_csv)

df = pd.read_csv(input_csv)

print(f"Found {len(df)} CSV rows.")


# -----------------------------
# CREATE GEOJSON FEATURES
# -----------------------------

features = []

for _, row in df.iterrows():

    latitude = row[latitude_column]
    longitude = row[longitude_column]

    # Skip rows with missing coordinates
    if pd.isna(latitude) or pd.isna(longitude):
        continue

    properties = {}

    for column in df.columns:

        if column not in [latitude_column, longitude_column]:

            value = row[column]

            if pd.isna(value):
                value = None

            properties[column] = value

    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [
                float(longitude),
                float(latitude)
            ]
        },
        "properties": properties
    }

    features.append(feature)


# -----------------------------
# CREATE GEOJSON
# -----------------------------

geojson = {
    "type": "FeatureCollection",
    "features": features
}


# -----------------------------
# SAVE GEOJSON
# -----------------------------

with open(output_geojson, "w", encoding="utf-8") as file:
    json.dump(
        geojson,
        file,
        indent=2,
        ensure_ascii=False
    )


# -----------------------------
# SUMMARY
# -----------------------------

print()
print("===================================")
print("CONVERSION COMPLETE")
print("===================================")
print(f"CSV rows:       {len(df)}")
print(f"GeoJSON points: {len(features)}")
print()
print(f"GeoJSON saved to:")
print(output_geojson)
print("===================================")
