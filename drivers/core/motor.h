#ifndef MOTOR_H
#define MOTOR_H
#include "enc.h"

class Motor {
protected:
    Enc enc;
public:
    Motor(int encA, int encB) : enc(encA, encB) {};
    virtual void set(double speed) = 0; // Speed is in range [-1,1]
    virtual void stop() = 0;
    int getTicks() const {
        return enc.pos;
    }
    void zero() {
        enc.pos = 0;
    }
};

class L298N: public Motor {
    int m1;
    int m2;
    int pwm;
public:
    L298N(int m1pin, int m2pin, int pwmpin, int encA, int encB);
    ~L298N(); // Calls stop
    void set(double speed);
    void stop();
};

class DRV: public Motor {
    int pwm1;
    int pwm2;
public:
    DRV(int pwmpin1, int pwmpin2, int encA, int encB);
    ~DRV(); // Calls stop
    void set(double speed);
    void stop();
};
#endif
