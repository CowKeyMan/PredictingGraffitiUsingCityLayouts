"""
This script combines graffiti amount to buildings
"""

import pandas as pd
from collections import defaultdict


df = pd.read_csv(
    'resources/data/graffiti_combined.csv',
    dtype={
        'Geo local area': str,
        'Count': int,
        'SITE_ID': str,
        'Latitude': float,
        'Longitude': float,
        'Type': str,
    }
)
df['Graffiti_count'] = 0

# 5 is wikipedia suggestion for "individual trees, houses"
# source: https://en.wikipedia.org/wiki/decimal_degrees
round_digits = 5

graffiti_locations_to_count = defaultdict(int)
for lat, lon, count in \
        df[df['Type'] == 'G'][['Latitude', 'Longitude', 'Count']].values:
    graffiti_locations_to_count[
        (round(lat, round_digits), round(lon, round_digits))
    ] += count

buildings_locations = defaultdict(list)
for lat, lon, site_id in \
        df[df['Type'] == 'B'][['Latitude', 'Longitude', 'SITE_ID']].values:
    buildings_locations[
        (round(lat, round_digits), round(lon, round_digits))
    ].append(site_id)

for location, count in graffiti_locations_to_count.items():
    if location in buildings_locations:
        for site_id in buildings_locations[location]:
            df.loc[df['SITE_ID'] == site_id, 'Graffiti_count'] += count


df = df[df['Type'] == 'B']

df.to_csv('resources/data/buildings_with_graffiti_counts.csv', index=False)
