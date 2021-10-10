"""
Reading from graffiti csv and joining the graffiti with
the buildings based on distance of their coordinates from one another
"""

import json
import pandas as pd
from shapely.geometry import shape
from collections import defaultdict
from shapely.geometry import mapping as shapely_to_dict
from shapely.errors import ShapelyDeprecationWarning
import warnings
warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning)

# 5 is wikipedia suggestion for "individual trees, houses"
# source: https://en.wikipedia.org/wiki/decimal_degrees
round_digits = 5

df_graffiti = pd.read_csv('resources/data/original/graffiti.csv', delimiter=';')
df_graffiti['coordinate'] = [
    shape(json.loads(x)) for x in df_graffiti['Geom']
]
df_graffiti['lon'] \
    = [round(c.x, round_digits) for c in df_graffiti['coordinate']]
df_graffiti['lat'] \
    = [round(c.y, round_digits) for c in df_graffiti['coordinate']]
df_graffiti = df_graffiti[['lat', 'lon', 'COUNT']]

df_building = pd.read_csv(
    'resources/data/generated/join_property_to_buildings.csv'
)
df_building['property_coordinate'] = [
    shape(json.loads(x)) for x in df_building['property_coordinate']
]
df_building['lon'] \
    = [round(c.x, round_digits) for c in df_building['property_coordinate']]
df_building['lat'] \
    = [round(c.y, round_digits) for c in df_building['property_coordinate']]

graffiti_lat_lon_to_counts = defaultdict(int)
for lat, lon, count in df_graffiti.values:
    graffiti_lat_lon_to_counts[
        (round(lon, round_digits), round(lat, round_digits))
    ] += count

df_building['graffiti_count'] = 0
for (lon, lat), count in graffiti_lat_lon_to_counts.items():
    df_building.loc[
        (df_building['lon'] == lon) & (df_building['lat'] == lat),
        'graffiti_count'
    ] += count

df_building['graffiti_count'] = df_building['graffiti_count'].astype(int)
df_building.drop(columns=['lon', 'lat'], inplace=True)
df_building['property_coordinate'] = [
    json.dumps(shapely_to_dict(x)) for x in df_building['property_coordinate']
]
df_building.to_csv(
    'resources/data/generated/buildings_with_graffiti_counts.csv', index=False
)
