#include "../DRV8833/DRV8833.h"
// Motor steps per revolution. Most steppers are 200 steps or 1.8 degrees/step
#define MOTOR_STEPS 200
#define RPM 120

#define DIR 8
#define STEP 9

#include "DRV8834.h"
#define M0 10
#define M1 11
DRV8834 stepper(MOTOR_STEPS, DIR, STEP, M0, M1);

int main(void){
    stepper.begin(1, MICROSTEPS);
    stepper.enable();
    stepper.rotate(180);
    delay(1000);
    stepper.rotate(360);
    delay(1000);
    stepper.rotate(-180);
    delay(1000);
}sasas