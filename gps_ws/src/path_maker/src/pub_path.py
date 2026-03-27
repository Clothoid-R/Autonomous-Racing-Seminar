#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped
import csv
import os

class PathPublisher(Node):
    def __init__(self):
        super().__init__('path_publisher')
        
        # Publisher 설정
        self.path_pub = self.create_subscription = self.create_publisher(Path, '/car1/path', 10)
        
        # 타이머 설정 (예: 1초마다 한 번씩 전체 경로 발행)
        self.timer = self.create_timer(1.0, self.publish_path)
        
        # CSV 파일 경로 (본인의 경로에 맞게 수정하세요)
        self.csv_file_path = '/home/th/Autonomous-Racing-Seminar/gps_ws/src/path_maker/track_gps_waypoints.csv' 
        # 첫 번째 좌표를 저장할 변수 (오프셋용)
        self.origin_lat = None
        self.origin_lon = None
        self.get_logger().info('Path Publisher가 시작되었습니다.')

    def publish_path(self):
            if not os.path.exists(self.csv_file_path):
                return

            path_msg = Path()
            path_msg.header.frame_id = 'car1/odom' # RViz Fixed Frame과 일치시킬 것
            path_msg.header.stamp = self.get_clock().now().to_msg()

            with open(self.csv_file_path, mode='r') as f:
                reader = csv.DictReader(f)
                for i, row in enumerate(reader):
                    x = float(row['x'])
                    y = float(row['y'])

                    # 첫 번째 좌표를 원점(0,0)으로 설정
                    if i == 0:
                        self.origin_x = x
                        self.origin_y = y

                    pose = PoseStamped()
                    pose.header = path_msg.header
                    
                    # GPS 1도는 약 111,000m입니다. 
                    # 위경도 차이에 111000을 곱해 미터 단위로 근사치 변환
                    pose.pose.position.x = x # 원점으로부터의 상대 좌표
                    pose.pose.position.y = y# 한국 위도 기준 경도 1도 거리
                    # pose.pose.position.x = lat
                    # pose.pose.position.y = lon
                    pose.pose.position.z = 0.0
                    pose.pose.orientation.w = 1.0
                    
                    path_msg.poses.append(pose)
            
            self.path_pub.publish(path_msg)
            self.get_logger().info(f'Published {len(path_msg.poses)} points to RViz')

def main(args=None):
    rclpy.init(args=args)
    node = PathPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()