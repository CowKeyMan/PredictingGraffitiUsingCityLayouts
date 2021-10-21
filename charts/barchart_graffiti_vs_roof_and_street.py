import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

df = pd.read_csv('buildings_all_features.csv')
df.drop(
    columns=[
        'highest_elevation_m',
        'building_polygon',
        'area_m2',
        'property_coordinate',
        'lon',
        'lat',
        'sub_buildings',
        'nearby_buildings_count',
        'nearby_graffiti_count',
        'nearby_graffiti_average',
        'nearby_graffiti_buildings',
        'nearby_buildings_average_height',
        'nearby_buildings_median_height',
        'nearby_buildings_total_sub_buildings',
        'nearby_buildings_average_sub_buildings',
        'nearby_buildings_median_sub_buildings',
        'geo_local_area_area_m2',
        'geo_local_area_population',
        'pop_density'
    ], inplace=True
)
print(df.head(n=100).to_string())
print(df.shape)
df['graffiti_count'] = (df['graffiti_count'] > 0).astype(float)
print(df.head(n=100).to_string())
print(df.shape)

roof = sb.countplot(
    x='roof_type',
    hue='graffiti_count',
    data=df
)
plt.show()
street = sb.countplot(
    x='street_type',
    hue='graffiti_count',
    data=df
)
plt.show()