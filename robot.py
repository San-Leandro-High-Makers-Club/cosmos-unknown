#########################
#                       #
# Configuration         #
#                       #
#########################


# Device IDs
DRIVE_CONTROLLER_ID = "6_1491370133845894324"
ARM_CONTROLLER_ID = "6_12577161366600381129"
LIMIT_SWITCH_ID = ""
CENTRE_LINE_FOLLOWER_ID = "2_3"
LEADING_LINE_FOLLOWER_ID = "2_4"

TOP_LIMIT_SWITCH = "switch0"
BOTTOM_LIMIT_SWITCH = "switch1"

# How to determine the desired drive motor velocity during teleop mode
def target_left_drive_motor_velocity():
    velocity: float = -Gamepad.get_value("joystick_left_y")
    if abs(velocity) < 0.1:
        velocity = 0
    return velocity


def target_right_drive_motor_velocity():
    velocity: float = -Gamepad.get_value("joystick_right_y")
    if abs(velocity) < 0.1:
        velocity = 0
    return velocity

# Buttons used to manually move the arm
ARM_UP_BUTTON = "l_bumper"
ARM_DOWN_BUTTON = "l_trigger"

# Which drive motor (a or b) is attached to the right and left wheels
L_DRIVE_MOTOR = 'a'
R_DRIVE_MOTOR = 'b'

# Which arm motor (a or b) is attached to the base of each arm
PINCER_MOTOR = 'b'
ARM_MOTOR = 'a'

# Whether the direction of the motors should be inverted
INVERT_L_DRIVE_MOTOR = True
INVERT_R_DRIVE_MOTOR = False
INVERT_PINCER_MOTOR = False
INVERT_ARM_MOTOR = False

# Speed at which the arms should raise and lower
ARM_SPEED = 1.0

# Speed at which the robot should drive during autonomous mode
AUTONOMOUS_SPEED = 0.8

# The minimum line follower reading that is considered to be on the tape
ON_LINE_THRESHOLD = 0.18

# The maximum line follower reading that is considered to be off the tape
OFF_LINE_THRESHOLD = 0.12

# The distance (as an encoder value) between the line follower sensors
LINE_FOLLOWER_SEPARATION: 100  # TODO: calibrate'

# Preset arm encoder positions
ARM_POSITIONS = {
    "button_a": 0, # highest position
    "button_b": -500  # lowest position
}


#########################
#                       #
# End of configuration  #
#                       #
#########################


def autonomous_setup():
    Robot.set_value(DRIVE_CONTROLLER_ID, "invert_" + L_DRIVE_MOTOR, INVERT_L_DRIVE_MOTOR)
    Robot.set_value(DRIVE_CONTROLLER_ID, "invert_" + R_DRIVE_MOTOR, INVERT_R_DRIVE_MOTOR)
    Robot.set_value(ARM_CONTROLLER_ID, "invert_" + PINCER_MOTOR, INVERT_PINCER_MOTOR)
    Robot.set_value(ARM_CONTROLLER_ID, "invert_" + ARM_MOTOR, INVERT_ARM_MOTOR)

    # Disable PID on each motor due to hardware issues
    Robot.set_value(DRIVE_CONTROLLER_ID, "pid_enabled_" + L_DRIVE_MOTOR, False)
    Robot.set_value(DRIVE_CONTROLLER_ID, "pid_enabled_" + R_DRIVE_MOTOR, False)
    Robot.set_value(ARM_CONTROLLER_ID, "pid_enabled_" + PINCER_MOTOR, False)
    Robot.set_value(ARM_CONTROLLER_ID, "pid_enabled_" + ARM_MOTOR, False)

    # Reset the drive encoders
    Robot.set_value(DRIVE_CONTROLLER_ID, "enc_" + L_DRIVE_MOTOR, 0)
    Robot.set_value(DRIVE_CONTROLLER_ID, "enc_" + R_DRIVE_MOTOR, 0)

    # Begin moving straight from the starting zone
    Robot.set_value(DRIVE_CONTROLLER_ID, "velocity_" + L_DRIVE_MOTOR, AUTONOMOUS_SPEED)
    Robot.set_value(DRIVE_CONTROLLER_ID, "velocity_" + R_DRIVE_MOTOR, AUTONOMOUS_SPEED)


def autonomous_main():
    pass


