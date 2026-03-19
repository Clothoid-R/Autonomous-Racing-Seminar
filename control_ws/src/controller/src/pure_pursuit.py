#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from nav_msgs.msg import Odometry
from nav_msgs.msg import Path

class PurePursuitController(Node):
    def __init__(self):
        super().__init__('pure_pursuit_controller')

        self.cmd_pub = self.create_publisher(Float32, 'car1/steering_angle', 10)
        self.odom_sub = self.create_subscription(Odometry, 'car1/odom', self.odom_callback, 10)
        self.path_sub = self.create_subscription(Path, 'car1/path', self.path_callback, 10)
        
        # ================================================
        # Pure Pursuit parameters
        self.lfd = 1.0 # Look-ahead distance
        # ================================================

        self.odom_msg = Odometry()

    def odom_callback(self, msg):
        self.odom_msg = msg


def main(args=None):
    rclpy.init(args=args)
    pure_pursuit_controller = PurePursuitController()
    rclpy.spin(pure_pursuit_controller)
    pure_pursuit_controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()