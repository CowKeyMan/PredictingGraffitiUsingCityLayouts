"""
Get other buildings and street lighting poles which are next
to each building. We also extract some information from nearby
buildings:

    * nearby_buildings_count
    * nearby_graffiti_count
    * nearby_graffiti_average
    * nearby_graffiti_buildings
    * nearby_buildings_average_height
    * nearby_buildings_median_height
    * nearby_buildings_total_sub_buildings
    * nearby_buildings_average_sub_buildings
    * nearby_buildings_median_sub_buildings

'nearby buildings' do not include the current building itself
"""

import json
import pandas as pd
from shapely.geometry import shape
import numpy as np
from shapely.errors import ShapelyDeprecationWarning
import warnings
warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning)


def euclidean(x1: float, y1: float, x2: float, y2: float):
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


initial_ref_point = (49.278439, -123.091596)
one_house_away_ref_point = (49.278684, -123.091583)
one_house_away_distance \
    = euclidean(*initial_ref_point, *one_house_away_ref_point)

name_to_distance = {
    'one_house_away': one_house_away_distance,
    'two_houses_away': one_house_away_distance * 2,
    'four_houses_away': one_house_away_distance * 4,
}

# 5 is wikipedia suggestion for "individual trees, houses"
# source: https://en.wikipedia.org/wiki/decimal_degrees
round_digits = 5

df_building = pd.read_csv(
    'resources/data/generated/buildings_with_graffiti_counts.csv'
)
df_building['property_coordinate'] = [
    shape(json.loads(x)) for x in df_building['property_coordinate']
]
df_building['lon'] \
    = [round(c.x, round_digits) for c in df_building['property_coordinate']]
df_building['lat'] \
    = [round(c.y, round_digits) for c in df_building['property_coordinate']]

df_lighting = pd.read_csv(
    'resources/data/original/street-lighting-poles.csv', delimiter=';'
)
df_lighting['Geom'] = [
    shape(json.loads(x)) for x in df_lighting['Geom']
]
df_lighting['lon'] \
    = [round(c.x, round_digits) for c in df_lighting['Geom']]
df_lighting['lat'] \
    = [round(c.y, round_digits) for c in df_lighting['Geom']]


buildings = df_building.to_dict('records')
length = len(buildings)
for i, building in enumerate(buildings):
    if i % 1000 == 0:
        print(f'{i+1}/{length}')
    building_distances = euclidean(
        building['lat'],
        building['lon'],
        df_building['lat'],
        df_building['lon'],
    )
    for name, distance in name_to_distance.items():
        np.set_printoptions(precision=20)
        df_close_buildings = df_building[
            (building_distances < distance)
            & (building_distances > 1e-12)
        ]
        exists = len(df_close_buildings)
        building |= {
            f'{name}_buildings_count': len(df_close_buildings),
            f'{name}_graffiti_count':
                df_close_buildings['graffiti_count'].sum(),
            f'{name}_graffiti_average':
                df_close_buildings['graffiti_count'].mean() if exists else 0,
            f'{name}_graffiti_buildings':
                sum(df_close_buildings['graffiti_count'] > 0),
            f'{name}_buildings_average_height':
                df_close_buildings['highest_elevation_m'].mean() if exists
                else 0,
            f'{name}_buildings_median_height':
                df_close_buildings['highest_elevation_m'].median() if exists
                    else 0,
            f'{name}_buildings_total_sub_buildings':
                df_close_buildings['sub_buildings'].sum(),
            f'{name}_buildings_average_sub_buildings':
                df_close_buildings['sub_buildings'].mean() if exists else 0,
            f'{name}_buildings_median_sub_buildings':
                df_close_buildings['sub_buildings'].median() if exists else 0,
        }

        lighting_distances = euclidean(
            building['lat'],
            building['lon'],
            df_lighting['lat'],
            df_lighting['lon'],
        )
        df_close_lighting = df_lighting[lighting_distances < distance]
        building |= {f'{name}_street_lights': len(df_close_lighting)}

pd.DataFrame(buildings).to_csv(
    'resources/data/generated/buildings_and_nearby_objects.csv', index=False
)
