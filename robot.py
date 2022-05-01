from typing import Dict

#########################
#                       #
# Configuration         #
#                       #
#########################


# Device IDs
DRIVE_CONTROLLER_ID = "6_1491370133845894324"
ARM_CONTROLLER_ID = "6_12577161366600381129"
LIMIT_SWITCH_ID = "1_13560084343449335556"
CENTER_LINE_FOLLOWER_ID = "2_1187947831541557793"
LEADING_LINE_FOLLOWER_ID = "2_17787866091254328692"

# Which of the three infrared sensors are actually on each side of the line followers
CENTER_LINE_FOLLOWER_SENSORS = {
    "left": "left",
    "center": "center",
    "right": "right"
}
LEADING_LINE_FOLLOWER_SENSORS = {
    "left": "left",
    "center": "center",
    "right": "right"
}

# Which limit switch is located at each end of the arm's range
TOP_LIMIT_SWITCH = "switch0"
BOTTOM_LIMIT_SWITCH = "switch1"


# How to determine the desired drive motor velocity during teleop mode
def target_left_drive_motor_velocity():
    velocity: float = -Gamepad.get_value("joystick_left_y")
    if abs(velocity) < 0.15:
        velocity = 0
    return velocity


def target_right_drive_motor_velocity():
    velocity: float = -Gamepad.get_value("joystick_right_y")
    if abs(velocity) < 0.15:
        velocity = 0
    return velocity


# Buttons used to manually move the arm
ARM_UP_BUTTON = "l_bumper"
ARM_DOWN_BUTTON = "l_trigger"

# Buttons used to operate the pincer
PINCER_OPEN_BUTTON = "r_bumper"
PINCER_CLOSE_BUTTON = "r_trigger"

# Which drive motor (a or b) is attached to the right and left wheels
L_DRIVE_MOTOR = 'a'
R_DRIVE_MOTOR = 'b'

# Which arm motor (a or b) is attached to the base of each arm
PINCER_MOTOR = 'a'
ARM_MOTOR = 'b'

# Whether the direction of the motors should be inverted
INVERT_L_DRIVE_MOTOR = True
INVERT_R_DRIVE_MOTOR = False
INVERT_PINCER_MOTOR = True
INVERT_ARM_MOTOR = False

# Speed at which the arms should raise and lower
ARM_SPEED = 0.5

# True speed at which the arm should move when a preset is activated. This is a "true" speed; attempts will be made
# to ensure that the arm does in fact travel at this speed (compensating for the effects of the gravitational torque).
AUTOMATIC_ARM_SPEED = 0.35

# Speed at which the pincer should open and close
PINCER_SPEED = 0.4

# Speed at which the robot should drive during autonomous mode
AUTONOMOUS_SPEED = 0.3

# Speed at which the robot should drive during autonomous mode when precision is needed
REDUCED_AUTONOMOUS_SPEED = 0.15

# Speed at which the robot should rotate during autonomous mode
AUTONOMOUS_ROTATION_SPEED = 0.4

# The minimum line follower reading that is considered to be on the tape
ON_LINE_THRESHOLD = 0.075

# The maximum line follower reading that is considered to be off the tape
OFF_LINE_THRESHOLD = 0.06

# The distance (as an encoder value) the drive motors much each turn (in opposite directions) to rotate the robot by 90
# degrees
QUARTER_TURN_ARC_LENGTH = 1065

# The maximum error (in degrees) to anticipate in autonomous_heading
HEADING_TOLERANCE = 10

# Range of arm positions (as encoder values) where the motor must be powered in the upwards direction to cancel the
# gravitational torque. In these positions, the arm is extended outwards in front of the robot.
ARM_GRAVITY_RANGE = (-1500, -790)

# Range of arm positions (as encoder values) where the motor must be powered in the downwards direction to cancel the
# gravitational torque. In these positions, the arm is folded back above the robot. 
REVERSE_ARM_GRAVITY_RANGE = (-315, 20)

# The velocity at which the arm motor must be powered when inside a gravity range to maintain its position
ARM_GRAVITY_POWER = 0.2

# Preset arm encoder positions
# The key is the gamepad button used to activate the preset; the value is the preset encoder position
ARM_POSITIONS = {
    "dpad_up": 0,  # highest position
    "dpad_down": -1180,  # lowest position
    "button_a": -1165,  # satellite dish
    "button_b": -760,  # refinery
    "button_x": -700  # command room
}

