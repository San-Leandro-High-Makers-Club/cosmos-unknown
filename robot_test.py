# Device IDsDRIVE_CONTROLLER_ID = "6_1491370133845894324"ARM_CONTROLLER_ID = "6_12577161366600381129"LIMIT_SWITCH_ID = ""CENTER_LINE_FOLLOWER_ID = "2_3"LEADING_LINE_FOLLOWER_ID = "2_4"# Which drive motor (a or b) is attached to the right and left wheelsL_DRIVE_MOTOR = 'a'R_DRIVE_MOTOR = 'b'# Which arm motor (a or b) is attached to the base of each armPINCER_MOTOR = 'a'ARM_MOTOR = 'b'TOP_LIMIT_SWITCH = "switch0"BOTTOM_LIMIT_SWITCH = "switch1"ARM_SPEED = 1.0   INVERT_L_DRIVE_MOTOR = TrueINVERT_R_DRIVE_MOTOR = FalseINVERT_PINCER_MOTOR = FalseINVERT_ARM_MOTOR = False     def arm_motors_test():     Robot.set_value(ARM_CONTROLLER_ID, "velocity_" + ARM_MOTOR, ARM_SPEED)     Robot.sleep(5)     Robot.set_value(ARM_CONTROLLER_ID, "velocity_" + ARM_MOTOR, 0)          Robot.sleep(2)          Robot.set_value(ARM_CONTROLLER_ID, "velocity_" + ARM_MOTOR, -ARM_SPEED)     Robot.sleep(5)     Robot.set_value(ARM_CONTROLLER_ID, "velocity_" + ARM_MOTOR, 0)          Robot.sleep(2)         Robot.set_value(ARM_CONTROLLER_ID, "velocity_" + PINCER_MOTOR, ARM_SPEED)     Robot.sleep(5)     Robot.set_value(ARM_CONTROLLER_ID, "velocity_" + PINCER_MOTOR, 0)          Robot.sleep(2)         Robot.set_value(ARM_CONTROLLER_ID, "velocity_" + PINCER_MOTOR, -ARM_SPEED)     Robot.sleep(5)     Robot.set_value(ARM_CONTROLLER_ID, "velocity_" + PINCER_MOTOR, 0)        def autonomous_setup():    passdef autonomous_main():    passdef teleop_setup():    # Set inversions for each motor    Robot.set_value(DRIVE_CONTROLLER_ID, "invert_" + L_DRIVE_MOTOR, INVERT_L_DRIVE_MOTOR)    Robot.set_value(DRIVE_CONTROLLER_ID, "invert_" + R_DRIVE_MOTOR, INVERT_R_DRIVE_MOTOR)    Robot.set_value(ARM_CONTROLLER_ID, "invert_" + PINCER_MOTOR, INVERT_PINCER_MOTOR)    Robot.set_value(ARM_CONTROLLER_ID, "invert_" + ARM_MOTOR, INVERT_ARM_MOTOR)    # Disable PID on each motor due to hardware issues    Robot.set_value(DRIVE_CONTROLLER_ID, "pid_enabled_" + L_DRIVE_MOTOR, False)    Robot.set_value(DRIVE_CONTROLLER_ID, "pid_enabled_" + R_DRIVE_MOTOR, False)    Robot.set_value(ARM_CONTROLLER_ID, "pid_enabled_" + PINCER_MOTOR, False)    Robot.set_value(ARM_CONTROLLER_ID, "pid_enabled_" + ARM_MOTOR, False)    Robot.run(arm_motors_test)def teleop_main():    pass