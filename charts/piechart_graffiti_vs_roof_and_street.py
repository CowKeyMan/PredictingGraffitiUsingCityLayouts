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
df = df[df.graffiti_count != 0]
print(df.head(n=100).to_string())
print(df.shape)
df['graffiti_count'] = (df['graffiti_count'] > 0).astype(float)
print(df.head(n=100).to_string())
print(df.shape)

roof = df.roof_type.value_counts()
print('roof\n', roof)

street = df.street_type.value_counts()
print('street\n', street)

#total_roof= sum(roof)
def make_autopct_roof(values):
    def my_autopct_roof(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
    return my_autopct_roof
fig = plt.figure(figsize=(5,3),dpi=144)
ax_roof = fig.add_subplot(121)

#plt.figure(0)
ax_roof = roof.plot(
    kind='pie',
    #autopct='%1.1f%%',
    autopct=make_autopct_roof(roof),
    fontsize=5
                    )
ax_roof.set_title(
    'Roof Type in the graffiti building',
    fontsize=7
)
plt.legend(
    title='Roof Type',
    bbox_to_anchor=(0.5, 0.1),
    prop={"size":5},
    title_fontsize=7
)
#plt.show()
def make_autopct_street(values):
    def my_autopct_street(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
    return my_autopct_street
ax_street = fig.add_subplot(122)
#plt.figure(1)
#total_street = sum(street)
ax_street = street.plot(
    kind='pie',
    #autopct='%1.1f%%'
    autopct=make_autopct_street(street),
    fontsize=5
)
ax_street.set_title(
    'Street Type in the graffiti building',
    fontsize=7
)
plt.legend(
    title='Street Type',
    bbox_to_anchor=(1.1, 0.1),
    prop={"size":5},
    title_fontsize=7
)
plt.show()