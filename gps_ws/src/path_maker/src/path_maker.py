import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry 
import csv
import math
class GPSRecorder(Node):
    def __init__(self):
        super().__init__('gps_recorder')
        # GPS 토픽 이름에 맞게 구독
        self.subscription = self.create_subscription(
            Odometry,
            '/car1/utm',
            self.listener_callback,
            10)
        
        # 결과를 저장할 CSV 파일 생성 (호스트 공유 폴더 경로로 설정하면 편합니다)
        self.csv_file = open('/home/th/Autonomous-Racing-Seminar/gps_ws/src/path_maker/track_gps_waypoints.csv', mode='w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(['x', 'y']) # 헤더 작성
        
        # 이전 좌표 저장 변수
        self.prev_x = None
        self.prev_y = None
        self.min_distance = 0.1 # 저장 기준 거리 (0.1m)

        self.get_logger().info('GPS 기록 시작: 0.1m 이동 시마다 저장합니다.')

    def euclidean_distance(self, x1, y1, x2, y2):
        """
        직교 좌표계에서의 두 점 사이 거리 계산 (피타고라스 정리)
        """
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    def save_data(self, x, y):
        self.csv_writer.writerow([x, y])
        self.csv_file.flush() # 실시간 기록 보장
        self.prev_x = x
        self.prev_y = y

    def listener_callback(self, msg):
        # 소수점 아래 7자리 정도면 매우 정밀함
        curr_x = msg.pose.pose.position.x
        curr_y = msg.pose.pose.position.y

        # 첫 데이터 수신 시 처리
        if self.prev_x is None or self.prev_y is None:
            self.save_data(round(curr_x, 4), round(curr_y, 4))
            return

        # 이전 지점과의 거리 계산 (m 단위)
        distance = self.euclidean_distance(self.prev_x, self.prev_y, curr_x, curr_y)

        # 0.1m 이상 이동했을 때만 저장
        if distance >= self.min_distance:
            self.save_data(round(curr_x, 4), round(curr_y, 4))
            self.get_logger().info(f'저장됨: x {curr_x}, y {curr_y} 이동 거리: {distance:.2f}m -> 저장 완료')

def main(args=None):
    rclpy.init(args=args)
    gps_recorder = GPSRecorder()
    
    try:
        rclpy.spin(gps_recorder)
    except KeyboardInterrupt:
        gps_recorder.get_logger().info('정지 신호 수신. 파일을 닫고 종료합니다.')
    finally:
        gps_recorder.csv_file.close() # 파일 안전하게 닫기
        gps_recorder.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()