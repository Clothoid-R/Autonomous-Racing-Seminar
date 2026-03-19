#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32
class Supervisor(Node):
    def __init__(self):
        super().__init__('supervisor')

        self.cmd_pub = self.create_publisher(Twist, 'car1/cmd_vel', 10)
        self.linear_sub = self.create_subscription(Float32, 'car1/linear_vel', self.linear_callback, 10)
        self.steering_sub = self.create_subscription(Float32, 'car1/steering_angle', self.steering_callback, 10)
        self.timer = self.create_timer(0.02, self.control_loop)

        self.linear_vel = 0.0
        self.steering_angle = 0.0

    def linear_callback(self, msg):
        
        self.linear_vel = msg.data

    def steering_callback(self, msg):
        self.steering_angle = msg.data
    
    def control_loop(self):
        cmd_msg = Twist()
        cmd_msg.linear.x = self.linear_vel
        cmd_msg.angular.z = 0.0  # No steering control in this example
        self.cmd_pub.publish(cmd_msg)

def main(args=None):
    rclpy.init(args=args)
    supervisor = Supervisor()
    rclpy.spin(supervisor)
    supervisor.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()