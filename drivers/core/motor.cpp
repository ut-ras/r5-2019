#include <pigpio.h>
#include <cmath>
#include "../inc/motor.h"

using namespace std;

const double DEADZONE = .05; // for speed not encoder ticks
const int FREQENCY = 440; // gotto make sure our motors are in tune

L298N::L298N(int m1pin, int m2pin, int pwmpin, int encA, int encB)
    : Motor(encA, encB), m1(m1pin), m2(m2pin), pwm(pwmpin) {
    gpioSetMode(m1, PI_OUTPUT);
    gpioSetMode(m2, PI_OUTPUT);
    gpioSetMode(pwm, PI_OUTPUT);
    gpioSetPWMfrequency(pwm, FREQENCY);   // lower freq gives lower min speed
    gpioSetPWMrange(pwm, 1000);      // not sure why we'd want a small range
}

void L298N::set(double speed) {
    if(speed > DEADZONE) {
        gpioWrite(m1, 1);
        gpioWrite(m2, 0);
    } else if(speed < -DEADZONE) {
        gpioWrite(m1, 0);
        gpioWrite(m2, 1);
    } else {
        gpioWrite(m1, 0);
        gpioWrite(m2, 0);
    }
    gpioPWM(pwm, abs(speed) * gpioGetPWMrange(pwm));
}

void L298N::stop() {
    set(0);
    gpioWrite(m1, 0);
    gpioWrite(m2, 0);
}

L298N::~L298N() {
    stop();
}

DRV::DRV(int pwmpin1, int pwmpin2, int encA, int encB)
    : Motor(encA, encB), pwm1(pwmpin1), pwm2(pwmpin2) {
    gpioSetMode(pwm1, PI_OUTPUT);
    gpioSetPWMfrequency(pwm1, 440);
    gpioSetPWMrange(pwm1, 1000);
    gpioSetMode(pwm2, PI_OUTPUT);
    gpioSetPWMfrequency(pwm2, 440);
    gpioSetPWMrange(pwm2, 1000);
}

void DRV::set(double speed) {
    double next1, next2;
    if(speed > DEADZONE) {
        next1 = pwm1;
        next2 = pwm2;
    } else if(speed < -DEADZONE) {
        next1 = pwm2;
        next2 = pwm1;
    } else {
        stop();
        return;
    }
    gpioPWM(next1, abs(speed) * gpioGetPWMrange(pwm1));
    gpioPWM(next2, 0);
}

void DRV::stop() {
    //todo: try 0's for sleep instead of break
    gpioWrite(pwm1, 0);
    gpioWrite(pwm2, 0);
}

DRV::~DRV() {
    stop();
}
