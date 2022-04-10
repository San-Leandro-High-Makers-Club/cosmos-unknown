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
TREAD_R = 'a'
TREAD_L = 'b'

# ARM MOTOR ID's
ARM_ID_R = 'a'
ARM_ID_L = 'b'

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
    if not JOYSTICK_RY() == 0:
        pass
