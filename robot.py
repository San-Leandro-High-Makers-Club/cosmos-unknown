#MOTOR CONTROllers
DRIVE_CONTROLLER_ID = "6_1491370133845894324"
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

#TREAD MOTOR INVERSIONS
TREAD_INVERT_L = False
TREAD_INVERT_R = False

#ARM MOTOR INVERSIONS
ARM_INVERT_L = False
ARM_INVERT_R = False

def autonomous_setup():
    Robot.set_value(DRIVE_CONTROLLER_ID, "invert"+TREAD_L, TREAD_INVERT_L)
    Robot.set_value(DRIVE_CONTROLLER_ID, "invert"+TREAD_R, TREAD_INVERT_R)
    Robot.set_value(ARM_CONTROLLER_ID, "invert"+ARM_ID_L, ARM_INVERT_L)
    Robot.set_value(ARM_CONTROLLER_ID, "invert"+ARM_ID_R, ARM_INVERT_R)

def autonomous_main():
    pass

def teleop_setup():
    Robot.set_value(DRIVE_CONTROLLER_ID, "invert"+TREAD_L, TREAD_INVERT_L)
    Robot.set_value(DRIVE_CONTROLLER_ID, "invert"+TREAD_R, TREAD_INVERT_R)
    Robot.set_value(ARM_CONTROLLER_ID, "invert"+ARM_ID_L, ARM_INVERT_L)
    Robot.set_value(ARM_CONTROLLER_ID, "invert"+ARM_ID_R, ARM_INVERT_R)

def teleop_main():
    if JOYSTICK_LY() != 0:
        Robot.set_value(DRIVE_CONTROLLER_ID, "velocity"+TREAD_L, JOYSTICK_LY())
    if JOYSTICK_RY() != 0:
        Robot.set_value(DRIVE_CONTROLLER_ID, "velocity"+TREAD_R, JOYSTICK_RY())
    if ARM_L() != 0:
        Robot.set_value(ARM_CONTROLLER_ID, "velocity"+ARM_ID_L, JOYSTICK_LY())
    if ARM_R() != 0:
        Robot.set_value(ARM_CONTROLLER_ID, "velocity"+ARM_ID_R, JOYSTICK_RY())
