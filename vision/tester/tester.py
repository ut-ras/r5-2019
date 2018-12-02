
"""Vision test framework"""

import cv2
import os

from .profile import profile


class TestSetupException(Exception):
    """Exception raised by incorrect test setup"""
    pass


def _module_test_dir(module):
    """Get the test directory of a module

    Parameters
    ----------
    module : python module
        Module to get test dir from

    Returns
    -------
    str
        Absolute filepath of the module's tests folder

    Raises
    ------
    TestSetupException
        If no ``tests`` folder is present
    """

    base_dir = os.path.join(os.path.dirname(module.__file__), "tests")

    if not os.path.isdir(base_dir):
        raise TestSetupException("Module must contain 'tests' folder")

    return os.path.join(os.path.dirname(module.__file__), "tests")


def list_tests(module):
    """List test images found in a module's tests folder

    Parameters
    ----------
    module : python module
        Module to search in
    """

    base_dir = _module_test_dir(module)

    return os.path.listdir(base_dir)


class VisionTestCase:
    """Vision test case manager

    Parameters
    ----------
    module : python module
        Module to reference
    filename : str
        Name of the test image to load
    kwargs : dict
        arguments to pass onto the function to be tested
    """

    def __init__(self, module, filename, **kwargs):

        self.module = module
        self.filename = filename
        self._kwargs = kwargs

        self.base_dir = _module_test_dir(module)
        name_split = filename.split(",")[0].split("_")
        self.name = name_split[0]
        self.meta = name_split[1:]
        self.img = cv2.imread(os.path.join(self.base_dir, self.filename), 0)

        if self.img is None:
            raise TestSetupException("Target image does not exist.")

        self.result = None

    def run(self):
        """Run the tester"""

        self.result, self.profile = profile(
            self.module.test, self.img, **self._kwargs)

    def save(self):
        """Save results to a file"""

        if self.result is None:
            raise TestSetupException("Cannot save unexecuted test result")

        if type(self.result) in [list, tuple]:
            for idx, img in enumerate(self.result):
                cv2.imwrite(
                    os.path.join(
                        self.base_dir,
                        "result_" + str(idx) + "_" + self.filename))
        else:
            cv2.imwrite(
                os.path.join(
                    self.base_dir, "result_" + self.filename), self.result)
