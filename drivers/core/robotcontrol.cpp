#include <Python.h>
#include <pigpio.h>
#include <iostream>
#include "motor.h"
#include "pid.h"

using namespace std;
enum VALID_STATES{TURN_RIGHT, DRIVE_FORWARD, TURN_LEFT, DRIVE_BACKWARD};
const int TIME_PER_DEGREE = 1; // need to be calculated
Motor* motors[4];

static PyObject* RobotInit(PyObject* self, PyObject* args){
    while(gpioInitialise() < 0);
    //motors[3] = new DRV(15, 14, 17, 18);
    //motors[2] = new DRV(25, 8, 7, 1);
    motors[1] = new DRV(27, 22, 10, 9);
    motors[0] = new DRV(6, 13, 5, 0);
    return Py_BuildValue("i", 1);
}

static PyObject* RobotControl(PyObject *self, PyObject *args) { //Pass in RobotState
    PyObject* DriveState;
    PyArg_ParseTuple(args, "O", &DriveState);
    PyObject* pyDriveState = PyObject_GetAttrString(DriveState, "drive_state");
    PyObject* pyElevator =  PyObject_GetAttrString(DriveState, "elevator_state");
    PyObject* pyClaw = PyObject_GetAttrString(DriveState, "claw_state");
    PyObject* pyMagnitude = PyObject_GetAttrString(DriveState, "drive_magnitude");
    /*int driveState;
    bool elevator, claw;
    float magnitude;
    driveState = (int)PyLong_AsLong(pyDriveState);
    elevator = PyObject_IsTrue(pyElevator);
    claw = PyObject_IsTrue(pyClaw);
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
    return Py_BuildValue("i", 1);*/
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