# Maximum acceptable deviation (as an encoder value) from the arm position when using a preset
ARM_POSITION_TOLERANCE = 8


#########################
#                       #
# End of configuration  #
#                       #
#########################


def autonomous_setup():
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

    # Reset the drive encoders
    Robot.set_value(DRIVE_CONTROLLER_ID, "enc_" + L_DRIVE_MOTOR, 0)
    Robot.set_value(DRIVE_CONTROLLER_ID, "enc_" + R_DRIVE_MOTOR, 0)

    # Begin moving straight from the starting zone
    Robot.set_value(DRIVE_CONTROLLER_ID, "velocity_" + L_DRIVE_MOTOR, AUTONOMOUS_SPEED)
    Robot.set_value(DRIVE_CONTROLLER_ID, "velocity_" + R_DRIVE_MOTOR, AUTONOMOUS_SPEED)


def get_line_follower_values(line_follower: str) -> Dict[str, float]:
    """Return the sensor readings of a line follower as a dictionary

    :param line_follower: a string (either "center" or "leading") representing which of the two line followers (the one
        mounted underneath the center of the robot, or the one underneath the front) from which to obtain values
    :return: a dictionary which maps the true positions of each of the three infrared sensors ("left", "center", or
        "right") to the reflected light value of that sensor, or an empty dictionary if an invalid line_follower
        parameter was used
    """

    if line_follower == "center":
        values = {}
        for sensor in list(CENTER_LINE_FOLLOWER_SENSORS):
            values[sensor] = Robot.get_value(CENTER_LINE_FOLLOWER_ID, CENTER_LINE_FOLLOWER_SENSORS[sensor])
        return values
    elif line_follower == "leading":
        values = {}
        for sensor in list(LEADING_LINE_FOLLOWER_SENSORS):
            values[sensor] = Robot.get_value(LEADING_LINE_FOLLOWER_ID, LEADING_LINE_FOLLOWER_SENSORS[sensor])
        return values
    else:
        return {}


# Store the current robot orientation (in degrees) relative to the starting zone during the autonomous period.
# Positive values are counterclockwise.
autonomous_heading = 0.0

# Store whether the robot has progressed beyond the third tape segment (in front of the campsite, parallel to the
# midline) during the autonomous period
completed_third_tape_segment = False

# Store whether the robot has reached the end zone during the autonomous period
completed_autonomous = False


