#include <pigpio.h>
#include <iostream>
#include "motor.h"
#include "pid.h"

using namespace std;
enum VALID_STATES{TURN_RIGHT, DRIVE_FORWARD, TURN_LEFT, DRIVE_BACKWARD};
const int TIME_PER_DEGREE = 0; // need to be calculated

/*void MotorControl(DrivetrainState command){
    switch(command.state){
        case TURN_RIGHT:
            motors[0]->set(-0.5);
            motors[1]->set(0.5);
            time_sleep(TIME_PER_DEGREE * magnitude);
            for(int i = 0; i < 2; i++){
                motors[i]->stop();
            }
        break;
        case DRIVE_FORWARD:
            for(int i = 0; i < 2; i++){
                motors[i]->set(command.magnitude);
            }
        break;
        case TURN_LEFT:
            motors[0]->set(0.5);
            motors[1]->set(-0.5);
            time_sleep(TIME_PER_DEGREE * magnitude);
            for(int i = 0; i < 2; i++){
                motors[i]->stop();
            }

        break;
        case DRIVE_BACKWARD:
            for(int i = 0; i < 2; i++){
                motors[i]->set(-command.magnitude);
            }
        break;
    }
}*/

int main2(void){
    //motors[3] = new DRV(15, 14, 17, 18);
    //motors[2] = new DRV(25, 8, 7, 1);
    //motors[1] = new DRV(27, 22, 10, 9);
    while(gpioInitialise() < 0);
    Motor* motors[4];
    motors[0] = new DRV(6, 13, 5, 0);
    cout << "Motors initialized" << endl;
    //for(int i = 0; i < 4; ++i) {
    //    linearControl[i] = new PID(.01, .01, .00003);            //configs borrowed from pacbot
    //}
    //for(int i = 0; i < 4; ++i) {
        for(double speed = -1; speed <= 1; speed += 0.25){
            motors[0]->set(speed);
            time_sleep(1);
            cout << motors[0]->getTicks() << endl;
            motors[0]->stop();
        }
    //}
}
int main(void){
    while(gpioInitialise() < 0);
    gpioSetMode(18, PI_OUTPUT);
    for(int i = 500; i <= 2500; i += 100){
        gpioServo(18, i);
        cout << gpioGetServoPulsewidth(18) << endl;
        time_sleep(0.5);
    }
}