/*
    main.cpp
    allows for robot initialization and turning RobotStates from control algorithm into robot actions
    Authors: Tony Li, Stefan deBruyn

*/


#include <Python.h>
#include <pigpio.h>
#include <iostream>
#include <chrono>
#include "pb-HAL/inc/motor.h"
#include "pid.h"
#include <sstream>

using namespace std;
enum VALID_STATES{TURN, DRIVE};
const int CLAW = 14;                //GPIO pins for servos
const int CAMERA = 15;              
const int ELEVATOR = 18;            
Motor* motors[2];
//time_t timer;


/*
    returns current time in milliseconds
*/
double time(){      
    chrono::milliseconds ms = chrono::duration_cast<chrono::milliseconds>(chrono::system_clock::now().time_since_epoch());
    return ms.count() / 1000.0;
}


/*
    updates velocity of motor according to pid control and target velocity
*//
void control(Motor* motor, PidController* pid, double targetvel, double* currvel, double time){
    double update = pid->update(targetvel - *currvel, time);
    *currvel = *currvel + update;
    if(*currvel > 1)
        motor->set(1);
    else if (*currvel < -1)
        motor->set(-1);
    else
        motor->set(*currvel);
}


/*
    Initializes motors and servos, should be called at startup
*/
static PyObject* RobotInit(PyObject* self, PyObject* args){
    while(gpioInitialise() < 0);
    //motors[3] = new DRV(15, 14, 17, 18);
    //motors[2] = new DRV(25, 8, 7, 1);
    gpioSetMode(CLAW, PI_OUTPUT);
    gpioSetMode(ELEVATOR, PI_OUTPUT);
    gpioSetMode(CAMERA, PI_OUTPUT);
    motors[1] = new DRV(13, 22, 1, 8);
    motors[0] = new DRV(6, 27, 25, 7);

    //time(&timer);
    return Py_BuildValue("i", 1);
}

