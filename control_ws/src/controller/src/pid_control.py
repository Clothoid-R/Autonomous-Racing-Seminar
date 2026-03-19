#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from nav_msgs.msg import Odometry

import time

class PIDController(Node):
    def __init__(self):
        super().__init__('pid_controller')

        self.cmd_pub = self.create_publisher(Float32, 'car1/linear_vel', 10)
        self.vel_sub = self.create_subscription(Odometry, 'car1/odom', self.odom_callback, 10)

        self.target_vel = 1.0

        # ================================================
        # PID parameters
        self.kp = 1.0
        self.ki = 0.0
        self.kd = 0.0
        # ================================================

        self.odom_msg = Odometry()

        self.timer = self.create_timer(0.02, self.loop)

    def odom_callback(self, msg):
        self.odom_msg = msg

    def pid_calculate(self):
        current_vel = self.odom_msg.twist.twist.linear.x
        
        error = self.target_vel - current_vel

        # Implement PID control logic here (not fully implemented for simplicity)
        control_signal = self.kp * error

        return control_signal
    
    def loop(self):
        control_signal = self.pid_calculate()
        # Use the control signal to publish velocity commands
        cmd_msg = Float32()
        cmd_msg.data = control_signal
        self.cmd_pub.publish(cmd_msg)

def main(args=None):
    rclpy.init(args=args)
    pid_controller = PIDController()
    rclpy.spin(pid_controller)
    pid_controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()