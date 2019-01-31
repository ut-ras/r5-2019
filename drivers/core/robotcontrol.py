class PID:
    """
    Simple feedforward PID controller.
    """

    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.t_last = None
        self.error_total = 0
        self.error_last = 0

    def update(self, t, error):
        """
        Fetches an update from the controller.

        Parameters
        ----------
        t: float
            Timestamp
        error: float
            Current system error

        Returns
        -------
        float
            Update
        """

        # D
        if self.t_last is None:
            upd = 0
        else:
            dt = t - self.t_last
            upd = self.kd * (error - self.error_last) / dt

        # P, I
        self.error_total += error
        upd += self.kp * error + self.ki * self.error_total
        self.error_last = error
        return upd
