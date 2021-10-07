import pandas as pd


building_area \
    = pd.read_csv('resources/data/graffiti_combined_buildings_area_m2.csv')
building_area = building_area[building_area['Type'] == 'B']
building_area = building_area[['Geo Local Area', 'SITE_ID', 'area_m2']]
local_area = pd.read_csv('resources/data/geolocal_area_m2.csv')
local_area['local_area_m2'] = local_area['area_m2']
local_area = local_area[['Name', 'local_area_m2']]

building_area = building_area.merge(
    local_area, left_on='Geo Local Area', right_on='Name', how='left'
)

building_area['area_normalized'] = \
    building_area['area_m2'] / building_area['local_area_m2']

building_area.to_csv('resources/data/buildings_with_local_area.csv')
