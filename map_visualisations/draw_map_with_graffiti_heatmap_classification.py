import geopandas as gpd
import matplotlib
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
    "-w", "--width", required=False, default=100, type=int
)
args = vars(argparser.parse_known_args()[0])
width_inches = args['width']

vancouver = gpd.read_file('resources/data/original/local-area-boundary.csv')
vancouver['geometry'] = [shape(json.loads(x)) for x in vancouver['Geom']]
buildings \
    = gpd.read_file('resources/data/generated/buildings_all_features.csv')
buildings['geometry'] \
    = [shape(json.loads(x)) for x in buildings['building_polygon']]

buildings['graffiti_count'] \
    = (buildings['graffiti_count'].astype(float) > 0).astype(float)

# custom colourmap
norm = matplotlib.colors.Normalize(0, buildings['graffiti_count'].max())
colors = [
    [norm(0), buildings_colour],
    [norm(0.99), buildings_colour],
    [norm(1), (246 / 255, 124 / 255, 82 / 255)],
    [norm(buildings['graffiti_count'].max()), "darkred"]
]
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", colors)

fig, ax = plt.subplots()
ax.axis('off')
vancouver.plot(
    ax=ax,
    edgecolor=edge_colour,
    facecolor=vancouver_colour,
    antialiased=True,
)
buildings = buildings.sort_values('graffiti_count')
buildings.plot(
    ax=ax,
    antialiased=True,
    column='graffiti_count',
#     legend=True,
    cmap=cmap,
)

xlim = ax.get_xlim()
ylim = ax.get_ylim()

x_difference = xlim[1] - xlim[0]
y_difference = ylim[1] - ylim[0]
fig.set_size_inches(width_inches, width_inches / x_difference * y_difference)

fig.savefig(
    'resources/images/vancouver_buildings_heatmap_classification.png',
    bbox_inches='tight',
    transparent="False",
    pad_inches=0.4
)

plt.show()
