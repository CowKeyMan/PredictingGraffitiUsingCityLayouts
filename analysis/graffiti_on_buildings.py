"""
This script checks if the graffiti are always on top of buildings
with regards to geolocation
"""

import pandas as pd

df = pd.read_csv(
    'resources/data/graffiti_combined.csv',
    dtype={
        'Geo Local Area': str,
        'Count': int,
        'SITE_ID': str,
        'Latitude': float,
        'Longitude': float,
        'Type': str,
    }
)

# 5 is wikipedia suggestion for "individual trees, houses"
# source: https://en.wikipedia.org/wiki/Decimal_degrees
round_digits = 5
graffiti_locations = set([
    (round(lat, round_digits), round(lon, round_digits))
    for lat, lon in df[df['Type'] == 'G'][['Latitude', 'Longitude']].values
])
buildings_locations = set([
    (round(lat, round_digits), round(lon, round_digits))
    for lat, lon in df[df['Type'] == 'B'][['Latitude', 'Longitude']].values
])

amount_on_buildings = 0
for gl in graffiti_locations:
    if gl in buildings_locations:
        amount_on_buildings += 1

conclusion = \
    f'''There are:
    {len(graffiti_locations)} total graffiti'
    {len(buildings_locations)} total buildings'
    {amount_on_buildings} graffiti on buildings'
This means that:
    {amount_on_buildings / len(graffiti_locations):.3f} of graffiti are associated with buildings
    {amount_on_buildings / len(buildings_locations):.3f} of buildings have some graffiti'''
print(conclusion)
with open('resources/statistics/graffiti_on_buildings.txt', 'w') as f:
    f.write(conclusion)
