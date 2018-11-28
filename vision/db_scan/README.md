# Guide for R5 DB_SCAN
### Testing:
Test images are in Test_Images folder.

__input: python3 DB_SCAN.py img_name BALL_RADIUS DENSITY OPTION__
__output__:
* single: a single colored mask of all found objects
* separate: a set of masks for each individual found object
* both: both single and separate
* time: returns a comprehensive time profile of all functions used in the program.

### Suggested BALL_RADIUS, DENSITY Ratios
Density << PI * BALL_RAD ^ 2
| BALL_RADIUS   | DENSITY |
| --------------|-----------|
| 1           | N/A       |
| 2           | N/A       |
| 3           | N/A       |
| 4           | N/A       |
| 5           | 40        |
| 6           | N/A       |
