import pandas as pd
import geopandas as gpd
from matplotlib import pyplot as plt
from shapely.geometry import shape
import json
import argparse
import seaborn as sns

colours = sns.color_palette("gray", 10)

vancouver_colour = colours[4]
edge_colour = colours[5]
buildings_colour = colours[7]

argparser = argparse.ArgumentParser(conflict_handler='resolve')
argparser.add_argument(
    "-w", "--width", required=False, default=300, type=int
)
args = vars(argparser.parse_known_args()[0])
width_inches = args['width']

vancouver = gpd.read_file('resources/data/local-area-boundary.csv')
vancouver['geometry'] = [shape(json.loads(x)) for x in vancouver['Geom']]
buildings = gpd.read_file('resources/data/property-parcel-polygons.csv')
buildings['geometry'] = [shape(json.loads(x)) for x in buildings['Geom']]

buildings_with_graffiti_counts = pd.read_csv(
    'resources/data/buildings_with_graffiti_counts.csv'
)

buildings = buildings.merge(
    buildings_with_graffiti_counts, left_on='SITE_ID', right_on='SITE_ID'
).reset_index()

fig, ax = plt.subplots()
ax.axis('off')
vancouver.plot(
    ax=ax,
    edgecolor=edge_colour,
    facecolor=vancouver_colour,
    antialiased=False,
)
buildings = buildings.sort_values('Graffiti_count')
buildings.plot(
    ax=ax,
    edgecolor=buildings_colour,
    antialiased=False,
    column='Graffiti_count',
    legend=True,
    cmap='OrRd'
)

xlim = ax.get_xlim()
ylim = ax.get_ylim()

x_difference = xlim[1] - xlim[0]
y_difference = ylim[1] - ylim[0]
fig.set_size_inches(width_inches, width_inches / x_difference * y_difference)

fig.savefig(
    'resources/images/vancouver_buildings_heatmap.png',
    bbox_inches='tight',
    transparent="False",
    pad_inches=0
)

plt.show()
