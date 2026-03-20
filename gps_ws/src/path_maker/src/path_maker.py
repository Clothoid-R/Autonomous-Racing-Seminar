import rclpy
from rclpy.node import Node
from sensor_msgs.msg import NavSatFix
import csv

class GPSRecorder(Node):
    def __init__(self):
        super().__init__('gps_recorder')
        # GPS 토픽 이름에 맞게 구독
        self.subscription = self.create_subscription(
            NavSatFix,
            '/car1/gps/fix',
            self.listener_callback,
            10)
        
        # 결과를 저장할 CSV 파일 생성 (호스트 공유 폴더 경로로 설정하면 편합니다)
        self.csv_file = open('gps_ws/src/path_maker/track_gps_waypoints.csv', mode='w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(['latitude', 'longitude']) # 헤더 작성
        
        self.get_logger().info(':red_car: GPS 기록을 시작합니다. 트랙을 주행해 주세요! (종료: Ctrl+C)')

    def listener_callback(self, msg):
        # 소수점 아래 7자리 정도면 매우 정밀함
        lat = round(msg.latitude, 7)
        lon = round(msg.longitude, 7)
        
        self.csv_writer.writerow([lat, lon])
        self.get_logger().info(f'저장됨: 위도 {lat}, 경도 {lon}')

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