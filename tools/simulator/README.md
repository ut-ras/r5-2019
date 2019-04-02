![r5engine](r5engine/asset/banner.png)

2D multi-robot simulation API for testing the University of Texas at Austin's Region V competition robots.

## Module Functions

* `graphics.py` - fancy font and geometry drawing functions
* `models.py` - 2D piecewise functions, such as for representing probability distributions
* `object.py` - interfaces for simulant objects
* `profiling.py` - trapezoidal and S-curve motion profiling algorithms for robot planning
* `robot.py` - interfaces for creating custom simulator robots
* `robotcontrol.py` - control algorithms for testing simulator functionality
* `robotcore.py` - state machines for assembling virtual robots
* `robotframe.py` - a threaded robot wrapper used to bridge simulated and real robots
* `util.py` - collection of miscellaneous utility functions
* `vision.py` - things relevant to simulating CV

## Dependencies

* NumPy
* pygame

## Maintainers

* [Matthew Yu](https://www.github.com/dimembermatt)
* [Chad Harthan](https://www.github.com/chadharthan)
* [Stefan deBruyn](https://www.github.com/stefandebruyn)
