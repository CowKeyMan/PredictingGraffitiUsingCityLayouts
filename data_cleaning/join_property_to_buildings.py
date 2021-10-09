import pandas as pd
import multiprocessing
from pathlib import Path
import argparse
import json
from shapely.ops import unary_union
from shapely.geometry import shape, MultiPolygon
from area import area

filename = Path(__file__).stem

argparser = argparse.ArgumentParser(conflict_handler='resolve')
argparser.add_argument(
    "-j", "--jobs", required=False, default=6, type=int
)
argparser.add_argument(
    "-n", "--no_cache", required=False, action='store_true'
)
args = vars(argparser.parse_known_args()[0])
jobs = args['jobs']
cache = not args['no_cache']


def conv_to_point(val):
    lon, lat = json.loads(val)['coordinates']
    return lat, lon


# load and filter
df_property = pd.read_csv(
    'resources/data/original/property-addresses.csv', delimiter=';'
)
df_property['Geom'] = df_property['Geom'].map(conv_to_point)
df_property['latitude'] = [x[0] for x in df_property['Geom']]
df_property['longitude'] = [x[1] for x in df_property['Geom']]
df_property.rename(
    columns={
        'Geo Local Area': 'geo_local_area',
        'STD_STREET': 'street',
        'Geom': 'geometry',
    },
    inplace=True
)
df_property = df_property[['geo_local_area', 'street', 'geometry']]

if Path(f'resources/data/cache/{filename}_1.csv').exists() and cache:
    df_building = pd.read_csv(f'resources/data/cache/{filename}_1.csv')
    df_building['geometry'] = [
        shape(x) for x in df_building['geometry']
    ]
else:
    df_building = pd.read_csv(
        'resources/data/original/building-footprints-2009.csv', delimiter=';'
        )
    df_building = df_building[[
        'BLDGID',
        'ROOFTYPE',
        'TOPELEV_M',
        'Geom'
    ]]

    df_building.rename(
        columns={
            'BLDGID': 'building_id',
            'ROOFTYPE': 'roof_type',
            'TOPELEV_M': 'highest_elevation_m',
            'Geom': 'geometry'
        },
        inplace=True
    )

    # group by building id

    def polygon_to_json(coordinate_list):
        return {
            "type": "Polygon",
            "coordinates": coordinate_list
        }

    new_building = []
    length = len(df_building['building_id'].unique())
    for i, bid in enumerate(df_building['building_id'].unique()):
        if i % 1000 == 0:
            print(f'{i+1}/{length}')
        df = df_building[df_building['building_id'] == bid]
        polygons = [shape(json.loads(x)) for x in df['geometry']]
        union_geometry = unary_union(polygons)
        if isinstance(union_geometry, MultiPolygon):
            # one of the buildings did not have a proper union, so we skip it
            continue
        coordinate_list = [list(union_geometry.exterior.coords)]
        union_geometry_json = json.dumps(polygon_to_json(coordinate_list))
        new_building.append({
            'building_id': bid,
            'roof_type': df['roof_type'].mode()[0],
            'highest_elevation_m': df['highest_elevation_m'].max(),
            'geometry': union_geometry_json,
            'area_m2': area(union_geometry_json),
            'sub_buildings': len(df),
        })

    df_building = pd.DataFrame(new_building)
    df_building.to_csv(f'resources/data/cache/{filename}_1.csv', index=False)

# join using wether it lies there or not
