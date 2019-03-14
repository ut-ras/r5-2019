"""FOV/color-based obstacle detection

Usage
-----
Initialize the vision module with ``VisionModule()``. Call the
``VisionModule.process`` function to get objects from an image.
"""

from matplotlib import pyplot as plt
import cv2
import numpy as np
import math

import samples

import collections
Object = collections.namedtuple("Object", ["rect", "dist", "meta"])


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
    CAM_HEIGHT = 5

    FIELD_LOWER = np.array([8, 130, 180])
    FIELD_UPPER = np.array([12, 200, 255])

    CUBE_LOWER = np.array([0, 0, 170])
    CUBE_UPPER = np.array([255, 120, 255])

    def __init__(
            self, width=640, height=480,
            erode_ksize=0.02, dilate_ksize=0.016):

        self.erode_ksize = int(erode_ksize * width)
        self.dilate_ksize = int(dilate_ksize * width)
        self.width = width
        self.height = height

        def make_square_kernel(i):
            return np.ones((i, i), np.uint8)

        self.__erode_mask = make_square_kernel(self.erode_ksize)
        self.__dilate_mask = make_square_kernel(self.dilate_ksize)
        self.__cube_erode_mask = make_square_kernel(2 * self.erode_ksize)

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

        # Compute and fill convex hull
        hull_fill = np.zeros(mask.shape, dtype=np.uint8)
        contours, hier = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for c in contours:
            hull_fill = cv2.fillConvexPoly(hull_fill, cv2.convexHull(c), 255)

        # bitwise AND with !FIELD
        mask = cv2.bitwise_and(cv2.bitwise_not(mask), hull_fill)

        return mask

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

        contours, hier = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        return [self.__get_object_properties(c, meta) for c in contours]

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

        return cubes + obstacles

    def process(self, img):
        """Process image

        Parameters
        ----------
        img : np.array, size=(WIDTH, HEIGHT, 3)
            Input RGB image

        Returns
        -------
        Object[]
            List of found objects
        """

        if img.shape != (self.width, self.height):
            img = cv2.resize(img, (self.width, self.height))

        img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

        mask = self.__get_field_mask(img)
        cubes = self.__get_objects(img, mask)

        return cubes


WIDTH = 640
HEIGHT = 480

COLORS = {
    "obstacle": (255, 0, 0),
    "cube": (0, 255, 0)
}


def load(tgt):

    return cv2.resize(samples.load(int(tgt)), (WIDTH, HEIGHT))


def draw(img, objects):
    for c in objects:
        cv2.rectangle(
            img,
            (c.rect[0], c.rect[1]),
            (c.rect[0] + c.rect[2], c.rect[1] + c.rect[3]),
            COLORS.get(c.meta), 3)
        plt.text(
            c.rect[0], c.rect[1],
            "{:.2f}".format(c.dist), color=(1, 1, 1))


if __name__ == '__main__':

    import time
    import sys

    mod = VisionModule(width=WIDTH, height=HEIGHT)

    if sys.argv[1] == 'all':
        total = 0
        for i in range(9):

            img = load(i)

            start = time.time()
            objects = mod.process(img)
            dur = time.time() - start

            print(dur)
            total += dur

            plt.subplot(330 + i + 1)
            draw(img, objects)
            plt.imshow(img)

        print("Avg time: {}ms".format(total / 9 * 1000))
        plt.show()

    else:
        img = load(int(sys.argv[1]))

        start = time.time()
        objects = mod.process(img)
        print(time.time() - start)

        draw(img, objects)
        plt.imshow(img)
        plt.show()
