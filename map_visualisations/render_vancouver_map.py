"""
Renders an image of the vancouver map, given the local-area-boundary
data, to an image called 'vancouver.jpg'

Run with the -w/--width parameter in order to change the size of the
returned image
"""

import geopandas as gpd
from matplotlib import pyplot as plt
import argparse

argparser = argparse.ArgumentParser(conflict_handler='resolve')
argparser.add_argument(
    "-w", "--width", required=False, default=15, type=int
)
width_inches = vars(argparser.parse_known_args()[0])['width']

vancouver = gpd.read_file('resources/data/local-area-boundary.geojson')
fig, ax = plt.subplots()
ax.axis('off')
vancouver.plot(
    ax=ax,
    edgecolor=(0.5, 0.5, 0.5),
    facecolor=(0, 0, 0),
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
