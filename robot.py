#MOTOR CONTROllers
DRIVE_CONTROLL_ID = "6_1491370133845894324"
ARM_CONTROLLER_ID = "6_12577161366600381129"

##### CONTROLLS SECTION #####

# reads a range from (-1.0, 1.0) --> (DOWN/LEFT, UP/RIGHT)
JOYSTICK_RY: float = lambda: Gamepad.get_value("joystick_right_y")
JOYSTICK_LY: float = lambda: Gamepad.get_value("joystick_left_y")

# reads TRUE/FALSE value depending on if BTN is Pressed
ARM_R: bool = lambda: Gamepad.get_value("r_trigger")
ARM_L: bool = lambda: Gamepad.get_value("l_trigger")

##### MOTORS SECTION #####

# TREAD MOTOR ID's
TREAD_R = '_a'
TREAD_L = '_b'

# ARM MOTOR ID's
ARM_ID_R = '_a'
ARM_ID_L = '_b'

#TREAD INVERSIONS
TREAD_INVERT_L = False
TREAD_INVERT_R = True

#ARM INVERSIONS
ARM_INVERT_L = False
ARM_INVERT_R = True

def autonomous_setup():
    pass

def autonomous_main():
    pass

def teleop_setup():
    pass

def teleop_main():
    resetMotors()
    if JOYSTICK_RY() != 0 && JOYSTICK_LY() != 0:
        Robot.set_value(DRIVE_CONTROLL_ID, "velocity"+TREAD_L, JOYSTICK_LY())
        Robot.set_value(DRIVE_CONTROLL_ID, "velocity"+TREAD_R, JOYSTICK_RY())
    elif JOYSTICK_RY() != 0 || JOYSTICK_LY() != 0:
        device = DRIVE_CONTROLL_ID
        if JOYSTICK_RY() != 0:
            motor = "velocity"+TREAD_R
            velocity = None
        else:
            motor = "velocity"+TREAD_L
            velocity = None
        Robot.set_value(device, motor, velocity)

def resetMotors(device: str = None, id: str = None):
    if not device:
        Robot.set_value(DRIVE_CONTROLL_ID, "velocity"+TREAD_L, 0)
        Robot.set_value(DRIVE_CONTROLL_ID, "velocity"+TREAD_R, 0)
        Robot.set_value(ARM_CONTROLLER_ID, "velocity"+ARM_ID_L, 0)
        Robot.set_value(ARM_CONTROLLER_ID, "velocity"+ARM_ID_R, 0)
    else:
        Robot.set_value(device, "velocity"+id, 0)
