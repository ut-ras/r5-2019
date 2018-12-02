"""Convex Hull

For finding the convex hull points of a binary openCV image or 2D numpy array.
"""

def convex_hull(image):
    """Finds the convex hull vertices for a binary image.

    Parameters
    ----------
    image : numpy.array
        binary image to perform convexhull on

    Returns
    -------
    [(int)]
        clockwise vertecies of convex hull
    """

    corners = find_corners(image)


    vertices = [corners[0]]

    for i in range(len(corners)):
        vertices.extend(
            _convex_hull_side(
                image, corners[i], corners[(i + 1) % len(corners)]))

    return vertices

def slope(point_a, point_b, flip):
    """Slope between two pixels.

    Parameters
    ----------
    a : \(int\)
        (x, y) coordinate of first pixel
    b : \(int\)
        (x, y) coordinate of second pixel
    flip : bool
        true if slope is needed from a flipped x and y axes

    Returns
    -------
    float
        slope between pixels
    """

    x_a, y_a = point_a
    x_b, y_b = point_b

    dx = x_b - x_a
    dy = y_b - y_a

    return -dx / dy if flip else dy / dx

def _convex_hull_side(image, start, end):
    """Convex hull  on rectanglar subset of an image from one direction.

    Parameters
    ----------
    image : numpy.array
        binary image to be processed
    start : (int)
        top left corner of subset in current orientation
    end : (int)
        bottom right corner of subset in current orientation

    Returns
    -------
    [(int)]
        convex hull set of vertecies not including the starting point
    """

    convex_points = [start]

    x_start, y_start = start
    x_end, y_end = end

    side = (x_start <= x_end, y_start <= y_end)


    ranges = {
        (True, True): [
            [x_start + 1, x_end + 1],
            [y_start, y_end + 1],
            False
            ],
        (False, True): [
            [y_start + 1, y_end + 1],
            [x_start, x_end - 1, -1],
            True
            ],
        (False, False): [
            [x_start - 1, x_end - 1, -1],
            [y_start, y_end - 1, -1],
            False
            ],
        (True, False): [
            [y_start - 1, y_end - 1, -1],
            [x_start, x_end + 1],
            True
            ]
    }

    prev = 0

    for outer in range(*ranges[side][0]):

        curr_pixel = None

        for inner in range(*ranges[side][1]):
            if ranges[side][2] and image[outer, inner] == 0:
                curr_pixel = (inner, outer)
                break
            elif not ranges[side][2] and image[inner, outer] == 0:
                curr_pixel = (outer, inner)
                break

        if curr_pixel is None:
            continue

        while True:
            # slope infinite for first point
            prev_slope = (
                float("-inf") if prev == 0
                else slope(
                    convex_points[prev - 1],
                    convex_points[prev],
                    ranges[side][2]))

            # remove previous point if it yields concave segment
            if prev_slope > slope(
                                convex_points[prev],
                                curr_pixel,
                                ranges[side][2]
                                ):
                convex_points.pop(prev)
                prev -= 1
            # add point to hull if it yields convex segment
            else:
                convex_points.append(curr_pixel)
                prev += 1
                break

    return convex_points[1:]


def find_corners(image):
    """Finds the four exteme pixels of a binary image.

    Parameters
    ----------
    image : numpy.array
        image of which to find corners of

    Returns
    -------
    [(int)]
        most top left, top right, bottom right, and bottom left pixels of the
        image
    """

    corners = []

    for side in range(4):
        corners.append(_find_corner(image, side))
    return corners


def _find_corner(image, corner):
    """Finds the extreme pixel of a binary image in a given direction.

    Parameters
    ----------
    image : numpy.array
        binary image to find corner in
    corner : int
        0 for top right, 1 for top left, 2 for bottom right, 3 for bottom left

    Returns
    -------
    (int)
        corner pixel in corner direction
    """

    # TODO make corner an enum

    height, width = image.shape

    ranges = {
        0: [[height], [width], True],
        1: [[width - 1, 0, -1], [height], False],
        2: [[height - 1, 0, -1], [width - 1, 0, -1], True],
        3: [[width], [height - 1, 0, -1], False]
    }

    for outer in range(*ranges[corner][0]):
        for inner in range(*ranges[corner][1]):
            if ranges[corner][2] and image[outer, inner] == 0:
                return (inner, outer)
            elif not ranges[corner][2] and image[inner, outer] == 0:
                return (outer, inner)
