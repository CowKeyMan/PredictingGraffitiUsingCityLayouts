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
fig = plt.figure(figsize=(7,3),dpi=144)

roof = fig.add_subplot(121)

roof = sb.countplot(
    x='roof_type',
    hue='graffiti_count',
    data=df
)
for p in roof.patches:
    roof.annotate(f'\n{p.get_height()}', (p.get_x()+0.2, p.get_height()), ha='center', color='black', size=5)
roof.axes.set_title("Roof Type",fontsize=15)
roof.set_xlabel("Roof Type",fontsize=7)
roof.set_ylabel("Amount of Building",fontsize=7)
roof.tick_params(labelsize=5)
plt.setp(roof.get_legend().get_texts(), fontsize='5')
plt.setp(roof.get_legend().get_title(), fontsize='5') # for legend title
plt.legend(labels=['No Graffiti', 'Graffiti'], fontsize='7')

street = fig.add_subplot(122)
street = sb.countplot(
    x='street_type',
    hue='graffiti_count',
    data=df
)
for p in street.patches:
    street.annotate(f'\n{p.get_height()}', (p.get_x()+0.2, p.get_height()), ha='center', color='black', size=5)
street.axes.set_title("Street Type",fontsize=15)
street.set_xlabel("Roof Type",fontsize=7)
street.set_ylabel("Amount of Building",fontsize=7)
street.tick_params(labelsize=5)
plt.setp(street.get_legend().get_texts(), fontsize='5')
plt.setp(street.get_legend().get_title(), fontsize='5') # for legend title
plt.savefig('barchart.png')
plt.legend(labels=['No Graffiti', 'Graffiti'], fontsize='7')
plt.show()