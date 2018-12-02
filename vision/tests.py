

from tester import *
import importlib
import sys


def fp(s, tab=8):

    left = " " * ((80 - len(s)) // 2 - tab)
    t = " " * tab
    bar = "-" * (len(s) + 16)

    return("\n" + left + bar + "\n" + left + t + s + "\n" + left + bar)


def test(name, target, **kwargs):

    header = (
        "Test Profile for {module} on test case {file}:"
        .format(module=name, file=target))
    print(fp(header))

    module = importlib.import_module(name)

    testcase = VisionTestCase(module, target, **kwargs)
    testcase.run()
    testcase.save()

    print(testcase.profile)


_HINT = """Arguments
---------
[0] module         : name of module to load
[1] target         : name of file to load from that module's test folder

Keyword Arguments
-----------------
General:
- stats=20         : number of profile stats; if 0, none are printed
DBScan:
- r=3              : ball radius to use
- d=8              : ball density to use
- option=single    : single or separate

Examples
--------
python tester.py db_scan r=3 d=5
"""


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(fp("Vision Tester"))
        print(_HINT)
    else:
        module, target = sys.argv[1:3]
        kwargs = {f.split("=")[0]: f.split("=")[1] for f in sys.argv[3:]}

        test(module, target, **kwargs)
