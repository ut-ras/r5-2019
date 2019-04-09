"""IO Definitions

Attributes
----------
LED1
    Finishing light
LED2, LED3, LED4
    General Purpose debug LEDs
RST
    Reset button
ESTOP
    Emergency stop
GP2
    General Purpose button BUT2
GP3
    General Purpose button BUT3
"""

import gpiozero


# LEDs
LED1 = gpiozero.LED(11)
LED2 = gpiozero.LED(0)
LED3 = gpiozero.LED(19)
LED4 = gpiozero.LED(26)


# Buttons
RST = gpiozero.Button(12)
ESTOP = gpiozero.Button(21)
GP2 = gpiozero.Button(16)
GP3 = gpiozero.Button(20)
