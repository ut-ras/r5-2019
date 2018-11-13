# Guide for R5 DB_SCAN
### Testing:
input: python3 DB_SCAN2.py img_name BALL_RADIUS DENSITY
output: result with labeled parameters

### Suggested BALL_RADIUS, DENSITY Ratios
Density > 60% of BALL_AREA
| BALL_RADIUS   | BALL_AREA |
| --------------|-----------|
| N/A           | N/A       |
| N/A           | N/A       |
| N/A           | N/A       |
| N/A           | N/A       |
| N/A           | N/A       |
| N/A           | N/A       |


##### Testing a flat circle object on a black canvas:
max density to display 1(2?) objects
| BALL_RADIUS   | DENSITY   |Theoretical Max Density?|
| --------------|-----------|------------------------|
| 3             | 11        |7^2 * k                 |
| 4             | 27        |9^2 * k                 |
| 5             | 47        |11^2 * k                |

Where k is a constant of proportionality of a circle
inside a square (adjusted for discrete circle)
