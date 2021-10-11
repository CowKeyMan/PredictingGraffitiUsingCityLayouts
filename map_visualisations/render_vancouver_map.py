"""
Renders an image of the vancouver map, given the local-area-boundary
data, to an image called 'vancouver.jpg'

Run with the -w/--width parameter in order to change the size of the
returned image

Run with -b/--buildings to also draw the buildings
"""

import geopandas as gpd
from matplotlib import pyplot as plt
from shapely.geometry import shape
import json
import argparse
import seaborn as sns

colours = sns.color_palette("gray", 10)

vancouver_colour = colours[4]
edge_colour = colours[5]
buildings_colour = (0, 0, 0)

argparser = argparse.ArgumentParser(conflict_handler='resolve')
argparser.add_argument(
    "-w", "--width", required=False, default=15, type=int
)
argparser.add_argument(
    "-b", "--buildings", required=False, default=False, action='store_true'
)
args = vars(argparser.parse_known_args()[0])
width_inches = args['width']

vancouver = gpd.read_file('resources/data/original/local-area-boundary.csv')
vancouver['geometry'] = [shape(json.loads(x)) for x in vancouver['Geom']]
buildings = gpd.read_file(
    'resources/data/generated/buildings_with_graffiti_counts.csv'
)
buildings['geometry'] \
    = [shape(json.loads(x)) for x in buildings['building_polygon']]
fig, ax = plt.subplots()
ax.axis('off')
vancouver.plot(
    ax=ax,
    edgecolor=edge_colour,
    facecolor=vancouver_colour,
    antialiased=False,
)
if args['buildings']:
    buildings.plot(
        ax=ax,
        edgecolor=buildings_colour,
        facecolor=buildings_colour,
        antialiased=False,
    )

xlim = ax.get_xlim()
ylim = ax.get_ylim()

print(f'xlim: {xlim}, ylim {ylim}')

x_difference = xlim[1] - xlim[0]
y_difference = ylim[1] - ylim[0]
fig.set_size_inches(width_inches, width_inches / x_difference * y_difference)

fig.savefig(
    'resources/images/vancouver.png',
    bbox_inches='tight',
    transparent="False",
    pad_inches=0
)

plt.show()
