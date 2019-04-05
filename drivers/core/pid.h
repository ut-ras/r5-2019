#ifndef CONTROL_PID_H
#define CONTROL_PID_H

int get__sign(double d);

class PidController {
protected:
  const bool RESET_I = true;
  double kp, ki, kd;
  double errorLast, errorTotal, timeLast;

public:
  PidController(double kp, double ki, double kd);

  double update(double error, double time);

  PidController* clone();

  void clear();
};

#endif
