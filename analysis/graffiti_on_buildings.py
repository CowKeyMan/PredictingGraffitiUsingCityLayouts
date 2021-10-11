"""
This script checks if the graffiti are always on top of properties
with regards to geolocation
"""

import pandas as pd
import json
from shapely.geometry import shape

df_graffiti = pd.read_csv(
    'resources/data/original/graffiti.csv', delimiter=';'
)
df_graffiti['geometry'] = [shape(json.loads(x)) for x in df_graffiti['Geom']]
df_graffiti['Longitude'] = [geom.x for geom in df_graffiti['geometry']]
df_graffiti['Latitude'] = [geom.y for geom in df_graffiti['geometry']]

df_property = pd.read_csv(
    'resources/data/original/property-addresses.csv', delimiter=';'
)
df_property['geometry'] = [shape(json.loads(x)) for x in df_property['Geom']]
df_property['Longitude'] = [geom.x for geom in df_property['geometry']]
df_property['Latitude'] = [geom.y for geom in df_property['geometry']]

# 5 is wikipedia suggestion for "individual trees, houses"
# source: https://en.wikipedia.org/wiki/Decimal_degrees
round_digits = 5
graffiti_locations = set([
    (round(lat, round_digits), round(lon, round_digits))
    for lat, lon in df_graffiti[['Latitude', 'Longitude']].values
])
properties_locations = set([
    (round(lat, round_digits), round(lon, round_digits))
    for lat, lon in df_graffiti[['Latitude', 'Longitude']].values
])

amount_on_properties \
    = sum([gl in properties_locations for gl in graffiti_locations])

conclusion = \
    f'''There are:
    {len(graffiti_locations)} total graffiti'
    {len(properties_locations)} total properties'
    {amount_on_properties} graffiti on properties'
This means that:
    {amount_on_properties / len(graffiti_locations):.3f} of graffiti are associated with properties
    {amount_on_properties / len(properties_locations):.3f} of properties have some graffiti'''
print(conclusion)
with open('resources/statistics/graffiti_on_properties.txt', 'w') as f:
    f.write(conclusion)
