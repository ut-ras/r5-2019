#ifndef PID_H
#define PID_H
#include <fstream>

class PID {
    double goal;
    double last;
    double sum;
    double kP;
    double kI;
    double kD;
    std::ofstream logFile;
public:
    PID(double p, double i, double d): kP(p), kI(i), kD(d) {
        set(0);
    }
    PID(double p, double i, double d, std::string logName);
    ~PID();
    void set(double setPoint);
    double update(double current, double dt); // dt in seconds
    double getErr() {
        return last;
    }
};

#endif
