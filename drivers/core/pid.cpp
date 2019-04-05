#include "pid.h"

int get__sign(double d) {
  return d < 0 ? -1 : (d > 0 ? 1 : 0);
}


PidController::PidController(double kp, double ki, double kd) {
  this->kp = kp;
  this->ki = ki;
  this->kd = kd;
  errorLast = errorTotal = timeLast = 0;
}

double PidController::update(double error, double time) {
  if (RESET_I && get__sign(error) != get__sign(errorLast))
    errorTotal = 0;

  double result = kp * error + ki * errorTotal;
  double dt = time - timeLast;

  if (dt != 0)
    result += kd * (error - errorLast) / dt;

  errorTotal += error;
  timeLast = time;
  errorLast = error;
  return result;
}

PidController* PidController::clone() {
    return new PidController(kp, ki, kd);
}

void PidController::clear() {
    errorLast = errorTotal = timeLast = 0;
}
