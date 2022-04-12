#########################
#                       #
# Configuration         #
#                       #
#########################


# Device IDs
DRIVE_CONTROLLER_ID = "6_1491370133845894324"
ARM_CONTROLLER_ID = "6_12577161366600381129"


# How to determine the desired drive motor velocity during teleop mode
def target_left_drive_motor_velocity():
    velocity: float = Gamepad.get_value("joystick_left_y")
    if abs(velocity) < 0.1:
        velocity = 0
    return velocity


def target_right_drive_motor_velocity():
    velocity: float = Gamepad.get_value("joystick_right_y")
    if abs(velocity) < 0.1:
        velocity = 0
    return velocity


# How to determine the desired arm motor velocity during teleop mode
ARM_UR: bool = lambda: Gamepad.get_value("l_bumper")
ARM_UL: bool = lambda: Gamepad.get_value("r_bumper")

ARM_DR: bool = lambda: Gamepad.get_value("r_trigger")
ARM_DL: bool = lambda: Gamepad.get_value("l_trigger")

# Which drive motor (a or b) is attached to the right and left wheels
L_DRIVE_MOTOR = 'a'
R_DRIVE_MOTOR = 'b'

# Which arm motor (a or b) is attached to the base of each arm
L_ARM_MOTOR = 'b'
R_ARM_MOTOR = 'a'

# Whether the direction of the motors should be inverted
INVERT_L_DRIVE_MOTOR = False
INVERT_R_DRIVE_MOTOR = True
INVERT_L_ARM_MOTOR = False
INVERT_R_ARM_MOTOR = False

# Speed at which the arms should raise and lower
ARM_SPEED = 1.0


#########################
#                       #
# End of configuration  #
#                       #
#########################


def autonomous_setup():
    # Set inversions for each motor
    Robot.set_value(DRIVE_CONTROLLER_ID, "invert_" + L_DRIVE_MOTOR, INVERT_L_DRIVE_MOTOR)
    Robot.set_value(DRIVE_CONTROLLER_ID, "invert_" + R_DRIVE_MOTOR, INVERT_R_DRIVE_MOTOR)
    Robot.set_value(ARM_CONTROLLER_ID, "invert_" + L_ARM_MOTOR, INVERT_L_ARM_MOTOR)
    Robot.set_value(ARM_CONTROLLER_ID, "invert_" + R_ARM_MOTOR, INVERT_R_ARM_MOTOR)

    # Disable PID on each motor due to hardware issues
    Robot.set_value(DRIVE_CONTROLLER_ID, "pid_enabled_" + L_DRIVE_MOTOR, False)
    Robot.set_value(DRIVE_CONTROLLER_ID, "pid_enabled_" + R_DRIVE_MOTOR, False)
    Robot.set_value(ARM_CONTROLLER_ID, "pid_enabled_" + L_ARM_MOTOR, False)
    Robot.set_value(ARM_CONTROLLER_ID, "pid_enabled_" + R_ARM_MOTOR, False)


def autonomous_main():
    pass


def teleop_setup():
    autonomous_setup()


def teleop_main():
    # Update velocity of each motor
    Robot.set_value(DRIVE_CONTROLLER_ID, "velocity_" + L_DRIVE_MOTOR, target_left_drive_motor_velocity())
    Robot.set_value(DRIVE_CONTROLLER_ID, "velocity_" + R_DRIVE_MOTOR, target_right_drive_motor_velocity())

    Robot.set_value(ARM_CONTROLLER_ID, "velocity_" + L_ARM_MOTOR, ARM_SPEED * ARM_UL())
    Robot.set_value(ARM_CONTROLLER_ID, "velocity_" + R_ARM_MOTOR, ARM_SPEED * ARM_UR())
    Robot.set_value(ARM_CONTROLLER_ID, "velocity_" + L_ARM_MOTOR, ARM_SPEED * ARM_DL() * -1)
    Robot.set_value(ARM_CONTROLLER_ID, "velocity_" + R_ARM_MOTOR, ARM_SPEED * ARM_DR() * -1)
