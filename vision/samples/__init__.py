"""Sample Images"""

import cv2
import os

ALLOWED_EXTENSIONS = ['jpg', 'JPG', 'png', 'PNG', 'JPEG', 'jpeg']


#
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
FILES = [
    f for f in os.listdir(BASE_DIR)
    if f.split('.')[-1] in ALLOWED_EXTENSIONS]


def __load(f):

    return cv2.cvtColor(cv2.imread(f), cv2.COLOR_BGR2RGB)


def load(x):

    # str -> is target filename
    if type(x) == str:
        return __load(os.path.join(BASE_DIR, x))

    # int -> load ith image
    elif type(x) == int and x < len(FILES):
        return __load(os.path.join(BASE_DIR, FILES[x]))

    else:
        raise ValueError("Invalid load target")
