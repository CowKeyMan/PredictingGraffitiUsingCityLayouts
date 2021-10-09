import pandas as pd
import json
from shapely.ops import unary_union
from shapely.geometry import shape, MultiPolygon
from shapely.geometry import mapping as shapely_to_dict
from area import area

# get polygon of the entirety of vancouver so we can see
# which buildings are on top of it
df_vancouver = pd.read_csv(
    'resources/data/original/local-area-boundary.csv', delimiter=';'
)
vancouver_polygons = [shape(json.loads(x)) for x in df_vancouver['Geom']]
vancouver_polygon = unary_union(vancouver_polygons)

# load and drop unecessary columns
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
        'Geom': 'building_polygon'
    },
    inplace=True
)


# group by building id
new_building = []
length = len(df_building['building_id'].unique())
for i, bid in enumerate(df_building['building_id'].unique()):
    if i % 1000 == 0:
        print(f'{i+1}/{length}')
    df = df_building[df_building['building_id'] == bid]
    polygons = [shape(json.loads(x)) for x in df['building_polygon']]
    union_geometry = unary_union(polygons)
    if isinstance(union_geometry, MultiPolygon):
        # one of the buildings did not have a proper union, so we skip it
        continue
    if union_geometry.area \
            != union_geometry.intersection(vancouver_polygon).area:
        continue
    union_geometry_json = json.dumps(shapely_to_dict(union_geometry))
    new_building.append({
        'building_id': bid,
        'roof_type': df['roof_type'].mode()[0],
        'highest_elevation_m': df['highest_elevation_m'].max(),
        'building_polygon': union_geometry_json,
        'area_m2': area(union_geometry_json),
        'sub_buildings': len(df),
    })
df_building = pd.DataFrame(new_building)
df_building.to_csv('resources/data/generated/filter_buildings.csv', index=False)
