#include <stdlib.h>
#include <algorithm>
#include "../inc/pid.h"

#define MAX_SPEED (.4)
#define MAX_SUM (1000)

PID::PID(double p, double i, double d, std::string logName) : kP(p), kI(i),
    kD(d) {
    set(0);
    logFile.open(logName.c_str(),
                 std::fstream::app); // change to "out" to overwrite
}

void PID::set(double set) {
    goal = set;
    sum = 0;
    last = 0;
    if(logFile.is_open()) {
        logFile << std::endl << "Set: " << set << " P: " << kP << " I: "
                << kI << " D: " << kD << std::endl;
    }
}

double PID::update(double current, double dt) {
    double err = goal - current;
    double d = (err - last) / dt;
    sum += err * dt;
    // sum = std::min(std::max(controller->sum, -MAX_SUM), MAX_SUM);
    last = err;
    double result = kP * err + kI * sum + kD * d;
    if(logFile.is_open()) {
        logFile << dt << " " << kP* err << " " << kI* sum << " " << kD* d
                << " " << result << std::endl;
    }
    return result;
}

PID::~PID() {
    if(logFile.is_open()) {
        logFile.close();
    }
}