def autonomous_main():
    global autonomous_heading, completed_third_tape_segment, completed_autonomous

    if completed_autonomous:  # we're done :)
        Robot.set_value(DRIVE_CONTROLLER_ID, "velocity_" + L_DRIVE_MOTOR, 0)
        Robot.set_value(DRIVE_CONTROLLER_ID, "velocity_" + R_DRIVE_MOTOR, 0)
        return

    if get_line_follower_values("leading")["left"] > get_line_follower_values("leading")["center"] >= ON_LINE_THRESHOLD:
        # We're drifting to the right
        # Rotate left until the leading line follower is above the line again, keeping track of how far we turn
        initial_encoder_position = Robot.get_value(DRIVE_CONTROLLER_ID, "enc_" + R_DRIVE_MOTOR)
        while get_line_follower_values("leading")["left"] >= get_line_follower_values("leading")["center"]:
            Robot.set_value(DRIVE_CONTROLLER_ID, "velocity_" + L_DRIVE_MOTOR, -AUTONOMOUS_ROTATION_SPEED)
            Robot.set_value(DRIVE_CONTROLLER_ID, "velocity_" + R_DRIVE_MOTOR, AUTONOMOUS_ROTATION_SPEED)
        theta = abs(Robot.get_value(DRIVE_CONTROLLER_ID, "enc_" + R_DRIVE_MOTOR) - initial_encoder_position) / (
                QUARTER_TURN_ARC_LENGTH / 90)
        # See if we've reached the end of the third tape segment
        if not completed_third_tape_segment:
            if abs(90 - abs(autonomous_heading)) < HEADING_TOLERANCE < abs(90 - abs(autonomous_heading + theta)):
                completed_third_tape_segment = True
        autonomous_heading += theta
        return  # Continue autonomous driving
    elif get_line_follower_values("leading")["right"] > get_line_follower_values("leading")["center"] >= \
            ON_LINE_THRESHOLD:
        # We're drifting to the left
        # Rotate right until the leading line follower is above the line again, keeping track of how far we turn
        initial_encoder_position = Robot.get_value(DRIVE_CONTROLLER_ID, "enc_" + L_DRIVE_MOTOR)
        while get_line_follower_values("leading")["right"] >= get_line_follower_values("leading")["center"]:
            Robot.set_value(DRIVE_CONTROLLER_ID, "velocity_" + L_DRIVE_MOTOR, AUTONOMOUS_ROTATION_SPEED)
            Robot.set_value(DRIVE_CONTROLLER_ID, "velocity_" + R_DRIVE_MOTOR, -AUTONOMOUS_ROTATION_SPEED)
        theta = abs(Robot.get_value(DRIVE_CONTROLLER_ID, "enc_" + L_DRIVE_MOTOR) - initial_encoder_position) / (
                QUARTER_TURN_ARC_LENGTH / 90)
        # See if we've reached the end of the third tape segment
        if not completed_third_tape_segment:
            if abs(90 - abs(autonomous_heading)) < HEADING_TOLERANCE < abs(90 - abs(autonomous_heading - theta)):
                completed_third_tape_segment = True
        autonomous_heading -= theta
        return  # Continue autonomous driving

    if get_line_follower_values("leading")["center"] >= ON_LINE_THRESHOLD:
        # Continue straight on the line
        Robot.set_value(DRIVE_CONTROLLER_ID, "velocity_" + L_DRIVE_MOTOR, AUTONOMOUS_SPEED)
        Robot.set_value(DRIVE_CONTROLLER_ID, "velocity_" + R_DRIVE_MOTOR, AUTONOMOUS_SPEED)
    else:
        # Proceed with caution
        Robot.set_value(DRIVE_CONTROLLER_ID, "velocity_" + L_DRIVE_MOTOR, REDUCED_AUTONOMOUS_SPEED)
        Robot.set_value(DRIVE_CONTROLLER_ID, "velocity_" + R_DRIVE_MOTOR, REDUCED_AUTONOMOUS_SPEED)

    if get_line_follower_values("leading")["center"] <= OFF_LINE_THRESHOLD:
        # See if we're almost done (on the line following tape inside the end zone)
        if completed_third_tape_segment and abs(90 - abs(autonomous_heading)) < HEADING_TOLERANCE:
            leading_sensors = get_line_follower_values("leading")
            if leading_sensors["left"] <= OFF_LINE_THRESHOLD and leading_sensors["right"] <= OFF_LINE_THRESHOLD:
                # This seems to be the end
                while get_line_follower_values("center")["center"] >= ON_LINE_THRESHOLD:
                    Robot.set_value(DRIVE_CONTROLLER_ID, "velocity_" + L_DRIVE_MOTOR, REDUCED_AUTONOMOUS_SPEED)
                    Robot.set_value(DRIVE_CONTROLLER_ID, "velocity_" + R_DRIVE_MOTOR, REDUCED_AUTONOMOUS_SPEED)
                Robot.set_value(DRIVE_CONTROLLER_ID, "velocity_" + L_DRIVE_MOTOR, 0)
                Robot.set_value(DRIVE_CONTROLLER_ID, "velocity_" + R_DRIVE_MOTOR, 0)
                completed_autonomous = True
                return


