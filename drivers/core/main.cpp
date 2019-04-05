/*
    main.cpp
    Primary driver class for a collector robot. Turns Python RobotStates into
    physical robot actions.
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

const int TURN_INSTRUCTION = 0;
const int DRIVE_INSTRUCTION = 1;

const int CLAW_PIN = 14;
const int CAMERA_PIN = 15;
const int ELEVATOR_PIN = 18;

const float DRIVE_SPURT = 5;
const float TURN_SPURT = 3.14159;

double time(){
    chrono::milliseconds ms = chrono::duration_cast<chrono::milliseconds>(chrono::system_clock::now().time_since_epoch());
    return ms.count() / 1000.0;
}

class RobotMind {
protected:
    const float DRIVE_VELOCITY = 200;
    const float TURN_VELOCITY = 100;
    const float CM_TICK_RATIO = 3.5 * 3.14159 / 300;
    const float TRACK_WIDTH = 9.5;
    const float CONTROL_FREQUENCY = 0.1;

    const int PID_MODE_DRIVE = 0;
    const int PID_MODE_TURN = 1;

    Motor *motor_alpha, *motor_beta;
    PidController *pid_drive_alpha, *pid_drive_beta;
    PidController *pid_turn_alpha, *pid_turn_beta;
    PidController *pid_alpha, *pid_beta;

    double time_last;
    float target_velocity_alpha, target_velocity_beta;
    float velocity_target_alpha, velocity_target_beta;
    float velocity_alpha, velocity_beta;
    float power_alpha, power_beta;
    int ticker_last_alpha, ticker_last_beta;

    int sign(float f) {
        return f < 0 ? -1 : (f > 0 ? 1 : 0);
    }

    float clamp(float f, float low, float high) {
        return f < low ? low : (f > high ? high : f);
    }

    void set_pid_mode(int mode) {
        if (mode == PID_MODE_DRIVE) {
            pid_alpha = pid_drive_alpha;
            pid_beta = pid_drive_beta;
        } else if (mode == PID_MODE_TURN) {
            pid_alpha = pid_turn_alpha;
            pid_beta = pid_turn_beta;
        }

        pid_alpha->clear();
        pid_beta->clear();
    }

public:
    RobotMind() {
        cout << "Creating RobotMind..." << endl;

        gpioSetMode(CLAW_PIN, PI_OUTPUT);
        gpioSetMode(ELEVATOR_PIN, PI_OUTPUT);
        gpioSetMode(CAMERA_PIN, PI_OUTPUT);

        pid_drive_alpha = new PidController(0.0001, 0, 0.00001);
        pid_drive_beta = pid_drive_alpha->clone();

        pid_turn_alpha = new PidController(0.00075, 0, 0.0001);
        pid_turn_beta = pid_turn_alpha->clone();

        motor_alpha = new DRV(6, 27, 7, 25);
        motor_beta = new DRV(13, 22, 8, 1);

        cout << "Robot online" << endl;
    }

    ~RobotMind() {
        delete motor_alpha;
        delete motor_beta;

        delete pid_drive_alpha;
        delete pid_drive_beta;
        delete pid_turn_alpha;
        delete pid_turn_beta;
    }

    float drive(float cm) {
        double epoch = time();

        ticker_last_alpha = ticker_last_beta = -1;
        power_alpha = power_beta = 0;
        time_last = 0;

        int ticker_init_alpha = motor_alpha->getTicks();
        int ticker_init_beta = motor_beta->getTicks();

        int displacement_ticks = (int)(cm / CM_TICK_RATIO);

        int ticker_target_alpha = ticker_init_alpha + displacement_ticks;
        int ticker_target_beta = ticker_init_beta + displacement_ticks;

        int direction_alpha = sign(ticker_target_alpha - ticker_init_alpha);
        int direction_beta = sign(ticker_target_beta - ticker_init_beta);

        velocity_target_alpha = DRIVE_VELOCITY * direction_alpha;
        velocity_target_beta = DRIVE_VELOCITY * direction_beta;

        set_pid_mode(PID_MODE_DRIVE);

        bool done = false;

        do {
            double time_current = time() - epoch;
            double dt = time_current - time_last;

            if (dt >= CONTROL_FREQUENCY) {
                int ticker_alpha = motor_alpha->getTicks();
                int ticker_beta = motor_beta->getTicks();

                int direction_now_alpha = sign(ticker_target_alpha - ticker_alpha);
                int direction_now_beta = sign(ticker_target_beta - ticker_beta);

                if (direction_now_alpha != direction_alpha || direction_now_beta != direction_beta)
                    done = true;
                else
                    control(ticker_alpha, ticker_beta, time_current);

                time_last = time_current;
            }

        } while (!done);

        stop();

        return (ticker_target_alpha - ticker_init_alpha) * CM_TICK_RATIO;
    }

    float turn(float rad) {
        double epoch = time();
        ticker_last_alpha = ticker_last_beta = -1;
        power_alpha = power_beta = 0;
        time_last = 0;

        int direction = sign(rad);
        velocity_target_alpha = TURN_VELOCITY * -direction;
        velocity_target_beta = TURN_VELOCITY * direction;

        set_pid_mode(PID_MODE_TURN);

        float turn_arc = 0;
        bool done = false;

        do {
            double time_current = time() - epoch;
            double dt = time_current - time_last;

            if (dt >= CONTROL_FREQUENCY) {
                int ticker_alpha = motor_alpha->getTicks();
                int ticker_beta = motor_beta->getTicks();

                control(ticker_alpha, ticker_beta, time_current);

                turn_arc += (-velocity_alpha + velocity_beta) / TRACK_WIDTH * dt * CM_TICK_RATIO;
                time_last = time_current;

                if (sign(rad - turn_arc) != direction)
                    done = true;
            }

        } while (!done);

        stop();

        return turn_arc;
    }

    void stop() {
        motor_alpha->stop();
        motor_beta->stop();
    }

    void control(int ticker_alpha, int ticker_beta, double t) {
        if (ticker_last_alpha != -1) {
            double dt = t - time_last;

            int d_ticker_alpha = ticker_alpha - ticker_last_alpha;
            int d_ticker_beta = ticker_beta - ticker_last_beta;

            velocity_alpha = d_ticker_alpha / dt;
            velocity_beta = d_ticker_beta / dt;

            float update_alpha = pid_alpha->update(velocity_target_alpha - velocity_alpha, t);
            float update_beta = pid_beta->update(velocity_target_beta - velocity_beta, t);

            power_alpha = clamp(power_alpha + update_alpha, -1, 1);
            power_beta = clamp(power_beta + update_beta, -1, 1);

            motor_alpha->set(power_alpha);
            motor_beta->set(power_beta);
        }

        ticker_last_alpha = ticker_alpha;
        ticker_last_beta = ticker_beta;
    }

    void set_claw(int toggle) {
        toggle == 1 ? gpioServo(CLAW_PIN, 600) : gpioServo(CLAW_PIN, 1000);
    }

    void set_elevator(int toggle) {
        toggle == 1 ? gpioServo(ELEVATOR_PIN, 2500) : gpioServo(ELEVATOR_PIN, 500);
    }

    void set_camera(int toggle) {
        toggle == 1 ? gpioServo(CAMERA_PIN, 750) : gpioServo(CAMERA_PIN, 1500);
    }
};

static RobotMind *robot_mind = nullptr;

/*
    updates velocity of motor according to pid control and target velocity
*/
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

    robot_mind = new RobotMind();

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
static PyObject* RobotControl(PyObject *self, PyObject *args) {
    PyObject* state;
    PyArg_ParseTuple(args, "O", &state);
    PyObject* py_drive_state = PyObject_GetAttrString(state, "drive_state");
    PyObject* py_velocity = PyObject_GetAttrString(state, "drive_velocity");
    PyObject* py_elevator =  PyObject_GetAttrString(state, "elevator_state");
    PyObject* py_claw = PyObject_GetAttrString(state, "claw_state");
    PyObject* py_camera = PyObject_GetAttrString(state, "camera_state");

    int drive_state = (int)PyLong_AsLong(py_drive_state);
    float magnitude = (float)PyFloat_AsDouble(py_velocity);
    bool elevator = PyObject_IsTrue(py_elevator);
    bool claw = PyObject_IsTrue(py_claw);
    bool camera = PyObject_IsTrue(py_camera);

    float return_value;

    if (drive_state == DRIVE_INSTRUCTION)
        return_value = robot_mind->drive(magnitude);
    else if (drive_state == TURN_INSTRUCTION)
        return_value = robot_mind->turn(magnitude);

    robot_mind->set_elevator(elevator);
    robot_mind->set_claw(claw);
    robot_mind->set_camera(camera);

    return Py_BuildValue("f", return_value);
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