/*
    Takes in Robot State with
    drive_state: TURN or DRIVE
    drive_velocity: double representing angle to turn or how far to travel in mm
    elevator_state: boolean with true being elevator lifted and false being set down
    claw_state: boolean with true being claw closed and false being claw open
    camera_state: boolean with true being camera laid down and false being camera upright

    and performs action until target is reached (until drive reaches its desired magnitude)
*/
static PyObject* RobotControl(PyObject *self, PyObject *args) { //Pass in RobotState
    PyObject* RobotState;
    PyArg_ParseTuple(args, "O", &RobotState);
    PyObject* pyDriveState = PyObject_GetAttrString(RobotState, "drive_state");         //retrieve all attributes from Python object
    PyObject* pyMagnitude = PyObject_GetAttrString(RobotState, "drive_velocity");
    PyObject* pyElevator =  PyObject_GetAttrString(RobotState, "elevator_state");
    PyObject* pyClaw = PyObject_GetAttrString(RobotState, "claw_state");
    PyObject* pyCamera = PyObject_GetAttrString(RobotState, "camera_state");
    
    int driveState;
    bool elevator, claw, camera;
    float magnitude;
    driveState = (int)PyLong_AsLong(pyDriveState);              //turn all attributes into cpp variables
    elevator = PyObject_IsTrue(pyElevator);
    claw = PyObject_IsTrue(pyClaw);
    camera = PyObject_IsTrue(pyCamera);
    magnitude = (float)PyFloat_AsDouble(pyMagnitude);
    int tick1, tick2, it;
    bool stopped1, stopped2;
    int target;
    double speeds[2], time_start, time_last, timer, dt_target;
    int target1, target2;               
    int diff1, diff2, currt1, currt2, last1, last2;
    double vel1, vel2;      
    
    switch(driveState){
        case TURN:
        {
            tick1 = motors[0]->getTicks();
            tick2 = motors[1]->getTicks();
            if(magnitude < 0){              //set target velocities based on whether angle is positive or negative
                target1 = -100;
                target2 = 100;
            }
            else{
                target1 = 100;
                target2 = -100;
            }
            for(int i = 0; i < 2; i++){
                speeds[i] = 0;
            }
            stopped1 = false;
            stopped2 = false;
            it = 0;
            PidController tctrl1 = PidController(0.0000001, 0, 0);
            PidController tctrl2 = PidController(0.0000001, 0, 0);
            time_start = time();
            time_last = 0;
            //motors[0]->set(0.1);
            //motors[1]->set(-0.05);
            do{ 
                cout << motors[0]->getTicks() << " " << motors[1]->getTicks() << endl;
                timer = time() - time_start;                                               
                double dt = timer - time_last;              //dt = time since last pid update
                if (dt >= dt_target) {
                    
                    currt1 = motors[0]->getTicks();
                    currt2 = motors[1]->getTicks();
                    diff1 = abs(currt1 - tick1);
                    diff2 = abs(currt2 - tick2);
                    if(it != 0){                            //skip on first iteration

                        vel1 = (currt1 - last1)/dt;
                        vel2 = (currt2 - last2)/dt;

                        cout << vel1 << " " << vel2 << endl;

                        control(motors[0], &tctrl1, target1, &speeds[0], timer);
                        control(motors[1], &tctrl2, target2, &speeds[1], timer);

                    }
                    last1 = currt1;
                    last2 = currt2;
                    it++;
                    time_last = timer;
                }
                if(!stopped1 && diff1 >= 2.12*abs(magnitude)){          //stop motor 1 if it reaches its goal
                        motors[0]->stop();
                        stopped1 = true;
                        gpioWrite(11, 1);
                    }
                if(!stopped2 && diff2 >= 2.12*abs(magnitude)){          //stop motor 2 if it reaches its goal
                    motors[1]->stop();
                    stopped2 = true;
                    gpioWrite(19, 1);
                }
            } while(diff1 < 2.12*abs(magnitude) || diff2 < 2.12*abs(magnitude));
            cout << "diff " << diff1 << " " << diff2 << endl;
            for(int i = 0; i < 2; i++){
                motors[i]->stop();
            } 
        break;
        }
        case DRIVE:{
            tick1 = motors[0]->getTicks();
            tick2 = motors[1]->getTicks();
            for(int i = 0; i < 2; i++){
                speeds[i] = 0;
            }

            gpioSetMode(11, PI_OUTPUT);
            gpioSetMode(19, PI_OUTPUT);
            gpioSetMode(26, PI_OUTPUT);
            gpioWrite(11, 0);
            gpioWrite(19, 0);
            gpioWrite(26, 0);
            it = 0;
            // PidController ctrl1 = PidController(0.0001, 0, 0.000001);
            // PidController ctrl2 = PidController(0.0001, 0, 0.000001);
            PidController ctrl1 = PidController(0.0001, 0.00000000, 0.00001);
            PidController ctrl2 = PidController(0.0001, 0.00000000, 0.00001);

            if(magnitude > 0) target = 75;  //target velocity :ticks per second
            else target = -100;
            dt_target = 0.1;
            double buf[100];
            stringstream stream;
            time_start = time();
            time_last = 0;
            for(int i = 0; i < 100; i++)
                buf[i] = 69;
            do{ 
                timer = time() - time_start;
                double dt = timer - time_last;              //dt = time since last pid update
                if (dt >= dt_target) {
                    //cout << timer << endl;
                    currt1 = motors[0]->getTicks();
                    currt2 = motors[1]->getTicks();
                    diff1 = abs(currt1 - tick1);
                    diff2 = abs(currt2 - tick2);
                    if(it != 0){                            //skip on first iteration
                        vel1 = (currt1 - last1)/dt;
                        vel2 = (currt2 - last2)/dt;
                        //buf[it%100] = vel1;
                        stream << vel1 << " " << vel2 << endl;

                        control(motors[0], &ctrl1, target, &speeds[0], timer);
                        control(motors[1], &ctrl2, target, &speeds[1], timer);

                    }
                    
                    last1 = currt1;
                    last2 = currt2;
                    it++;
                    time_last = timer;
                    if(!stopped1 && diff1 >= 2.5*abs(magnitude)){       //stop motor 1 if it reaches its goal
                        motors[0]->stop();
                        //target = 0;
                        stopped1 = true;
                        gpioWrite(11, 1);
                    }
                    if(!stopped2 && diff2 >= 2.5*abs(magnitude)){       //stop motor 2 if it reaches its goal
                        motors[1]->stop();
                        //target = 0;
                        stopped2 = true;
                        gpioWrite(19, 1);
                    }
                }
                
            } while(diff1 < 2.5*abs(magnitude) || diff2 < 2.5*abs(magnitude));
            //cout << diff1 << " " << diff2 << endl;
            gpioWrite(26, 1);
            for(int i = 0; i < 2; i++){
                motors[i]->stop();
            } 
            cout << "too" << diff1 << " " << diff2 << endl;
            cout << stream.str();
            // for(int i = 0; i < 100; i++)
            //     cout << buf[i] << endl;
            // cout << "it " << it << endl;
            
        break;
        }

    }

    claw == 1 ? gpioServo(CLAW, 600) : gpioServo(CLAW, 1000); //true, claw closed, false, claw opened
    elevator == 1 ? gpioServo(ELEVATOR, 2500) : gpioServo(ELEVATOR, 500); //true, elevator lifted, false, elevator lowered
    camera == 1 ? gpioServo(CAMERA, 750) : gpioServo(CAMERA, 1500); //true, camera down, false, camera up
    
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
