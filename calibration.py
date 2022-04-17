DRIVE_CONTROLLER_ID = "6_1491370133845894324"

L_DRIVE_MOTOR = 'a'
R_DRIVE_MOTOR = 'b'

INVERT_L_DRIVE_MOTOR = True
INVERT_R_DRIVE_MOTOR = False

AUTONOMOUS_SPEED = 1.0

counter = 0


def autonomous_setup():
    Robot.set_value(DRIVE_CONTROLLER_ID, "invert_" + L_DRIVE_MOTOR, INVERT_L_DRIVE_MOTOR)
    Robot.set_value(DRIVE_CONTROLLER_ID, "invert_" + R_DRIVE_MOTOR, INVERT_R_DRIVE_MOTOR)
    
    Robot.set_value(DRIVE_CONTROLLER_ID, "pid_enabled_" + L_DRIVE_MOTOR, False)
    Robot.set_value(DRIVE_CONTROLLER_ID, "pid_enabled_" + R_DRIVE_MOTOR, False)
    
    Robot.set_value(DRIVE_CONTROLLER_ID, "enc_" + L_DRIVE_MOTOR, 0)
    Robot.set_value(DRIVE_CONTROLLER_ID, "enc_" + R_DRIVE_MOTOR, 0)


def autonomous_main():
    global counter
    if counter == 0:
        counter += 1
        drive_forward(5000)


def teleop_setup():
    pass


def teleop_main():
    pass


def drive_forward(distance: int, speed=AUTONOMOUS_SPEED, tolerance=34) -> None:
    """Drive in a straight line for the specified distance, then stop

    :param distance: the distance to drive (as an encoder value). If negative, drive in reverse.
    :param speed: the speed at which to primarily drive. If extremely low, simply return immediately.
    :param tolerance: the maximum distance (as an encoder value) by which it is acceptable to deviate from the specified
        distance. Defaults to 34, which is about a 1 cm travel distance for the robot.
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

    initial_left_motor_position: int = abs(Robot.get_value(DRIVE_CONTROLLER_ID, "enc_" + L_DRIVE_MOTOR))
    initial_right_motor_position: int = abs(Robot.get_value(DRIVE_CONTROLLER_ID, "enc_" + R_DRIVE_MOTOR))

    def left_motor_distance_travelled():
        return abs(Robot.get_value(DRIVE_CONTROLLER_ID, "enc_" + L_DRIVE_MOTOR)) - initial_left_motor_position

    def right_motor_distance_travelled():
        return abs(Robot.get_value(DRIVE_CONTROLLER_ID, "enc_" + R_DRIVE_MOTOR)) - initial_right_motor_position

    def average_distance_travelled():
        return int((left_motor_distance_travelled() + right_motor_distance_travelled()) / 2)

    while abs(distance) - average_distance_travelled() > 170:
        Robot.set_value(DRIVE_CONTROLLER_ID, "velocity_" + L_DRIVE_MOTOR, speed)
        Robot.set_value(DRIVE_CONTROLLER_ID, "velocity_" + R_DRIVE_MOTOR, speed)

    reduced_speed = 0.15
    if distance < 0:
        reduced_speed *= -1
    while abs(distance) - average_distance_travelled() > tolerance:
        Robot.set_value(DRIVE_CONTROLLER_ID, "velocity_" + L_DRIVE_MOTOR, reduced_speed)
        Robot.set_value(DRIVE_CONTROLLER_ID, "velocity_" + R_DRIVE_MOTOR, reduced_speed)

    Robot.set_value(DRIVE_CONTROLLER_ID, "velocity_" + L_DRIVE_MOTOR, 0)
    Robot.set_value(DRIVE_CONTROLLER_ID, "velocity_" + R_DRIVE_MOTOR, 0)

    if abs(distance) + tolerance < average_distance_travelled():
        adjustment_distance = average_distance_travelled() - distance
        drive_forward(-adjustment_distance, 0.5 * speed, tolerance)
