import pandas as pd
import json

# -----------------------------
# SETTINGS
# -----------------------------

input_csv = "convert/Sites_RLSeDNA_september_update.csv"
output_geojson = "eDNA_sites_september_update.geojson"

# Change these if your CSV uses different column names
latitude_column = "latitude"
longitude_column = "longitude"


# -----------------------------
# READ CSV
# -----------------------------

df = pd.read_csv(input_csv)


# -----------------------------
# CREATE GEOJSON FEATURES
# -----------------------------

features = []

for _, row in df.iterrows():

    # Get coordinates
    latitude = row[latitude_column]
    longitude = row[longitude_column]

    # Skip rows with missing coordinates
    if pd.isna(latitude) or pd.isna(longitude):
        continue

    # Convert remaining columns into properties
    properties = {}

    for column in df.columns:
        if column not in [latitude_column, longitude_column]:
            value = row[column]

            # Convert pandas NaN to None
            if pd.isna(value):
                value = None

            properties[column] = value

    # Create GeoJSON Point
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
# SAVE FILE
# -----------------------------

with open(output_geojson, "w", encoding="utf-8") as file:
    json.dump(geojson, file, indent=2, ensure_ascii=False)

print(f"Done! Created {output_geojson}")
print(f"Converted {len(features)} points.")

