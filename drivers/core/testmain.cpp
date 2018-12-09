

int main(void){motors[3] = new DRV(15, 14, 17, 18);
    motors[2] = new DRV(25, 8, 7, 1);
    motors[1] = new DRV(27, 22, 10, 9);
    motors[0] = new DRV(6, 13, 5, 0);
    cout << "Motors initialized" << endl;
    for(int i = 0; i < 4; ++i) {
        linearControl[i] = new PID(.01, .01, .0003);
    }
    }
    