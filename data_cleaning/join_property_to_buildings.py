"""
The properties contain the addresses of the buildings, hence they are joined
To do this, the coordinate of the properties are taken and intersected over
each building. If the property coordinate intersects with the building
polygon, then we merge them
"""

import pandas as pd
import json
from shapely.geometry import shape
from shapely.geometry import mapping as shapely_to_dict
import multiprocessing
import argparse
from pathlib import Path
from shapely.errors import ShapelyDeprecationWarning
import warnings
warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning)

argparser = argparse.ArgumentParser(conflict_handler='resolve')
argparser.add_argument(
    "-j", "--jobs", required=False, default=12, type=int
)
jobs = vars(argparser.parse_known_args()[0])['jobs']

# load and filter property
df_property = pd.read_csv(
    'resources/data/original/property-addresses.csv', delimiter=';'
)
df_property.rename(
    columns={
        'Geo Local Area': 'geo_local_area',
        'STD_STREET': 'street',
        'Geom': 'property_coordinate',
    },
    inplace=True
)
df_property = df_property[['geo_local_area', 'street', 'property_coordinate']]
df_property = df_property.dropna().reset_index(drop=True)
df_property['property_coordinate'] = [
    shape(json.loads(x)) for x in df_property['property_coordinate']
]

# load buildings
df_building = pd.read_csv('resources/data/generated/filter_buildings.csv')
df_building['building_polygon'] = [
    shape(json.loads(x)) for x in df_building['building_polygon']
]


def chunk_process(index, properties, buildings):
    result = []
    length = len(buildings)
    for i, building in enumerate(buildings):
        if i % 100 == 0:
            print(f'{index}: {i+1}/{length}')
        poly = building['building_polygon']
        for prop in properties:
            if not prop['property_coordinate'] \
                    .intersects(poly):
                continue
            entry = building | prop
            entry['property_coordinate'] = json.dumps(
                shapely_to_dict(prop['property_coordinate'])
            )
            entry['building_polygon'] = json.dumps(
                shapely_to_dict(building['building_polygon'])
            )
            result.append(entry)
            continue
    pd.DataFrame(result).to_csv(
        f'resources/data/cache/join_property_to_buildings_temp_{index}.csv',
        index=False
    )


if __name__ == '__main__':
    processes = []
    buildings = df_building.to_dict('records')
    properties = df_property.to_dict('records')
    chunk_size = len(buildings) / jobs
    for j in range(jobs):
        chunk = buildings[round(j * chunk_size): round((j + 1) * chunk_size)]
        process = multiprocessing.Process(
            target=chunk_process,
            args=[j, properties, chunk],
        )
        process.start()
        processes.append(process)

    for process in processes:
        process.join()

    df = pd.concat(
        [
            pd.read_csv(
                'resources/data/cache/'
                f'join_property_to_buildings_temp_{index}.csv'
            )
            for index in range(jobs)
        ],
        ignore_index=True
    )
    for index in range(jobs):
        Path(
            f'resources/data/cache/join_property_to_buildings_temp_{index}.csv'
        ).unlink()

    # write result to csv
    df.to_csv(
        'resources/data/generated/join_property_to_buildings.csv',
        index=False
    )
