#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from visualization_msgs.msg import Marker

class UTMVisualizer(Node):
    def __init__(self):
        super().__init__('utm_visualizer')
        
        # 1. 현재 위치(UTM) 구독 
        # (만약 메시지 타입이 PoseStamped라면 Odometry 대신 PoseStamped로 변경해주세요)
        self.utm_sub = self.create_subscription(
            Odometry, 
            '/car1/utm', 
            self.utm_callback, 
            10
        )
        
        # 2. RViz2에 띄울 마커(Marker) 퍼블리셔 생성
        self.marker_pub = self.create_publisher(Marker, '/car1/utm_marker', 10)
        
        self.get_logger().info('UTM Visualizer 시작: 현재 위치를 빨간색 구슬로 표시합니다.')

    def utm_callback(self, msg):
        marker = Marker()
        
        # RViz2 기준 좌표계 설정 (경로를 띄웠던 car1/odom 과 일치시킵니다)
        marker.header.frame_id = 'car1/odom' 
        marker.header.stamp = self.get_clock().now().to_msg()
        
        # 마커의 네임스페이스와 ID (고유값)
        marker.ns = "current_utm"
        marker.id = 0
        
        # 마커의 모양을 구(SPHERE)로 설정
        marker.type = Marker.SPHERE
        marker.action = Marker.ADD
        
        # 위치 입력 (Odometry 메시지에서 추출)
        marker.pose = msg.pose.pose
        
        # 구슬의 크기 설정 (미터 단위, x/y/z 지름)
        marker.scale.x = 0.5  # 50cm
        marker.scale.y = 0.5
        marker.scale.z = 0.5
        
        # 구슬의 색상 설정 (R, G, B, Alpha) -> 빨간색, 불투명도 100%
        marker.color.r = 1.0
        marker.color.g = 0.0
        marker.color.b = 0.0
        marker.color.a = 1.0 
        
        # 마커 유지 시간 (0이면 영구 유지 후 덮어쓰기)
        marker.lifetime.sec = 0
        marker.lifetime.nanosec = 0
        
        self.marker_pub.publish(marker)

def main(args=None):
    rclpy.init(args=args)
    node = UTMVisualizer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()