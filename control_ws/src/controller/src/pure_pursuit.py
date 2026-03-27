#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from nav_msgs.msg import Path, Odometry
from visualization_msgs.msg import Marker  # 마커 발행을 위해 추가

import math

class PurePursuitController(Node):
    def __init__(self):
        super().__init__('pure_pursuit_controller')

        self.cmd_pub = self.create_publisher(Float32, 'car1/steering_angle', 10)
        
        # Look-ahead Point 시각화를 위한 마커 퍼블리셔 추가
        self.marker_pub = self.create_publisher(Marker, 'car1/lookahead_marker', 10)
        
        self.gps_sub = self.create_subscription(Odometry, 'car1/utm', self.utm_callback, 10)
        self.path_sub = self.create_subscription(Path, 'car1/path', self.path_callback, 10)
        self.odom_sub = self.create_subscription(Odometry, 'car1/odom', self.odom_callback, 10) # Odometry 사용 (위치 정보)
        
        # Pure Pursuit parameters
        self.lfd = 2.5 # Look-ahead distance (적절한 값으로 조정 필요)
        self.wheelbase = 1.0 # 차량의 축거
        
        self.path = None
        self.current_utm = Odometry()
        self.current_pose = None

        # GPS 기반 Yaw 계산을 위한 변수들
        self.prev_utm_x = None
        self.prev_utm_y = None
        self.current_yaw = 0.0    
        self.min_dist_for_yaw = 0.01
        self.control_timer = self.create_timer(0.02, self.control_loop) # 50Hz 제어 루프
    def path_callback(self, msg):
        # 경로 수신
        if self.path is None:
            self.path = msg.poses
    
    def odom_callback(self, msg):
        self.current_pose = msg.pose.pose

    def utm_callback(self, msg):
        self.current_utm = msg
        curr_x = msg.pose.pose.position.x
        curr_y = msg.pose.pose.position.y

        # 1. 초기 위치 저장
        if self.prev_utm_x is None or self.prev_utm_y is None:
            self.prev_utm_x = curr_x
            self.prev_utm_y = curr_y
            return

        # 2. 이동 거리 및 Yaw 계산 (GPS-only Heading)
        dx_yaw = curr_x - self.prev_utm_x
        dy_yaw = curr_y - self.prev_utm_y
        dist_yaw = math.sqrt(dx_yaw**2 + dy_yaw**2)

        if dist_yaw >= self.min_dist_for_yaw:
            self.current_yaw = math.atan2(dy_yaw, dx_yaw)
            self.prev_utm_x = curr_x
            self.prev_utm_y = curr_y
        
    def findLookaheadPoint(self):
        if not self.path:
            return None

        # 1. 차량의 현재 위치
        cx = self.current_utm.pose.pose.position.x
        cy = self.current_utm.pose.pose.position.y

        # 2. 경로에서 가장 가까운 점(Nearest Point) 찾기
        nearest_idx = 0
        min_dist = float('inf')

        for i, pose_stamped in enumerate(self.path):
            pt = pose_stamped.pose.position
            dist = math.hypot(pt.x - cx, pt.y - cy)

            if dist < min_dist:
                min_dist = dist
                nearest_idx = i

        # 3. 가장 가까운 점 이후부터 거리를 누적하며 Look-ahead Point 찾기
        accumulated_dist = 0.0

        for i in range(nearest_idx + 1, len(self.path)):
            p1 = self.path[i - 1].pose.position
            p2 = self.path[i].pose.position

            # 두 웨이포인트 사이의 거리 계산
            segment_len = math.hypot(p2.x - p1.x, p2.y - p1.y)
            accumulated_dist += segment_len

            # 누적 거리가 전방 주시 거리(lfd)를 넘어서는 순간의 점을 반환 (선형보간 생략)
            if accumulated_dist >= self.lfd:
                return p2

        # 4. 경로가 너무 짧아서 lfd에 도달하지 못하면 가장 마지막 점 반환
        return self.path[-1].pose.position

    def publish_lookahead_marker(self, target_point):
        marker = Marker()
        # RViz Fixed Frame과 일치시킵니다 (path_publisher에서 설정한 frame_id와 동일하게)
        marker.header.frame_id = 'car1/odom' 
        marker.header.stamp = self.get_clock().now().to_msg()
        
        marker.ns = 'lookahead_point'
        marker.id = 1
        
        # 마커 모양을 구(SPHERE)로 설정
        marker.type = Marker.SPHERE
        marker.action = Marker.ADD
        
        # 목표점 좌표 입력
        marker.pose.position.x = target_point.x
        marker.pose.position.y = target_point.y
        marker.pose.position.z = 0.0
        marker.pose.orientation.w = 1.0
        
        # 마커 크기 설정 (x, y, z 지름, 0.4m 크기)
        marker.scale.x = 0.4
        marker.scale.y = 0.4
        marker.scale.z = 0.4
        
        # 파란색 (R:0, G:0, B:1) 불투명도 100%
        marker.color.r = 0.0
        marker.color.g = 0.0
        marker.color.b = 1.0
        marker.color.a = 1.0 
        
        self.marker_pub.publish(marker)

    def computeSteeringAngle(self, target_point):
        
        yaw = self.current_yaw
        self.get_logger().info(f'Current Yaw: {math.degrees(yaw):.2f} degrees')
        # 차량 기준의 상대 좌표로 변환 (Global to Local)
        dx = target_point.x - self.current_utm.pose.pose.position.x
        dy = target_point.y - self.current_utm.pose.pose.position.y

        # 차량 진행 방향을 기준으로 한 상대적 위치
        local_x = dx * math.cos(-yaw) - dy * math.sin(-yaw)
        local_y = dx * math.sin(-yaw) + dy * math.cos(-yaw)

        # 알파(alpha) 계산: 차량 헤딩과 목표점 사이의 각도
        alpha = math.atan2(local_y, local_x)

        # Pure Pursuit 공식 적용
        # delta = atan(2 * L * sin(alpha) / Ld)
        steering_angle = math.atan2(2.0 * self.wheelbase * math.sin(alpha), self.lfd)
        
        return steering_angle

    def control_loop(self):
        # 경로가 없으면 제어 종료
        if self.path is None:
            return

        # 3. 목표점(Look-ahead Point) 찾기
        target_point = self.findLookaheadPoint()
        out_msg = Float32()
        
        if target_point:
            self.publish_lookahead_marker(target_point)
            
            # 4. 조향각 계산
            steering_angle = self.computeSteeringAngle(target_point)
            print(f"steering_angle: {steering_angle}")
            out_msg.data = steering_angle
            self.cmd_pub.publish(out_msg)
        else:
            self.get_logger().warn('No valid look-ahead point found.')
            out_msg.data = 0.0
            self.cmd_pub.publish(out_msg)
            
def main(args=None):
    rclpy.init(args=args)
    pure_pursuit_controller = PurePursuitController()
    try:
        rclpy.spin(pure_pursuit_controller)
    except KeyboardInterrupt:
        pass
    finally:
        pure_pursuit_controller.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()