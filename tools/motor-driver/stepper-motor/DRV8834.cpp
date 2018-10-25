/*
 * DRV8834 - LV Stepper Motor Driver Driver (A4988-compatible - mostly)
 * Indexer mode only.

 * Copyright (C)2015 Laurentiu Badea
 *
 * This file may be redistributed under the terms of the MIT license.
 * A copy of this license has been included with this distribution in the file LICENSE.
 */
#include "DRV8834.h"
#include "GPIOClass.h"

/*
 * Basic connection: only DIR, STEP are connected.
 * Microstepping controls should be hardwired.
 */
DRV8834::DRV8834(short steps, short dir_pin, short step_pin)
:BasicStepperDriver(steps, dir_pin, step_pin)
{}

DRV8834::DRV8834(short steps, short dir_pin, short step_pin, short enable_pin)
:BasicStepperDriver(steps, dir_pin, step_pin, enable_pin)
{}

/*
 * Fully wired. All the necessary control pins for DRV8834 are connected.
 */
DRV8834::DRV8834(short steps, short dir_pin, short step_pin, short m0_pin, short m1_pin)
:BasicStepperDriver(steps, dir_pin, step_pin), m0_pin(m0_pin), m1_pin(m1_pin)
{}

DRV8834::DRV8834(short steps, short dir_pin, short step_pin, short enable_pin, short m0_pin, short m1_pin)
:BasicStepperDriver(steps, dir_pin, step_pin, enable_pin), m0_pin(m0_pin), m1_pin(m1_pin)
{}

/*
 * Set microstepping mode (1:divisor)
 * Allowed ranges for DRV8834 are 1:1 to 1:32
 * If the control pins are not connected, we recalculate the timing only
 *
 */
short DRV8834::setMicrostep(short microsteps){
    BasicStepperDriver::setMicrostep(microsteps);

    if (!IS_CONNECTED(m0_pin) || !IS_CONNECTED(m1_pin)){
        return this->microsteps;
    }

    /*
     * Step mode truth table
     * M1 M0    step mode
     *  0  0     1
     *  0  1     2
     *  0  Z     4
     *  1  0     8
     *  1  1    16
     *  1  Z    32
     *
     *  Z = high impedance mode (M0 is tri-state)
     */

    GPIOClass GPIOm1 (to_string(m1_pin));
    GPIOClass GPIOm0 (to_string(m0_pin));
    GPIOm1.export_gpio();
    GPIOm1.setdir_gpio("out");
    GPIOm1.setval_gpio((this->microsteps < 8) ? 0 : 1)

    switch(this->microsteps){
    case 1:
    case 8:
        GPIOm0.export_gpio();
        GPIOm0.setdir_gpio("out");
        GPIOm0.setval_gpio(0);
        break;
    case 2:
    case 16:
        GPIOm0.export_gpio();
        GPIOm0.setdir_gpio("out");
        GPIOm0.setval_gpio(1);
        break;
    case 4:
    case 32:
        GPIOm0.export_gpio();
        GPIOm0.setdir_gpio("in");
        break;
    }
    return this->microsteps;
}

short DRV8834::getMaxMicrostep(){
    return DRV8834::MAX_MICROSTEP;
}
