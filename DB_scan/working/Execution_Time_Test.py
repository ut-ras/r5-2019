import DB_SCAN3 as V3
import DB_SCAN4 as V4
import sys

# main
if __name__ == "__main__":
    MASK_NAME = sys.argv[1]
    BALL_RAD = int(sys.argv[2])
    DENSITY = int(sys.argv[3])
    OPTION = int(sys.argv[4])
    ITERATIONS = int(sys.argv[5])

    total_time = 0
    # test V3 10 times, return the avg and the set of results
    V3_times = []
    for test in range(ITERATIONS):
        print("Running...")
        run_time = V3.output_module(MASK_NAME, BALL_RAD, DENSITY, OPTION)
        V3_times.append(run_time)
        total_time = total_time + run_time

    print("Avg Time for V3 for {name} at r:{r}; d:{d} = {t}"
        .format(name=MASK_NAME,r=BALL_RAD, d=DENSITY, t=total_time/ITERATIONS))
    print(V3_times)

    total_time = 0
    # test V3 10 times, return the avg and the set of results
    V4_times = []
    for test in range(ITERATIONS):
        print("Running...")
        run_time = V4.output_module(MASK_NAME, BALL_RAD, DENSITY, OPTION)
        V4_times.append(run_time)
        total_time = total_time + run_time

    print("Avg Time for V4 for {name} at r:{r}; d:{d} = {t}"
        .format(name=MASK_NAME,r=BALL_RAD, d=DENSITY, t=total_time/ITERATIONS))
    print(V4_times)