def drive_forward(distance: int, speed=AUTONOMOUS_SPEED, tolerance=100, stop=True) -> None:
    """Drive in a straight line for the specified distance, decelerating near the end

    :param distance: the distance to drive (as an encoder value). If negative, drive in reverse.
    :param speed: the speed at which to primarily drive. If extremely low, simply return immediately.
    :param tolerance: the maximum distance (as an encoder value) by which it is acceptable to deviate from the specified
        distance
    :param stop: if True, come to rest after the specified distance has been travelled, and attempt adjustments if the
        specified distance has been overshot
    :return: None
    """

    speed = abs(speed)
    if speed < 0.1:
        return
    tolerance = abs(tolerance)
    if tolerance > abs(distance):
        return
    if distance < 0:
        speed *= -1

    initial_left_motor_position: int = Robot.get_value(DRIVE_CONTROLLER_ID, "enc_" + L_DRIVE_MOTOR)
    initial_right_motor_position: int = Robot.get_value(DRIVE_CONTROLLER_ID, "enc_" + R_DRIVE_MOTOR)

    def left_motor_distance_travelled():
        return Robot.get_value(DRIVE_CONTROLLER_ID, "enc_" + L_DRIVE_MOTOR) - initial_left_motor_position

    def right_motor_distance_travelled():
        return Robot.get_value(DRIVE_CONTROLLER_ID, "enc_" + R_DRIVE_MOTOR) - initial_right_motor_position

    def average_distance_travelled():
        return int((left_motor_distance_travelled() + right_motor_distance_travelled()) / 2)

    while abs(distance - average_distance_travelled()) > 500:  # TODO: calibrate
        Robot.set_value(DRIVE_CONTROLLER_ID, "velocity_" + L_DRIVE_MOTOR, speed)
        Robot.set_value(DRIVE_CONTROLLER_ID, "velocity_" + R_DRIVE_MOTOR, speed)

    reduced_speed = 0.15
    if distance < 0:
        reduced_speed *= -1
    while abs(distance - average_distance_travelled()) > tolerance:
        Robot.set_value(DRIVE_CONTROLLER_ID, "velocity_" + L_DRIVE_MOTOR, reduced_speed)
        Robot.set_value(DRIVE_CONTROLLER_ID, "velocity_" + R_DRIVE_MOTOR, reduced_speed)

    if stop:
        Robot.set_value(DRIVE_CONTROLLER_ID, "velocity_" + L_DRIVE_MOTOR, 0)
        Robot.set_value(DRIVE_CONTROLLER_ID, "velocity_" + R_DRIVE_MOTOR, 0)
        Robot.sleep(1)
        if abs(distance - average_distance_travelled()) > tolerance:
            adjustment_distance = -abs(distance - average_distance_travelled())
            drive_forward(adjustment_distance, 0.5 * speed, tolerance, stop)


def arm_control():
    while True:
        bottom_switch_pressed: bool = Robot.get_value(LIMIT_SWITCH_ID, BOTTOM_LIMIT_SWITCH)
        top_switch_pressed: bool = Robot.get_value(LIMIT_SWITCH_ID, TOP_LIMIT_SWITCH)
        move_arm_up: bool = Gamepad.get_value(ARM_UP_BUTTON)
        move_arm_down: bool = Gamepad.get_value(ARM_DOWN_BUTTON)

        desired_preset = ""
        for button in list(ARM_POSITIONS):
            if Gamepad.get_value(button):
                if desired_preset == "":
                    desired_preset = button
                else:
                    desired_preset = ""
                    break

        if desired_preset == "":
            if move_arm_up and move_arm_down:
                move_arm_up = False
                move_arm_down = False

            if top_switch_pressed:
                Robot.set_value(ARM_CONTROLLER_ID, "velocity_" + ARM_MOTOR, 0)
                Robot.set_value(ARM_CONTROLLER_ID, "enc_"+ARM_MOTOR, ARM_POSITIONS["button_a"])
                move_arm_up = False

            if bottom_switch_pressed:
                Robot.set_value(ARM_CONTROLLER_ID, "velocity_" + ARM_MOTOR, 0)
                Robot.set_value(ARM_CONTROLLER_ID, "enc_"+ARM_MOTOR, ARM_POSITIONS["button_b"])
                move_arm_down = False

            if move_arm_up:
                Robot.set_value(ARM_CONTROLLER_ID, "velocity_" + ARM_MOTOR, ARM_SPEED)
            elif move_arm_down:
                Robot.set_value(ARM_CONTROLLER_ID, "velocity_" + ARM_MOTOR, -ARM_SPEED)
            else:
                Robot.set_value(ARM_CONTROLLER_ID, "velocity_" + ARM_MOTOR, 0)
        else:
            encoder_value = Robot.get_value(ARM_CONTROLLER_ID, "enc_" + ARM_MOTOR)
            while encoder_value <= ARM_POSITIONS[desired_preset]:
                Robot.set_value(ARM_CONTROLLER_ID, "velocity_" + ARM_MOTOR, ARM_SPEED)
            Robot.set_value(ARM_CONTROLLER_ID, "velocity_" + ARM_MOTOR, 0)


def teleop_setup():
    # Set inversions for each motor
    Robot.set_value(DRIVE_CONTROLLER_ID, "invert_" + L_DRIVE_MOTOR, INVERT_L_DRIVE_MOTOR)
    Robot.set_value(DRIVE_CONTROLLER_ID, "invert_" + R_DRIVE_MOTOR, INVERT_R_DRIVE_MOTOR)
    Robot.set_value(ARM_CONTROLLER_ID, "invert_" + PINCER_MOTOR, INVERT_PINCER_MOTOR)
    Robot.set_value(ARM_CONTROLLER_ID, "invert_" + ARM_MOTOR, INVERT_ARM_MOTOR)

    # Disable PID on each motor due to hardware issues
    Robot.set_value(DRIVE_CONTROLLER_ID, "pid_enabled_" + L_DRIVE_MOTOR, False)
    Robot.set_value(DRIVE_CONTROLLER_ID, "pid_enabled_" + R_DRIVE_MOTOR, False)
    Robot.set_value(ARM_CONTROLLER_ID, "pid_enabled_" + PINCER_MOTOR, False)
    Robot.set_value(ARM_CONTROLLER_ID, "pid_enabled_" + ARM_MOTOR, False)

    Robot.run(arm_control)


def teleop_main():
    # Update velocity of each motor
    Robot.set_value(DRIVE_CONTROLLER_ID, "velocity_" + L_DRIVE_MOTOR, target_left_drive_motor_velocity())
    Robot.set_value(DRIVE_CONTROLLER_ID, "velocity_" + R_DRIVE_MOTOR, target_right_drive_motor_velocity())
