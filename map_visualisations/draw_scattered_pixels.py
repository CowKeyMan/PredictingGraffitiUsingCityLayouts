import pandas as pd
import cv2
from utilities import coordinate_to_image_space


type_to_color = {
    'G': (255, 0, 0),
    'B': (0, 255, 0),
    'L': (0, 0, 255),
}
type_to_size = {
    'G': 1,
    'B': 2,
    'L': 2,
}


# load data
vancouver_image = cv2.imread('resources/images/vancouver.png')
df = pd.read_csv(
    'resources/data/graffiti_combined.csv',
    dtype={
        'Geo Local Area': str,
        'Count': int,
        'SITE_ID': str,
        'Latitude': float,
        'Longitude': float,
        'Type': str,
    }
).sort_values('Type').reset_index()

# draw pixels
for i, row in enumerate(df.to_dict('records')):
    x, y = row['Latitude'], row['Longitude']
    cv2.circle(
        vancouver_image,
        coordinate_to_image_space(vancouver_image, (x, y)),
        type_to_size[row['Type']],
        type_to_color[row['Type']],
        -1
    )
    if i % 1000 == 0:
        print(f'{i + 1} / {len(df)}')

cv2.namedWindow('V', cv2.WINDOW_NORMAL)
cv2.imshow('V', vancouver_image)
cv2.waitKey(0)
cv2.imwrite('resources/images/map_with_scattered_pixels.png', vancouver_image)
