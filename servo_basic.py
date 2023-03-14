"""A CircuitPython program that controls a servo motor.

Description
-----------

A CircuitPython program that controls a servo motor.

Includes routines for demonstrating different ways you can control your servo.

Circuit
-------

- A servo motor's signal wire is connected to pin D5.

Libraries/Modules
-----------------

- *time* Standard Library
    - https://docs.python.org/3/library/time.html
    - Provides access to the *sleep* function.
- *board* CircuitPython Core Module
    - https://circuitpython.readthedocs.io/en/latest/shared-bindings/board/
    - Provides access to the board's GPIO pins and hardware.
- *pwmio* CircuitPython Core Module
    - https://docs.circuitpython.org/en/latest/shared-bindings/pwmio/
    - Provides support for pulse width modulation protocols.
- *Adafruit_CircuitPython_Motor* CircuitPython Helper Library
    - https://github.com/adafruit/Adafruit_CircuitPython_Motor
    - Provides support for controlling servo motors.

Notes
-----

- View printed output in the serial console.
- Comments are Sphinx (reStructuredText) compatible.

TODO
----

- None.

Author(s)
---------

- Created by John Woolsey on 02/18/2023.
- Modified by John Woolsey on 02/26/2023.

Copyright (c) 2023 Woolsey Workshop.  All rights reserved.

Members
-------
"""


# Imports
from time import sleep
import board
import pwmio
from adafruit_motor import servo


# Global Constants
DEBUG = True
"""The mode of operation; `False` = normal, `True` = debug."""

SERVO_A_0_DEGREES_PULSE_WIDTH = 1000
"""The 0 degrees pulse width in microseconds for servo A."""

SERVO_A_180_DEGREES_PULSE_WIDTH = 2000
"""The 180 degrees pulse width in microseconds for servo A."""


# Pin Mapping
servo_a_pin = pwmio.PWMOut(board.D5, frequency=50)
"""The pin connected to the signal wire of servo A."""


# Global Instances
# servo_a = servo.Servo(servo_a_pin)
# """The servo A instance.
# Connects and initializes servo A with the default actuation range (180) and minimum (750) and maximum (2250) pulse widths.
# """

# servo_a = servo.Servo(servo_a_pin, actuation_range=180, min_pulse=1000, max_pulse=2000)
# """The servo A instance.
# Connects and initializes servo A with a 180 degree actuation range and conservative minimum and maximum pulse widths.
# """

servo_a = servo.Servo(servo_a_pin, actuation_range=180, min_pulse=SERVO_A_0_DEGREES_PULSE_WIDTH, max_pulse=SERVO_A_180_DEGREES_PULSE_WIDTH)
"""The servo A instance.
Connects and initializes servo A with a 180 degree actuation range and the specified minimum and maximum pulse widths.
"""


# Functions
def basic_operations():
    """Demonstrates the basic operations of servo motors."""

    if DEBUG: print("Setting angle to 90 degrees.")
    servo_a.angle = 90   # center position
    sleep(5)
    if DEBUG: print("Setting angle to 0 degrees.")
    servo_a.angle = 0    # farthest position on one side
    sleep(5)
    if DEBUG: print("Setting angle to 90 degrees.")
    servo_a.angle = 90   # center position
    sleep(5)
    if DEBUG: print("Setting angle to 180 degrees.")
    servo_a.angle = 180  # farthest position on the other side
    sleep(5)


def servo_sweep(start_angle, stop_angle, step_angle=1, step_time=0.015):
    """Sweeps the servo from one position (angle) to another.

    Performs appropriate error checking of input values.

    Prints debugging information if DEBUG is set.

    :param start_angle: The value of the starting angle, 0-180 degrees.
    :type start_angle:  int
    :param stop_angle:  The value of the stopping angle, 0-180 degrees.
    :type stop_angle:   int
    :param step_angle:  The value of the stepping angle, 1-180 degrees; defaults to 1.
    :type step_angle:   int
    :param step_time:   The value of the stepping time in seconds; defaults to 0.015.
    :type step_time:    float
    """

    # Error checking of input values
    if start_angle != int(start_angle) or start_angle < 0 or start_angle > 180:  # check start_angle value
        print(f"ERROR: The start_angle value of {start_angle} is invalid.")
        return
    if stop_angle != int(stop_angle) or stop_angle < 0 or stop_angle > 180:  # check stop_angle value
        print(f"ERROR: The stop_angle value of {stop_angle} is invalid.")
        return
    if step_angle != int(step_angle) or step_angle < 1 or step_angle > abs(stop_angle - start_angle):  # check step_angle value
        print(f"ERROR: The step_angle value of {step_angle} is invalid.")
        return
    if step_time < 0:  # check step_time value
        print(f"ERROR: The step_time value of {step_time} is invalid.")
        return

    # Show operation description
    if DEBUG:
        print(f"Sweeping angle from {start_angle} to {stop_angle} degrees in increments of {step_angle} degree(s) with a {step_time} s step time.")

    # Perform operation
    if start_angle < stop_angle:  # increasing angle
        for angle in range(start_angle, stop_angle + 1, step_angle):
            if DEBUG: print(f"Setting angle to {angle} degrees.")
            servo_a.angle = angle  # library enforces actuation range safeguards
            sleep(step_time)
    else:  # decreasing angle
        for angle in range(start_angle, stop_angle - 1, -step_angle):
            if DEBUG: print(f"Setting angle to {angle} degrees.")
            servo_a.angle = angle  # library enforces actuation range safeguards
            sleep(step_time)


def sweep_operations():
    """Demonstrates a variety of servo sweeping operations."""

    servo_sweep(0, 180)          # sweep from 0 to 180 in 1 degree (default) increments with 0.015 s (default) delays in between
    sleep(5)
    servo_sweep(180, 0)          # sweep from 180 to 0 in 1 degree (default) increments with 0.015 s (default) delays in between
    sleep(5)
    servo_sweep(45, 135, 15, 1)  # sweep from 45 to 135 in 15 degree increments with 1 second delays in between
    sleep(5)
    servo_sweep(180, 0, 45, 1)   # sweep from 180 to 0 in 45 degree increments with 1 second delays in between
    sleep(5)


def main():
    """The main program entry."""

    while True:
        basic_operations()    # demonstrates basic servo operation
        # sweep_operations()  # demonstrates servo sweeping operations


if __name__ == "__main__":  # required for generating Sphinx documentation
    main()
