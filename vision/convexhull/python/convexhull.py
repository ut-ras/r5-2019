"""Convex Hull

Module docstring goes here
"""


def slope(a, b, flip):
    """returns slope between two pixels

    Parameters
    ----------
    a : tuple of ints
        (x, y) coordinate of first pixel
    b : tuple of ints
        (x, y) coordinate of second pixel
    flip : bool
        true if slope is needed from a flipped x and y axes

    Returns
    -------
    float
        slope between pixels
    """

    ax, ay = a
    bx, by = b

    dx = bx - ax
    dy = by - ay

    return -dx / dy if flip else dy / dx


def convex_hull(image):
    """finds the convex hull vertecies for a binary image

    Parameters
    ----------
    image : binary opencv image
        image to perform convexhull on

    Returns
    -------
    list of tuples of ints
        clockwise vertecies of convex hull
    """

    corners = find_corners(image)

    print("Corners:", corners)

    vertices = [corners[0]]

    for i in range(len(corners)):
        print("Convex hulling points: ", corners[i], corners[(i + 1) % len(corners)])
        vertices.extend(
            _convex_hull_side(
                image, corners[i], corners[(i + 1) % len(corners)]))

    return vertices


def _convex_hull_side(image, start, end):
    """performs convex hull algorihim on rectanglar subset of an image from one direction

    Parameters
    ----------
    image : binary opencv image
        image to be processed
    start : tuple of ints
        top left corner of subset in current orientation
    end : tuple of ints
        bottom right corner of subset in current orientation

    Returns
    -------
    list of tuples of ints
        convex hull set of vertecies not including the starting point
    """

    convex_points = [start]

    x1, y1 = start
    x2, y2 = end

    side = (x1 <= x2, y1 <= y2)

    print(side)

    ranges = {
        (True, True): [[x1 + 1, x2 + 1], [y1, y2 + 1], False],
        (False, True): [[y1 + 1, y2 + 1], [x1, x2 - 1, -1], True],
        (False, False): [[x1 - 1, x2 - 1, -1], [y1, y2 - 1, -1], False],
        (True, False): [[y1 - 1, y2 - 1, -1], [x1, x2 + 1], True]
    }

    prev = 0

    for outer in range(*ranges[side][0]):

        curr_pixel = None

        for inner in range(*ranges[side][1]):
            '''if ranges[side][2]:
                print(inner, outer)
            else:
                print(outer, inner)'''
            if ranges[side][2] and image[outer, inner] == 0:
                curr_pixel = (inner, outer)
                break
            elif not ranges[side][2] and image[inner, outer] == 0:
                curr_pixel = (outer, inner)
                break

        if curr_pixel is None:
            continue

        print(f"Tst: {curr_pixel}")

        while True:
            # slope infinite for first point
            prev_slope = (
                float("-inf") if prev == 0
                else slope(
                    convex_points[prev - 1],
                    convex_points[prev],
                    ranges[side][2]))

            print(f"Slp: {prev_slope} : {slope(convex_points[prev], curr_pixel, ranges[side][2])}")

            # remove previous point if it yields concave segment
            if prev_slope > slope(convex_points[prev], curr_pixel, ranges[side][2]):
                print(f"Del: {convex_points.pop(prev)}")
                prev -= 1
            # add point to hull if it yields convex segment
            else:
                print(f"Add: {curr_pixel}")
                convex_points.append(curr_pixel)
                prev += 1
                break

    return convex_points[1:]


def find_corners(image):
    """finds the four exteme pixels of a binary image

    Parameters
    ----------
    image : binary opencv image
        image of which to find corners of

    Returns
    -------
    list of tuples of ints
        most top left, top right, bottom right, and bottom left pixels of the image
    """

    corners = []

    for side in range(4):
        corners.append(_find_corner(image, side))
    return corners


def _find_corner(image, corner):
    """finds the extreme pixel of a binary image in a given direction

    Parameters
    ----------
    image : binary opencv image
        image to find corner in
    corner : int
        0 for top right, 1 for top left, 2 for bottom right, 3 for bottom left

    Returns
    -------
    tuple of ints
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
