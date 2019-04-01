#include <Python.h>
#include <pigpio.h>
#include <iostream>
#include "pb-HAL/inc/motor.h"
#include "pb-HAL/inc/pid.h"

using namespace std;
enum VALID_STATES{TURN_RIGHT, DRIVE_FORWARD, TURN_LEFT, DRIVE_BACKWARD};
//const double TIME_PER_DEGREE = 0.01; // need to be calculated
const int CLAW = 14;
const int ELEVATOR = 18;
Motor* motors[2];

static PyObject* RobotInit(PyObject* self, PyObject* args){
    while(gpioInitialise() < 0);
    //motors[3] = new DRV(15, 14, 17, 18);
    //motors[2] = new DRV(25, 8, 7, 1);
    gpioSetMode(CLAW, PI_OUTPUT);
    gpioSetMode(ELEVATOR, PI_OUTPUT);
    motors[1] = new DRV(13, 22, 1, 8);
    motors[0] = new DRV(6, 27, 7, 25);
    return Py_BuildValue("i", 1);
}

static PyObject* RobotControl(PyObject *self, PyObject *args) { //Pass in RobotState
    PyObject* DriveState;
    PyArg_ParseTuple(args, "O", &DriveState);
    PyObject* pyDriveState = PyObject_GetAttrString(DriveState, "drive_state");
    PyObject* pyElevator =  PyObject_GetAttrString(DriveState, "elevator_state");
    PyObject* pyClaw = PyObject_GetAttrString(DriveState, "claw_state");
    PyObject* pyMagnitude = PyObject_GetAttrString(DriveState, "drive_magnitude");
    int driveState;
    bool elevator, claw;
    float magnitude;
    driveState = (int)PyLong_AsLong(pyDriveState);
    elevator = PyObject_IsTrue(pyElevator);
    claw = PyObject_IsTrue(pyClaw);
    magnitude = (float)PyFloat_AsDouble(pyMagnitude);
    int tick1, tick2;
    bool stopped1, stopped2;

    switch(driveState){
        case TURN_RIGHT:
            tick1 = motors[0]->getTicks();
            tick2 = motors[1]->getTicks();
            motors[0]->set(-0.2);
            motors[1]->set(0.4);
            stopped1 = false;
            stopped2 = false;
            while(abs(motors[0]->getTicks() - tick1) < 1.6*magnitude || abs(motors[1]->getTicks() - tick2) < 1.6*magnitude){
                cout << abs(motors[0]->getTicks() - tick1) << " " << abs(motors[1]->getTicks() - tick2) << endl;
                if(!stopped1 && abs(motors[0]->getTicks() - tick1) >= 1.6*magnitude){
                    motors[0]->stop();
                    stopped1 = true;
                    motors[1]->set(0.5);
                }
                if(!stopped2 && abs(motors[1]->getTicks() - tick2) >= 1.6*magnitude){
                    motors[1]->stop();
                    stopped2 = true;
                    motors[0]->set(-0.25);
                }
            }
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
            tick1 = motors[0]->getTicks();
            tick2 = motors[1]->getTicks();
            motors[0]->set(0.4);
            motors[1]->set(-0.2);
            stopped1 = false;
            stopped2 = false;
            while(abs(motors[0]->getTicks() - tick1) < 1.6*magnitude || abs(motors[1]->getTicks() - tick2) < 1.6*magnitude){
                cout << abs(motors[0]->getTicks() - tick1) << " " << abs(motors[1]->getTicks() - tick2) << endl;
                if(!stopped1 && abs(motors[0]->getTicks() - tick1) >= 1.6*magnitude){
                    motors[0]->stop();
                    stopped1 = true;
                    motors[1]->set(-0.25);
                }
                if(!stopped2 && abs(motors[1]->getTicks() - tick2) >= 1.6*magnitude){
                    motors[1]->stop();
                    stopped2 = true;
                    motors[0]->set(0.5);
                }
            }
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
        gpioServo(CLAW, 2500);
        //time_sleep(0.5);
    }
    else{
        gpioServo(CLAW, 500);
        //time_sleep(0.5);
    }

    if(elevator == 1){
        gpioServo(ELEVATOR, 2500);
        //time_sleep(0.5);
    }
    else{
        gpioServo(ELEVATOR, 500);
        //time_sleep(0.5);
    }   
    return Py_BuildValue("i", 1);
}

static PyMethodDef regVmethods[] = {
    {"RobotInit", (PyCFunction)RobotInit, METH_VARARGS, NULL},
    {"RobotControl", (PyCFunction)RobotControl, METH_VARARGS, NULL}
};

static struct PyModuleDef regVmodule = {
    PyModuleDef_HEAD_INIT,
    "regV",
    NULL,
    -1,
    regVmethods
};

PyMODINIT_FUNC PyInit_regV(void) {
    return PyModule_Create(&regVmodule);
    //Py_InitModule3("regV", regVmethods,
     //             "");
}

int main(int argc, char* argv[]) {
    wchar_t* program = Py_DecodeLocale(argv[0], NULL);
    if (program == NULL) {
        fprintf(stderr, "RIP");
        exit(1);
    }
    PyImport_AppendInittab("regV", PyInit_regV);
    Py_SetProgramName(program);
    Py_Initialize();
    PyImport_ImportModule("regV");
    PyMem_RawFree(program);
    return 0;
}