# Control the arm based on driver and sensor input
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

        if desired_preset == "":  # control the arm manually
            if move_arm_up and move_arm_down:
                move_arm_up = False
                move_arm_down = False

            if top_switch_pressed:
                Robot.set_value(ARM_CONTROLLER_ID, "enc_" + ARM_MOTOR, max(ARM_POSITIONS.values()))
                move_arm_up = False

            if bottom_switch_pressed:
                Robot.set_value(ARM_CONTROLLER_ID, "enc_" + ARM_MOTOR, min(ARM_POSITIONS.values()))
                move_arm_down = False

            if move_arm_up:
                Robot.set_value(ARM_CONTROLLER_ID, "velocity_" + ARM_MOTOR, ARM_SPEED)
            elif move_arm_down:
                Robot.set_value(ARM_CONTROLLER_ID, "velocity_" + ARM_MOTOR, -ARM_SPEED)
            else:
                encoder_value = Robot.get_value(ARM_CONTROLLER_ID, "enc_" + ARM_MOTOR)
                if ARM_GRAVITY_RANGE[0] < encoder_value < ARM_GRAVITY_RANGE[1]:
                    Robot.set_value(ARM_CONTROLLER_ID, "velocity_" + ARM_MOTOR, ARM_GRAVITY_POWER)
                elif REVERSE_ARM_GRAVITY_RANGE[0] < encoder_value < REVERSE_ARM_GRAVITY_RANGE[1]:
                    Robot.set_value(ARM_CONTROLLER_ID, "velocity_" + ARM_MOTOR, -ARM_GRAVITY_POWER)
                else:
                    Robot.set_value(ARM_CONTROLLER_ID, "velocity_" + ARM_MOTOR, 0)

        else:  # control the arm automatically using preset encoder positions
            encoder_value = Robot.get_value(ARM_CONTROLLER_ID, "enc_" + ARM_MOTOR)
            while abs(encoder_value - ARM_POSITIONS[desired_preset]) > ARM_POSITION_TOLERANCE:
                if encoder_value < ARM_POSITIONS[desired_preset]:  # going up
                    if Robot.get_value(LIMIT_SWITCH_ID, TOP_LIMIT_SWITCH) or Gamepad.get_value(ARM_DOWN_BUTTON):
                        break
                    desired_arm_speed = AUTOMATIC_ARM_SPEED
                    if ARM_GRAVITY_RANGE[0] < encoder_value < ARM_GRAVITY_RANGE[1]:
                        # we're fighting gravity
                        desired_arm_speed += ARM_GRAVITY_POWER
                    if REVERSE_ARM_GRAVITY_RANGE[0] < encoder_value < REVERSE_ARM_GRAVITY_RANGE[1]:
                        # gravity is already working in our favour
                        desired_arm_speed -= ARM_GRAVITY_POWER
                    if desired_arm_speed > 1:
                        desired_arm_speed = 1
                    elif desired_arm_speed < 0:
                        desired_arm_speed = 0
                    Robot.set_value(ARM_CONTROLLER_ID, "velocity_" + ARM_MOTOR, desired_arm_speed)
                elif encoder_value > ARM_POSITIONS[desired_preset]:  # going down
                    if Robot.get_value(LIMIT_SWITCH_ID, BOTTOM_LIMIT_SWITCH) or Gamepad.get_value(ARM_UP_BUTTON):
                        break
                    desired_arm_speed = -AUTOMATIC_ARM_SPEED
                    if ARM_GRAVITY_RANGE[0] < encoder_value < ARM_GRAVITY_RANGE[1]:
                        # gravity is already working in our favour
                        desired_arm_speed += ARM_GRAVITY_POWER
                    if REVERSE_ARM_GRAVITY_RANGE[0] < encoder_value < REVERSE_ARM_GRAVITY_RANGE[1]:
                        # we're fighting gravity
                        desired_arm_speed -= ARM_GRAVITY_POWER
                    if desired_arm_speed < -1:
                        desired_arm_speed = -1
                    elif desired_arm_speed > 0:
                        desired_arm_speed = 0
                    Robot.set_value(ARM_CONTROLLER_ID, "velocity_" + ARM_MOTOR, desired_arm_speed)
                encoder_value = Robot.get_value(ARM_CONTROLLER_ID, "enc_" + ARM_MOTOR)
            continue

        open_pincer: bool = Gamepad.get_value(PINCER_OPEN_BUTTON)
        close_pincer: bool = Gamepad.get_value(PINCER_CLOSE_BUTTON)

        if open_pincer and close_pincer:
            open_pincer = False
            close_pincer = False

        if open_pincer:
            Robot.set_value(ARM_CONTROLLER_ID, "velocity_" + PINCER_MOTOR, PINCER_SPEED)
        elif close_pincer:
            Robot.set_value(ARM_CONTROLLER_ID, "velocity_" + PINCER_MOTOR, -PINCER_SPEED)
        else:
            Robot.set_value(ARM_CONTROLLER_ID, "velocity_" + PINCER_MOTOR, 0)


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

    # Start arm control
    Robot.run(arm_control)


def teleop_main():
    # Update velocity of each motor
    Robot.set_value(DRIVE_CONTROLLER_ID, "velocity_" + L_DRIVE_MOTOR, target_left_drive_motor_velocity())
    Robot.set_value(DRIVE_CONTROLLER_ID, "velocity_" + R_DRIVE_MOTOR, target_right_drive_motor_velocity())
