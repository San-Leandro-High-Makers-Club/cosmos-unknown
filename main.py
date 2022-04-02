# Device IDs. For production, set them to the numeric values shown in Dawn.
MOTOR_ID = "6_1"
ARM_MOTOR_ID = "6_2"
LINE_FOLLOWER_ID = "2_3"

# These constants define the keymap used during teleop to move or turn the robot,
# or to raise/lower the arm. By default they conform to the WASD convention, plus
# I and K to raise and lower, but may be reset if desired.
FORWARD_KEY = "w"
BACKWARD_KEY = "s"
LEFT_KEY = "a"
RIGHT_KEY = "d"
RAISE_KEY = "i"
LOWER_KEY = "k"

# These constants define the keys used during teleop to control the robot's speed.
# They default to the up and down arrow keys, but may be reset if desired.
ACCELERATE_KEY = "up_arrow"
DECELERATE_KEY = "down_arrow"

# Store up to 9 encoder presets for the arm motor in this array. The first and last
# elements should represent the minimum and maximum positions, respectively.
ARM_POSITIONS = [-413, -369, -345, -317, -305, -201, -188, 0]

# Set this to define the encoder tolerance for the arm. When the arm is automatically
# being moved to a position, it will automatically stop when the encoder reading is
# within the target position +/- this tolerance value.
ARM_POSITION_TOLERANCE = 8

# Set this to define the minimum value for the line follower reading to be considered
# high, that is, on the line.
# https://github.com/pioneers/runtime/wiki/Lowcar-Devices#line-follower
ON_LINE_THRESHOLD = 0.18

# Set this to define the maximum value for the line follower reading to be considered
# low, that is, off the line.
OFF_LINE_THRESHOLD = 0.12

# Set this value to define the increments by which speed changes for one keypress.
# The speed is a value between 0 and 1, so this value should be of the order of
# magnitude of one-tenth.
ACCELERATION_INCREMENT = 0.1

# Set this constant to define the speed at which the arm motor should run. Should
# be a value in the range (0, 1].
ARM_SPEED = 0.07

# Set this constant to define the speed at which the robot should drive during
# autonomous mode. Should be a value in the range (0, 1].
AUTONOMOUS_SPEED = 0.5

# Set this value to define the multiplier by which the inner motor's speed during a
# circular (i.e., not pivot) turn is reduced. For instance, 0.7 will cause the inner
# motor's speed to drop to 70% its regular value.
TURNING_SPEED_REDUCTION_FACTOR = 0.5

# The KoalaBear motor controller manages two motors, A and B, one for each side.
# Therefore, each of its parameters must be qualified by appending "_a" or "_b",
# for example as in "velocity_a" and "velocity_b".
# https://github.com/pioneers/runtime/wiki/Lowcar-Devices#koalabear
# Set each of the constants below to either "_a" or "_b" to indicate which motor
# corresponds to the left, and which corresponds to the right.
L_MOTOR = "_b"
R_MOTOR = "_a"

# There is a separate KoalaBear controller for the arm. Set this constant to "_a"
# or "_b" to define which motor on the controller is actually in use.
ARM_MOTOR = "_b"

# The convention used throughout the rest of this code is that a positive velocity
# value, such as 1.0, indicates that the motor should rotate in the forward direction.
# (In the case of the arm motor, positive means the motor should raise the arm.)
# In case one or more of the motors controlled by KoalaBear rotate the wrong way,
# set the appropriate constant(s) below to True.
INVERT_L = False
INVERT_R = True
INVERT_ARM = False

# The "velocity" parameters for the motors are used frequently. For convenience, the
# following constants will be automatically set to "velocity_a" and "velocity_b",
# dependent on which motor corresponds to each side.
# These should not be changed manually.
V_L = "velocity" + L_MOTOR
V_R = "velocity" + R_MOTOR

# Speed at which the motors should rotate. Should be a value in the range (0, 1].
# The speed to use during the autonomous period is configured separately.
# This is a variable, not a constant, yet should not be changed manually.
speed = 0.8


# Checks if a non-zero number key is pressed. Returns the number, or -1 if no number key is pressed.
def number_key_pressed():
    for i in range(1, 9):
        if Keyboard.get_value(str(i)):
            return i
    return -1


# Waits for key presses to raise and lower the arm
def arm_control():
    while True:
        if Keyboard.get_value(RAISE_KEY) and not Keyboard.get_value(LOWER_KEY):
            Robot.set_value(ARM_MOTOR_ID, "velocity" + ARM_MOTOR, ARM_SPEED)
        elif Keyboard.get_value(LOWER_KEY) and not Keyboard.get_value(RAISE_KEY):
            Robot.set_value(ARM_MOTOR_ID, "velocity" + ARM_MOTOR, -1 * ARM_SPEED)
        else:
            Robot.set_value(ARM_MOTOR_ID, "velocity" + ARM_MOTOR, 0)

        number_key = number_key_pressed()
        if number_key != -1 and len(ARM_POSITIONS) > number_key - 1 >= 0:
            move_arm_to(ARM_POSITIONS[number_key - 1])

        # When the zero key is hit, reset the encoder
        if Keyboard.get_value("0"):
            Robot.set_value(ARM_MOTOR_ID, "enc" + ARM_MOTOR, 0)


