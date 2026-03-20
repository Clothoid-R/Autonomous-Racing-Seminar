#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from nav_msgs.msg import Odometry, Path
import math

class PurePursuitController(Node):
    def __init__(self):
        super().__init__('pure_pursuit_controller')

        self.cmd_pub = self.create_publisher(Float32, 'car1/steering_angle', 10)
        self.odom_sub = self.create_subscription(Odometry, 'car1/odom', self.odom_callback, 10)
        self.path_sub = self.create_subscription(Path, 'car1/path', self.path_callback, 10)
        
        # Pure Pursuit parameters
        self.lfd = 2.0  # Look-ahead distance (적절한 값으로 조정 필요)
        self.wheelbase = 1.0 # 차량의 축거
        
        self.path = None
        self.current_pose = None

    def path_callback(self, msg):
        # 경로 수신
        self.path = msg.poses

    def odom_callback(self, msg):
        self.current_pose = msg.pose.pose
        
        if self.path is None:
            return

        # 1. 목표점(Look-ahead Point) 찾기
        target_point = self.findLookaheadPoint()
        msg = Float32()
        
        if target_point:
            # 2. 조향각 계산
            steering_angle = self.computeSteeringAngle(target_point)
            
            # 3. 퍼블리시
            msg.data = steering_angle
            self.cmd_pub.publish(msg)
        else:
            self.get_logger().warn('No valid look-ahead point found.')
            msg.data = 0.0
            self.cmd_pub.publish(msg)


    def findLookaheadPoint(self):
        if not self.path:
            return None

        for pose_stamped in self.path:
            dx = pose_stamped.pose.position.x - self.current_pose.position.x
            dy = pose_stamped.pose.position.y - self.current_pose.position.y
            dist = math.sqrt(dx**2 + dy**2)
            
            # 현재 위치에서 전방 주시 거리(lfd)와 가장 유사한 점 선택
            if dist >= self.lfd:
                return pose_stamped.pose.position
        
        return self.path[-1].pose.position # 경로 끝에 도달하면 마지막 점 반환

    def computeSteeringAngle(self, target_point):
        # 차량의 현재 yaw(헤딩) 계산 (Quaternion -> Euler)
        q = self.current_pose.orientation
        siny_cosp = 2 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1 - 2 * (q.y * q.y + q.z * q.z)
        yaw = math.atan2(siny_cosp, cosy_cosp)

        # 차량 기준의 상대 좌표로 변환 (Global to Local)
        dx = target_point.x - self.current_pose.position.x
        dy = target_point.y - self.current_pose.position.y
        
        # 차량 진행 방향을 기준으로 한 상대적 위치
        local_x = dx * math.cos(-yaw) - dy * math.sin(-yaw)
        local_y = dx * math.sin(-yaw) + dy * math.cos(-yaw)

        # 알파(alpha) 계산: 차량 헤딩과 목표점 사이의 각도
        alpha = math.atan2(local_y, local_x)

        # Pure Pursuit 공식 적용
        # delta = atan(2 * L * sin(alpha) / Ld)
        steering_angle = math.atan2(2.0 * self.wheelbase * math.sin(alpha), self.lfd)
        
        return steering_angle

def main(args=None):
    rclpy.init(args=args)
    pure_pursuit_controller = PurePursuitController()
    rclpy.spin(pure_pursuit_controller)
    pure_pursuit_controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()