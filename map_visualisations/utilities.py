import numpy as np


def coordinate_to_image_space(
    image: np.ndarray, coordinate: tuple[float, float]
) -> tuple[int, int]:
    xlim = (-123.23492813110349, -123.01311874389648)
    ylim = (49.19409275054516, 49.30065441131179)
    (lat, lon) = coordinate
    ret_x = (lon - xlim[0]) / (xlim[1] - xlim[0]) * image.shape[1]
    ret_y = \
        image.shape[0] - (lat - ylim[0]) / (ylim[1] - ylim[0]) * image.shape[0]
    return round(ret_x), round(ret_y)
