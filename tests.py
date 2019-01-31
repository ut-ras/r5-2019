#   ______          __
#  /_  __/__  _____/ /____  _____
#   / / / _ \/ ___/ __/ _ \/ ___/
#  / / /  __(__  ) /_/  __/ /
# /_/  \___/____/\__/\___/_/

"""General purpose tester for all Region-V code.

Each test should be in a class that extends
```unittest.TestCase```. This module should then be imported in some form by
this file.

This file will recursively search all imported modules for
```unittest.TestCase``` objects, and adds them to a test suite. Only modules
with source in the ```r5-2019``` directory will be tested.
"""

import unittest
from types import ModuleType


def get_submodules(module):
    """Get submodules for a module

    Parameters
    ----------
    module : python module
        Module to add recursively. If ```module``` has any other modules
        in it's ```__dict__```, those modules are also added.

    Returns
    module[]
        List of found modules.
    """

    modules = [module]

    for key, value in module.__dict__.items():
        if (
                isinstance(value, ModuleType) and
                hasattr(value, "__file__") and
                "r5-2019" in value.__file__):
            modules += get_submodules(value)

    return modules


def run_tests(modules):
    """Run tests on a set of modules.

    Parameters
    ----------
    modules : module[]
        LIst of modules to test
    """
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    modlist = []
    for module in modules:
        modlist += get_submodules(module)

    for mod in modlist:
        suite.addTests(loader.loadTestsFromModule(mod))

    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)


if __name__ == "__main__":

    import control
    # Add more modules here
    # Ex.
    # import foo
    # import bar

    run_tests([control])
