import pandas as pd
from area import area
import json


df = pd.read_csv('resources/data/local-area-boundary.csv', delimiter=';')
df['area_m2'] \
    = df.apply(lambda row: round(area(json.loads(row['Geom'])), 2), axis=1)
df['geometry'] = df['Geom']
df.drop(columns=['Geom', 'geo_point_2d'], inplace=True)
df.to_csv('resources/data/geolocal_area_m2.csv', index=False)
