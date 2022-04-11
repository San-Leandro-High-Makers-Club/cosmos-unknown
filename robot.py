##### MOTOR CONTROlLER SECTION #####

# CONTROLLER ID'S
DRIVE_CONTROLLER_ID = "6_1491370133845894324"
ARM_CONTROLLER_ID = "6_12577161366600381129"

# DEADBAND RANGE'S
DRIVE_DB_RANGE = None
ARM_DB_RANGE = None

##### CONTROLLS SECTION #####

# reads a range from (-1.0, 1.0) --> (DOWN/LEFT, UP/RIGHT)
JOYSTICK_RY: float = lambda: Gamepad.get_value("joystick_right_y")
JOYSTICK_LY: float = lambda: Gamepad.get_value("joystick_left_y")

# reads TRUE/FALSE value depending on if BTN is Pressed

ARM_UR: bool = lambda: Gamepad.get_value("l_bumper")
ARM_UL: bool = lambda: Gamepad.get_value("r_bumper")

ARM_DR: bool = lambda: Gamepad.get_value("r_trigger")
ARM_DL: bool = lambda: Gamepad.get_value("l_trigger")

##### MOTORS SECTION #####

# TREAD MOTOR ID's
TREAD_ID_R = '_a'
TREAD_ID_L = '_b'

# ARM MOTOR ID's
ARM_ID_R = '_a'
ARM_ID_L = '_b'

# TREAD + ARM MOTOR INVERSIONS
TREAD_INVERT_L = False
TREAD_INVERT_R = False
ARM_INVERT = False

# ARM MOTOR SPEED
ARM_SPEED = 1.0


def autonomous_setup():
    # sets the inverts for the individual motors on each controller
    Robot.set_value(DRIVE_CONTROLLER_ID, "invert" + TREAD_ID_L, TREAD_INVERT_L)
    Robot.set_value(DRIVE_CONTROLLER_ID, "invert" + TREAD_ID_R, TREAD_INVERT_R)
    Robot.set_value(ARM_CONTROLLER_ID, "invert" + ARM_ID_L, ARM_INVERT)
    Robot.set_value(ARM_CONTROLLER_ID, "invert" + ARM_ID_R, ARM_INVERT)


def autonomous_main():
    pass


def teleop_setup():
    # sets the inverts for the individual motors on each controller
    Robot.set_value(DRIVE_CONTROLLER_ID, "invert" + TREAD_ID_L, TREAD_INVERT_L)
    Robot.set_value(DRIVE_CONTROLLER_ID, "invert" + TREAD_ID_R, TREAD_INVERT_R)
    Robot.set_value(ARM_CONTROLLER_ID, "invert" + ARM_ID_L, ARM_INVERT)
    Robot.set_value(ARM_CONTROLLER_ID, "invert" + ARM_ID_R, ARM_INVERT)


def teleop_main():
    # updates the velocity param value of the motor, on condition TRUE
    if JOYSTICK_LY() != 0:
        Robot.set_value(DRIVE_CONTROLLER_ID, "velocity" + TREAD_ID_L, JOYSTICK_LY())
    if JOYSTICK_RY() != 0:
        Robot.set_value(DRIVE_CONTROLLER_ID, "velocity" + TREAD_ID_R, JOYSTICK_RY())
    if ARM_UL() != 0:
        Robot.set_value(ARM_CONTROLLER_ID, "velocity" + ARM_ID_L, ARM_SPEED)
    if ARM_UR() != 0:
        Robot.set_value(ARM_CONTROLLER_ID, "velocity" + ARM_ID_R, ARM_SPEED)
    if ARM_DL() != 0:
        Robot.set_value(ARM_CONTROLLER_ID, "velocity" + ARM_ID_L, ARM_SPEED*-1)
    if ARM_DL() != 0:
        Robot.set_value(ARM_CONTROLLER_ID, "velocity" + ARM_ID_R, ARM_SPEED*-1)
