DRIVE_CONTROLLER_ID = "6_1491370133845894324"

L_DRIVE_MOTOR = 'a'
R_DRIVE_MOTOR = 'b'

INVERT_L_DRIVE_MOTOR = True
INVERT_R_DRIVE_MOTOR = False

AUTONOMOUS_SPEED = 1.0


def autonomous_setup():
    Robot.set_value(DRIVE_CONTROLLER_ID, "invert_" + L_DRIVE_MOTOR, INVERT_L_DRIVE_MOTOR)
    Robot.set_value(DRIVE_CONTROLLER_ID, "invert_" + R_DRIVE_MOTOR, INVERT_R_DRIVE_MOTOR)
    
    Robot.set_value(DRIVE_CONTROLLER_ID, "pid_enabled_" + L_DRIVE_MOTOR, False)
    Robot.set_value(DRIVE_CONTROLLER_ID, "pid_enabled_" + R_DRIVE_MOTOR, False)
    
    Robot.set_value(DRIVE_CONTROLLER_ID, "enc_" + L_DRIVE_MOTOR, 0)
    Robot.set_value(DRIVE_CONTROLLER_ID, "enc_" + R_DRIVE_MOTOR, 0)
    
    drive_forward(5000)


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


def teleop_setup():
    pass


def teleop_main():
    pass
