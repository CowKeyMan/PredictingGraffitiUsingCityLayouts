import pandas as pd
from area import area
import json
import numpy as np


df = pd.read_csv(
    'resources/data/property-parcel-polygons.csv',
    delimiter=';',
    dtype={
        'CIVIC_NUMBER': str,
        'STREETNAME': str,
        'TAX_COORD': str,
        'SITE_ID': str,
        'Geom': str,
    }
)
df['area_m2'] \
    = df.apply(lambda row: round(area(json.loads(row['Geom'])), 2), axis=1)
df['geometry'] = df['Geom']
df = df[['SITE_ID', 'area_m2', 'geometry']]
df['SITE_ID'] = df['SITE_ID'].astype(str)

df_combined = pd.read_csv(
    'resources/data/graffiti_combined.csv',
    dtype={
        'Geo Local Area': str,
        'Count': np.int32,
        'SITE_ID': str,
        'Latitude': float,
        'Longitude': float,
        'Type': str,
    }
)

df_combined = pd.merge(df_combined, df, "left", on="SITE_ID")

df_combined.to_csv(
    'resources/data/graffiti_combined_buildings_area_m2.csv',
    index=False
)
