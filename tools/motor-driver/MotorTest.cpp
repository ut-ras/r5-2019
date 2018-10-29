#include "../DRV8833/DRV8833.h"
// Motor steps per revolution. Most steppers are 200 steps or 1.8 degrees/step
#define MOTOR_STEPS 200
#define RPM 120
#define MICROSTEPS 16
#define DIR 8
#define STEP 9
#include "DRV8834.h"
#define M0 10
#define M1 11
#define MOTOR_ACCEL 2000
#define MOTOR_DECEL 1000

const int inputA1 = 5, inputA2 = 6, inputB1 = 9, inputB2 = 10;

DRV8834 stepper(MOTOR_STEPS, DIR, STEP, M0, M1);
DRV8834 dcmotor;

//DRV8834 test main
int main(void){
	//test basic rotations based on degrees
    stepper.begin(10, MICROSTEPS);
    stepper.enable();
    stepper.rotate(180);
    delay(1000);
    stepper.rotate(360);
    delay(1000);
    stepper.rotate(-180);
    delay(1000);
    stepper.stop();
    //test rotation based on speed profile
    stepper.setRPM(RPM);
    stepper.setSpeedProfile(stepper.LINEAR_SPEED, MOTOR_ACCEL, MOTOR_DECEL);
    stepper.startRotate(360);
    delay(1000);

    //test different microstep settings (1 is 1 microstep per step, 32 is 32 microsteps per step)
    stepper.setRPM(10);
    stepper.setMicrostep(1);
    stepper.rotate(360);     
    stepper.move(MOTOR_STEPS);    // forward revolution
    stepper.move(-MOTOR_STEPS);   // reverse revolution
    delay(5000);

	stepper.setMicrostep(8);
    stepper.move(4 * MOTOR_STEPS);    // forward revolution
    stepper.move(-2 * MOTOR_STEPS);   // reverse revolution
    delay(5000);

	stepper.setMicrostep(32);
    stepper.move(16 * MOTOR_STEPS);    // forward revolution
    stepper.move(-16 * MOTOR_STEPS);   // reverse revolution
    delay(5000);    
}
//DRV8833 test main
int main2(void){
	dcmotor.attachMotorA(inputA1, inputA2);
	dcmotor.attachMotorB(inputB1, inputB2);
	int speed;
	delay(1000);
	for(int i = 0; i <= 2; i++){
		speed = 255;
		for(int k = i; k > 0; k--){
			speed = speed/2;
		}
		dcmotor.motorAForward(speed);
		dcmotor.motorBForward(speed);
		delay(1000);
		dcmotor.motorAReverse(motorSpeed);
		dcmotor.motorBReverse(motorSpeed);
		delay(1000);
	}
	dcmotor.motorAStop();
	dcmotor.motorBStop();
	delay(1000);
}