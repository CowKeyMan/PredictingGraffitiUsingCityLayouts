"""
Renders an image of the vancouver map, given the local-area-boundary
data, to an image called 'vancouver.jpg'

Run with the -w/--width parameter in order to change the size of the
returned image
"""

import geopandas as gpd
from matplotlib import pyplot as plt
from shapely.geometry import shape
import json
import argparse

edge_colour = (0.5, 0.5, 0.5)
vancouver_colour = (0, 0, 0)
buildings_colour = (0.7, 0.7, 0.7)

argparser = argparse.ArgumentParser(conflict_handler='resolve')
argparser.add_argument(
    "-w", "--width", required=False, default=15, type=int
)
argparser.add_argument(
    "-b", "--buildings", required=False, default=False, action='store_true'
)
args = vars(argparser.parse_known_args()[0])
width_inches = args['width']

vancouver = gpd.read_file('resources/data/local-area-boundary.csv')
vancouver['geometry'] = [shape(json.loads(x)) for x in vancouver['Geom']]
buildings = gpd.read_file('resources/data/property-parcel-polygons.csv')
buildings['geometry'] = [shape(json.loads(x)) for x in buildings['Geom']]
fig, ax = plt.subplots()
ax.axis('off')
vancouver.plot(
    ax=ax,
    edgecolor=edge_colour,
    facecolor=(0, 0, 0),
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
