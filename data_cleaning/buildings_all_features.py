"""
Merge buildings, streets and geo local area details so
that all the information is in a single place
"""


import pandas as pd


df_building = pd.read_csv(
    'resources/data/generated/buildings_and_nearby_objects.csv'
)
df_streets = pd.read_csv(
    'resources/data/generated/street_details.csv'
)
df_geo_local_area = pd.read_csv(
    'resources/data/generated/geo_local_area_details.csv'
)

df_building = df_building.merge(df_streets, on='street')
df_building = df_building.merge(df_geo_local_area, on='geo_local_area')

df_building.to_csv(
    'resources/data/generated/buildings_all_features.csv', index=False
)
