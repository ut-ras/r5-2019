#include <pigpio.h>
#include <iostream>
#include "../inc/motor.h"
#include "../inc/pid.h"

int main(void){
    motors[3] = new DRV(15, 14, 17, 18);
    motors[2] = new DRV(25, 8, 7, 1);
    motors[1] = new DRV(27, 22, 10, 9);
    motors[0] = new DRV(6, 13, 5, 0);
    cout << "Motors initialized" << endl;
    for(int i = 0; i < 4; ++i) {
        linearControl[i] = new PID(.01, .01, .0003);            //configs borrowed from pacbot
    }
    for(int i = 0; i < 4; ++i) {
        for(int i = -1; i <= 1; i += 0.25){
            motors[i]->set(i);
            time_sleep(1);
            motors[i]->stop();
        }
    }
}
int main2(void){
    gpioSetMode(18, PI_OUTPUT);
    for(int i = 0; i <= 2500; i += 500){
        gpioServo(18, i);
        cout << gpioGetServoPulsewidth(18);
        time_sleep(1);
    }
}