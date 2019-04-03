#include <Python.h>
#include <pigpio.h>
#include <iostream>
#include "pb-HAL/inc/motor.h"
#include "pb-HAL/inc/pid.h"

using namespace std;
enum VALID_STATES{TURN, DRIVE};
const int CLAW = 14;
const int CAMERA = 15;
const int ELEVATOR = 18;
Motor* motors[2];

static PyObject* RobotInit(PyObject* self, PyObject* args){
    while(gpioInitialise() < 0);
    //motors[3] = new DRV(15, 14, 17, 18);
    //motors[2] = new DRV(25, 8, 7, 1);
    gpioSetMode(CLAW, PI_OUTPUT);
    gpioSetMode(ELEVATOR, PI_OUTPUT);
    gpioSetMode(CAMERA, PI_OUTPUT);
    motors[1] = new DRV(13, 22, 1, 8);
    motors[0] = new DRV(6, 27, 7, 25);
    return Py_BuildValue("i", 1);
}

static PyObject* RobotControl(PyObject *self, PyObject *args) { //Pass in RobotState
    PyObject* DriveState;
    PyArg_ParseTuple(args, "O", &DriveState);
    PyObject* pyDriveState = PyObject_GetAttrString(DriveState, "drive_state");
    PyObject* pyMagnitude = PyObject_GetAttrString(DriveState, "drive_velocity");
    PyObject* pyElevator =  PyObject_GetAttrString(DriveState, "elevator_state");
    PyObject* pyClaw = PyObject_GetAttrString(DriveState, "claw_state");
    PyObject* pyCamera = PyObject_GetAttrString(DriveState, "camera_state");
    
    int driveState;
    bool elevator, claw, camera;
    float magnitude;
    driveState = (int)PyLong_AsLong(pyDriveState);
    elevator = PyObject_IsTrue(pyElevator);
    claw = PyObject_IsTrue(pyClaw);
    camera = PyObject_IsTrue(pyCamera);
    magnitude = (float)PyFloat_AsDouble(pyMagnitude);
    int tick1, tick2;
    bool stopped1, stopped2;
    
    switch(driveState){
        case TURN:
            tick1 = motors[0]->getTicks();
            tick2 = motors[1]->getTicks();
            if(magnitude < 0){
                motors[0]->set(-0.2);
                motors[1]->set(0.4);
            }
            else{
                motors[0]->set(0.4);
                motors[1]->set(-0.2);
            }
            stopped1 = false;
            stopped2 = false;
            while(abs(motors[0]->getTicks() - tick1) < 1.6*abs(magnitude) || abs(motors[1]->getTicks() - tick2) < 1.6*abs(magnitude)){
                if(!stopped1 && abs(motors[0]->getTicks() - tick1) >= 1.6*abs(magnitude)){
                    motors[0]->stop();
                    stopped1 = true;
                }
                if(!stopped2 && abs(motors[1]->getTicks() - tick2) >= 1.6*abs(magnitude)){
                    motors[1]->stop();
                    stopped2 = true;
                }
            }
            for(int i = 0; i < 2; i++){
                motors[i]->stop();
            }
        break;
        case DRIVE:
            tick1 = motors[0]->getTicks();
            tick2 = motors[1]->getTicks();
            for(int i = 0; i < 2; i++){
                magnitude > 0 ? motors[i]->set(0.28) : motors[i]->set(-0.25);
            }
            //motors[0]->set(0.25);
            //motors[1]->set(0.25);
            int count = 0;
            gpioSetMode(11, PI_OUTPUT);
            gpioSetMode(19, PI_OUTPUT);
            gpioSetMode(26, PI_OUTPUT);
            gpioWrite(11, 0);
            gpioWrite(19, 0);
            while(abs(motors[0]->getTicks() - tick1) < 2.3*abs(magnitude) || abs(motors[1]->getTicks() - tick2) < 2.3*abs(magnitude)){
                if(++count > 20){
                    cout << abs(motors[0]->getTicks() - tick1) << " " << abs(motors[1]->getTicks() - tick2) << endl;
                    count = 0;
                }
                if(!stopped1 && abs(motors[0]->getTicks() - tick1) >= 2.3*abs(magnitude)){
                    motors[0]->stop();
                    stopped1 = true;
                    gpioWrite(11, 1);
                }
                if(!stopped2 && abs(motors[1]->getTicks() - tick2) >= 2.3*abs(magnitude)){
                    motors[1]->stop();
                    stopped2 = true;
                    gpioWrite(19, 1);
                }
            }
            gpioWrite(26, 1);
            for(int i = 0; i < 2; i++){
                motors[i]->stop();
            }
        break;

    }

    claw == 1 ? gpioServo(CLAW, 833) : gpioServo(CLAW, 500); //30
    elevator == 1 ? gpioServo(ELEVATOR, 2500) : gpioServo(ELEVATOR, 500); //180
    camera == 1 ? gpioServo(CAMERA, 750) : gpioServo(CAMERA, 1500); //90
    
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