# Moves the arm to the specified encoder position
def move_arm_to(position):
    # Retrieves current position of the arm motor
    current_position = Robot.get_value(ARM_MOTOR_ID, "enc" + ARM_MOTOR)

    while current_position + ARM_POSITION_TOLERANCE < position or current_position - ARM_POSITION_TOLERANCE > position:
        if current_position < position:
            Robot.set_value(ARM_MOTOR_ID, "velocity" + ARM_MOTOR, ARM_SPEED)
        elif position < current_position:
            Robot.set_value(ARM_MOTOR_ID, "velocity" + ARM_MOTOR, -1 * ARM_SPEED)

        # Retrieves current position of the arm motor
        current_position = Robot.get_value(ARM_MOTOR_ID, "enc" + ARM_MOTOR)

    Robot.set_value(ARM_MOTOR_ID, "velocity" + ARM_MOTOR, 0)


# Waits for key presses to change the driving speed of the robot
def speed_control():
    global speed  # We'll be changing the speed within this function
    while True:
        if Keyboard.get_value(ACCELERATE_KEY) and speed + ACCELERATION_INCREMENT <= 1.0:
            speed += ACCELERATION_INCREMENT
            # Now busy-wait until the key is released before trying to do anything else
            while True:
                if not Keyboard.get_value(ACCELERATE_KEY):
                    break
        if Keyboard.get_value(DECELERATE_KEY) and speed - ACCELERATION_INCREMENT > 0:
            speed -= ACCELERATION_INCREMENT
            # Now busy-wait until the key is released before trying to do anything else
            while True:
                if not Keyboard.get_value(DECELERATE_KEY):
                    break


def autonomous_setup():
    # Disable PID controller due to hardware issues on the drive motors
    # https://docs.google.com/document/d/1Bi5tDYYOviFL5MYXJ8SwrKTu1mmJ2zzqVhgLzXcIwQg/edit
    Robot.set_value(MOTOR_ID, 'pid_enabled_a', False)
    Robot.set_value(MOTOR_ID, 'pid_enabled_b', False)

    # Configure inversions
    Robot.set_value(MOTOR_ID, "invert" + L_MOTOR, INVERT_L)
    Robot.set_value(MOTOR_ID, "invert" + R_MOTOR, INVERT_R)

    # Begin moving from the starting zone
    Robot.set_value(MOTOR_ID, V_L, AUTONOMOUS_SPEED)
    Robot.set_value(MOTOR_ID, V_R, AUTONOMOUS_SPEED)


def autonomous_main():
    driftingLeft = Robot.get_value(LINE_FOLLOWER_ID, "right") >= ON_LINE_THRESHOLD and Robot.get_value(
        LINE_FOLLOWER_ID, "left") <= OFF_LINE_THRESHOLD
    driftingRight = Robot.get_value(LINE_FOLLOWER_ID, "left") >= ON_LINE_THRESHOLD and Robot.get_value(
        LINE_FOLLOWER_ID, "right") <= OFF_LINE_THRESHOLD

    if driftingLeft:
        # Correct by turning towards the right
        Robot.set_value(MOTOR_ID, V_R, TURNING_SPEED_REDUCTION_FACTOR * AUTONOMOUS_SPEED)
    elif driftingRight:
        # Correct by turning towards the left
        Robot.set_value(MOTOR_ID, V_L, TURNING_SPEED_REDUCTION_FACTOR * AUTONOMOUS_SPEED)
    else:
        # Set all motors to go straight
        Robot.set_value(MOTOR_ID, V_L, AUTONOMOUS_SPEED)
        Robot.set_value(MOTOR_ID, V_R, AUTONOMOUS_SPEED)


def teleop_setup():
    # Tell PiE staff to put arm into reset position (bent all the way back at the maximum) before running
    # This line will set the position of the arm to an encoder value of 0
    Robot.set_value(ARM_MOTOR_ID, "enc" + ARM_MOTOR, 0)

    # Disable PID controller due to hardware issues on the drive motors
    # https://docs.google.com/document/d/1Bi5tDYYOviFL5MYXJ8SwrKTu1mmJ2zzqVhgLzXcIwQg/edit
    Robot.set_value(MOTOR_ID, 'pid_enabled_a', False)
    Robot.set_value(MOTOR_ID, 'pid_enabled_b', False)

    # Configure inversions
    Robot.set_value(MOTOR_ID, "invert" + L_MOTOR, INVERT_L)
    Robot.set_value(MOTOR_ID, "invert" + R_MOTOR, INVERT_R)
    Robot.set_value(ARM_MOTOR_ID, "invert" + ARM_MOTOR, INVERT_ARM)

    Robot.run(arm_control)
    Robot.run(speed_control)


def teleop_main():
    # These will store the speed that each motor should be set to
    current_speed_left = 0
    current_speed_right = 0

    if Keyboard.get_value(FORWARD_KEY):
        current_speed_left = speed
        current_speed_right = speed
        if Keyboard.get_value(LEFT_KEY) != Keyboard.get_value(RIGHT_KEY):
            # We're trying to turn whilst driving forward. Reduce the speed of the wheels on the inside of the turn
            if Keyboard.get_value(LEFT_KEY):
                current_speed_left *= TURNING_SPEED_REDUCTION_FACTOR
            else:
                current_speed_right *= TURNING_SPEED_REDUCTION_FACTOR
    elif Keyboard.get_value(BACKWARD_KEY):
        current_speed_left = speed * -1
        current_speed_right = speed * -1
    elif Keyboard.get_value(LEFT_KEY) != Keyboard.get_value(RIGHT_KEY):
        # We're trying to turn without moving forward. Turn around the robot's own axis (run wheels on each side in
        # opposite directions)
        if Keyboard.get_value(LEFT_KEY):
            current_speed_left = speed * -1
            current_speed_right = speed
        else:
            current_speed_left = speed
            current_speed_right = speed * -1

    # Perform the actual update to the motors
    Robot.set_value(MOTOR_ID, V_L, current_speed_left)
    Robot.set_value(MOTOR_ID, V_R, current_speed_right)
