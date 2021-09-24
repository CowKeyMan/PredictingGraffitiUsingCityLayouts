import json
import csv

import pandas as pd
from area import area
with open('local-area-boundary.geojson') as f:
    data = json.load(f)

print('data ', data)

for feature in data['features']:
    print('mapid ', feature['properties']['mapid'])
    print('name ', feature['properties']['name'])
    print('type ',feature['geometry']['type'])
    print('coordinates ', feature['geometry']['coordinates'])
    # https://github.com/mapbox/geojson-area
    print('area ',round(area(feature['geometry']),2))

csv_file = open('resources/data/area_m2.csv', 'w')
header=['mapid', 'name', 'area m2', 'geometry']
csv_writer= csv.writer(csv_file, delimiter=',')
csv_writer.writerow(header)

for feature in data['features']:
    csv_writer.writerow([feature['properties']['mapid'], feature['properties']['name'], round(area(feature['geometry']),2), feature['geometry']['coordinates']])
csv_file.close()