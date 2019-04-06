"""FOV/color-based obstacle detection

Usage
-----
Initialize the vision module with ``VisionModule()``. Call the
``VisionModule.process`` function to get objects from an image.
"""

import cv2
import numpy as np
import math


import collections
Object = collections.namedtuple("Object", ["rect", "dist", "meta"])


def _find_contours(mask):
    """Helper function to deal with OpenCV version changes in the findContours
    API, because fuck opencv, you assholes"""

    if cv2.__version__ == '4.0.0':
        contours, hier = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    else:
        _, contours, hier = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    return contours


class VisionModule():
    """Vision module

    Parameters
    ----------
    width : int
        Image width.
    height : int
        Image height. If the input image shape (to process) is not equal to
        (width, height), the image is resized.
    erode_ksize : float
        Erosion kernel size, as a fraction of the image width.
    dilate_ksize : float
        Dilation kernel size, as a fraction of the image width.
    """

    FOV_H = math.radians(63.54)
    FOV_V = math.radians(42.36)
    CAM_HEIGHT = 6

    FIELD_LOWER = np.array([0, 110, 130])
    FIELD_UPPER = np.array([25, 255, 255])

    CUBE_LOWER = np.array([0, 17, 110])
    CUBE_UPPER = np.array([30, 213, 230])

    BASE_STATION_LOWER = np.array([45, 140, 60])
    BASE_STATION_UPPER = np.array([65, 255, 150])

    LIGHT_LOWER = np.array([70, 20, 250])
    LIGHT_UPPER = np.array([100, 50, 255])

    GREEN_LOWER = np.array([50, 245, 50])
    GREEN_UPPER = np.array([70, 255, 80])

    YELLOW_LOWER = np.array([20, 220, 175])
    YELLOW_UPPER = np.array([30, 255, 255])

    HORIZON = 240

    def __init__(
            self, width=640, height=480,
            erode_ksize=0.025, dilate_ksize=0.020, cube_ksize=0.04,
            isolate=5):

        self.erode_ksize = int(erode_ksize * width)
        self.dilate_ksize = int(dilate_ksize * width)
        self.cube_ksize = int(cube_ksize * width)
        self.width = width
        self.height = height
        self.isolate = isolate

        def make_square_kernel(i):
            return np.ones((i, i), np.uint8)

        self.__erode_mask = make_square_kernel(self.erode_ksize)
        self.__dilate_mask = make_square_kernel(self.dilate_ksize)
        self.__cube_erode_mask = make_square_kernel(self.erode_ksize)

    def __below_horizon(self, contour):

        x, y, w, h = cv2.boundingRect(contour)
        return y + h > self.HORIZON and w > 100 and h > 50

    def __get_field_mask(self, src):
        """Get field mask:

        mask <- erode, then dilate thresholded scene
        intersect mask complement with convex hull of mask

        Parameters
        ----------
        src : np.array -- shape=(WIDTH, HEIGHT, 3)
            Input image

        Returns
        -------
        np.array -- shape=(WIDTH, HEIGHT)
            Object mask
        """

        # Threshold
        mask = cv2.inRange(src, self.FIELD_LOWER, self.FIELD_UPPER)

        # Clean up
        mask = cv2.erode(mask, self.__erode_mask)
        mask = cv2.dilate(mask, self.__dilate_mask)
        cv2.rectangle(mask, (0, 0), (640, self.HORIZON), 0, -1)

        # Compute and fill convex hull
        hull_fill = np.zeros(mask.shape, dtype=np.uint8)
        try:
            contours = np.concatenate([
                c for c in _find_contours(mask)
                if self.__below_horizon(c)
            ])

            cvxhull = cv2.convexHull(contours)
            hull_fill = cv2.fillConvexPoly(hull_fill, cvxhull, 255)

            # bitwise AND with !FIELD
            mask = cv2.bitwise_and(cv2.bitwise_not(mask), hull_fill)
            return mask, cvxhull

        except ValueError:
            return mask, None

    def __get_object_properties(self, obj, meta):
        """Get object properties

        Parameters
        ----------
        obj : np.array
            Contour (one output of cv2.findContours)
        meta : arbitrary type
            Object metadata (is assigned to 'meta' flag)

        Returns
        -------
        Object
            Object with computed bounding box, distance, and tagged metadata
        """

        x, y, w, h = cv2.boundingRect(obj)
        try:
            d = (
                self.CAM_HEIGHT /
                math.tan(
                    self.FOV_V * ((y + h) - self.height / 2) / self.height))
        except ZeroDivisionError:
            d = -1

        return Object(rect=[x, y, w, h], dist=d, meta=meta)

    def __mask_to_objects(self, mask, meta):
        """Convert mask to a list of Objects

        Parameters
        ----------
        mask : np.array -- size=(WIDTH, HEIGHT)
            Input mask
        meta : arbitrary type
            Mask metadata; all objects are tagged with 'meta'

        Returns
        -------
        Object[]
            List of found objects
        """

        try:
            return [
                self.__get_object_properties(c, meta)
                for c in _find_contours(mask)
            ]
        except ValueError:
            return []

    def __get_objects(self, src, mask):
        """Get cubes and obstacles in the scene

        Parameters
        ----------
        src : np.array -- size=(WIDTH, HEIGHT, 3)
            Input image
        mask : np.array -- size=(WIDTH, HEIGHT)
            Obstacle Mask

        Returns
        -------
        Object[]
            Found objects
        """

        # cv2.imshow("src", src)

        green_halo = cv2.inRange(src, self.GREEN_LOWER, self.GREEN_UPPER)
        green_halo = cv2.dilate(green_halo, self.__dilate_mask)
        cv2.rectangle(green_halo, (0, self.HORIZON), (640, 480), 0, -1)
        green = self.__mask_to_objects(green_halo, "green")

        yellow_halo = cv2.inRange(src, self.YELLOW_LOWER, self.YELLOW_UPPER)
        yellow_halo = cv2.dilate(yellow_halo, self.__dilate_mask)
        cv2.rectangle(yellow_halo, (0, self.HORIZON), (640, 480), 0, -1)
        yellow = self.__mask_to_objects(yellow_halo, "yellow")

        base_station = cv2.inRange(
            src, self.BASE_STATION_LOWER, self.BASE_STATION_UPPER)
        base_station = cv2.dilate(base_station, self.__dilate_mask)
        base = self.__mask_to_objects(base_station, "base")

        cube_mask = cv2.inRange(src, self.CUBE_LOWER, self.CUBE_UPPER)
        cube_mask = cv2.bitwise_and(mask, cube_mask)
        cube_mask = cv2.dilate(cube_mask, self.__dilate_mask)
        cube_mask = cv2.erode(cube_mask, self.__cube_erode_mask)
        cube_mask = cv2.dilate(cube_mask, self.__dilate_mask)

        cubes = self.__mask_to_objects(cube_mask, "cube")

        mask = cv2.bitwise_and(mask, cv2.bitwise_not(cube_mask))
        mask = cv2.erode(mask, self.__erode_mask)
        mask = cv2.dilate(mask, self.__dilate_mask)

        obstacles = self.__mask_to_objects(mask, "obstacle")

        return cubes + obstacles + yellow + green + base

    def __inside(self, target, refs):

        for r in refs:
            if (r.rect[0] - self.isolate < target.rect[0] and (
                    r.rect[0] + r.rect[2] + self.isolate >
                    target.rect[0] + target.rect[2])):
                return True
        return False

    def __contains(self, target, refs):

        for r in refs:
            if (target.rect[0] - self.isolate < r.rect[0] and (
                    target.rect[0] + target.rect[2] + self.isolate >
                    r.rect[0] + r.rect[2])):
                return True
        return False

    def process(self, img):
        """Process image

        Parameters
        ----------
        img : np.array, size=(WIDTH, HEIGHT, 3)
            Input BGR image

        Returns
        -------
        Object[]
            List of found objects
        """

        if img.shape != (self.width, self.height):
            img = cv2.resize(img, (self.width, self.height))

        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        mask, cvxhull = self.__get_field_mask(img)
        objs = self.__get_objects(img, mask)

        final = []
        objs.sort(key=lambda x: x.rect[2], reverse=True)
        for x in objs:

            if x.meta in ["yellow", "blue", "green"]:
                if x.rect[2] > 25:
                    final.append(x)
            elif x.meta in ["base"]:
                if x.rect[2] < 100 and x.rect[3] > 50:
                    final.append(x)
            else:
                if not self.__inside(x, final):
                    final.append(x)

        return final, mask, cvxhull
