#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
import sys
import termios
import tty
import time

msg = """
Controling TurtleBot3 Waffle via keyboard:
--------------------------------------------
W/S: Increase/Decrease Linear
A/D: Increase/Decrease Angular
Space: Stop quickly
X: Surely stopping 
CTRL-C: Exiting
"""

# Tham số
LIN_VEL_STEP = 0.1
ANG_VEL_STEP = 0.1
LIN_VEL_MAX = 5.0
ANG_VEL_MAX = 2.5

def get_key():
    """Reading from the terminal"""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        key = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return key

def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

def main():
    rospy.init_node('keyboard_ramp_teleop')
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    linear_vel = 0.0
    angular_vel = 0.0
    twist = Twist()
    is_stopped = False  # Biến để theo dõi trạng thái dừng

    print(msg)

    try:
        while not rospy.is_shutdown():
            key = get_key()

            if key == 'w' and not is_stopped:
                linear_vel += LIN_VEL_STEP
                linear_vel = constrain(linear_vel, -LIN_VEL_MAX, LIN_VEL_MAX)
            elif key == 's' and not is_stopped:
                linear_vel -= LIN_VEL_STEP
                linear_vel = constrain(linear_vel, -LIN_VEL_MAX, LIN_VEL_MAX)
            elif key == 'a' and not is_stopped:
                angular_vel += ANG_VEL_STEP
                angular_vel = constrain(angular_vel, -ANG_VEL_MAX, ANG_VEL_MAX)
            elif key == 'd' and not is_stopped:
                angular_vel -= ANG_VEL_STEP
                angular_vel = constrain(angular_vel, -ANG_VEL_MAX, ANG_VEL_MAX)
            elif key == ' ':
                is_stopped = True
                linear_vel = 0.0
                angular_vel = 0.0
                rospy.loginfo("Robot Stop right now...")
            elif key == 'x':
                is_stopped = False
                linear_vel = 0.0
                angular_vel = 0.0
            elif key in ['w', 's', 'a', 'd'] and is_stopped:
                is_stopped = False  # Tiếp tục khi nhấn các phím điều khiển sau khi dừng
            elif key == '\x03':
                break

            twist.linear.x = linear_vel
            twist.angular.z = angular_vel
            pub.publish(twist)

            rospy.loginfo(f"linear: {linear_vel:.2f} m/s, angular: {angular_vel:.2f} rad/s")

    except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
    main()