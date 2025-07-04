#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
import sys, select, termios, tty

def get_key():
    settings = termios.tcgetattr(sys.stdin)
    try:
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            key = sys.stdin.read(1)
        else:
            key = ''
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def teleop():
    pub = rospy.Publisher('/vehicle/cmd_vel', Twist, queue_size=10)
    rospy.init_node('teleop_vehicle', anonymous=True)
    rate = rospy.Rate(10) # 10 Hz

    linear_speed = 0.0
    angular_speed = 0.0
    max_linear_speed = 5.0  # m/s
    max_angular_speed = 1.0  # rad/s

    while not rospy.is_shutdown():
        key = get_key()
        twist = Twist()

        if key == 'w':
            linear_speed = min(linear_speed + 0.1, max_linear_speed)
        elif key == 's':
            linear_speed = max(linear_speed - 0.1, -max_linear_speed)
        elif key == 'a':
            angular_speed = max(angular_speed - 0.1, -max_angular_speed)
        elif key == 'd':
            angular_speed = min(angular_speed + 0.1, max_angular_speed)
        elif key == ' ':
            linear_speed = 0.0
            angular_speed = 0.0
        else:
            if key == '\x03':  # Ctrl+C
                break

        twist.linear.x = linear_speed
        twist.angular.z = angular_speed
        pub.publish(twist)

        rate.sleep()

if __name__ == '__main__':
    try:
        teleop()
    except rospy.ROSInterruptException:
        pass