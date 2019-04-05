#include <pigpio.h>
#include "../inc/enc.h"

void _cb(int gpio, int level, uint32_t tick, void* user) {
    Enc* enc = (Enc*)user;
    if (gpio == enc->encA) {
        enc->levA = level;
    } else {
        enc->levB = level;
    }
    if (gpio != enc->lastGpio) { // Debounce
        enc->lastGpio = gpio;
        if ((gpio == enc->encA) && (level == 1)) {
            if (enc->levB) {
                ++enc->pos;
            }
        } else if ((gpio == enc->encB) && (level == 1)) {
            if (enc->levA) {
                --enc->pos;
            }
        }
    }
}

Enc::Enc(int apin, int bpin) {
    encA = apin;
    encB = bpin;
    levA = 0;
    levB = 0;
    pos = 0;
    lastGpio = -1;
    gpioSetMode(apin, PI_INPUT);
    gpioSetMode(bpin, PI_INPUT);
    gpioSetPullUpDown(apin, PI_PUD_UP);
    gpioSetPullUpDown(bpin, PI_PUD_UP);
    gpioSetAlertFuncEx(apin, _cb, this);
    gpioSetAlertFuncEx(bpin, _cb, this);
}

Enc::~Enc() {
    gpioSetAlertFunc(encA, 0);
    gpioSetAlertFunc(encB, 0);
}

