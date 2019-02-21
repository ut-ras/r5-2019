#include <pigpio.h>
#include <iostream>
#include "motor.h"
#include "pid.h"
#include <Python.h>

using namespace std;
enum VALID_STATES{TURN_RIGHT, DRIVE_FORWARD, TURN_LEFT, DRIVE_BACKWARD};
const int TIME_PER_DEGREE = 0; // need to be calculated

void RobotControl(PyObject* DriveState){ //Pass in RobotState
    PyObject* pyDriveState, pyElevator, pyClaw, pyMagnitude;
    pyDriveState = PyObject_GetAttrString(DriveState, "drive_state");
    pyElevator = PyObject_GetAttrString(DriveState, "elevator_state");
    pyClaw = PyObject_GetAttrString(DriveState, "claw_state");
    pyMagnitude = PyObject_GetAttrString(DriveState, "magnitude");
    int driveState, elevator, claw;
    float magnitude;
    driveState = (int)PyLong_AsLong(pyDriveState);
    elevator = PyBool_IsTrue(pyElevator);
    claw = PyBool_IsTrue(pyClaw);
    magnitude = (float)PyFloat_AsDouble(pyMagnitude);

    switch(driveState){
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
                motors[i]->set(magnitude);
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
                motors[i]->set(-magnitude);
            }
        break;
    }

    if(claw == 1){
        //engage claw
    }
    else{
        //disengage claw
    }

    if(elevator == 1){
        //raise elevator
    }
    else{
        //lower elevator
    }   
}