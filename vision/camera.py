"""Camera interface module

Command Line Test
-----------------
python camera.py 100
-> captures 100 frames and saves as 1.jpg ... 100.jpg

Usage
-----
camera = Camera()
img = camera.capture()

# do things with img
camera.save()  # saves current image

camera.close()
"""

import time

import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray


class Camera:
    """PiCamera interface"""

    def __init__(self):
        self.camera = PiCamera()
        self.camera.rotation = 180
        self.camera.resolution = (640, 480)
        self.camera.rotation = 180
        self.camera.awb_mode = 'off'
        self.camera.awb_gains = (1.45, 1.9)
        self.capture_raw = PiRGBArray(self.camera)

        self.frame_id = 0
        self.fps = 0
        self.start_time = time.time()

    def capture(self):
        """Capture image

        Returns
        -------
        np.array
            reference to image array; NOT UNIQUE PER CAPTURE.
        """

        self.capture_raw.truncate(0)
        self.camera.capture(
            self.capture_raw, format='bgr', use_video_port=True)

        self.frame_id += 1
        self.fps = (time.time() - self.start_time) / self.frame_id

        return self.capture_raw.array

    def save(self):
        """Save current frame"""

        print("Saved {}.jpg".format(self.frame_id))
        cv2.imwrite("{}.jpg".format(self.frame_id), self.capture_raw.array)

    def close(self):
        """Close camera"""

        self.camera.close()

    def __del__(self):
        """Destructor method to ensure camera closing"""

        self.close()


def capture_test(i=300):

    camera = Camera()

    for _ in range(i):
        camera.capture()
        camera.save()

    camera.close()


if __name__ == '__main__':
    import sys
    if len(sys.argv) >= 2:
        capture_test(int(sys.argv[1]))
