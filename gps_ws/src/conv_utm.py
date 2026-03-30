import rclpy
from rclpy.node import Node
from sensor_msgs.msg import NavSatFix
import csv
import math

# 순수 파이썬으로 구현한 UTM 변환 공식 (WGS84 기준)
def latlon_to_utm(lat, lon):
    a = 6378137.0
    eccSquared = 0.00669438002290
    k0 = 0.9996

    ZoneNumber = int((lon + 180) / 6) + 1
    LongOrigin = (ZoneNumber - 1) * 6 - 180 + 3
    LongOriginRad = math.radians(LongOrigin)

    latRad = math.radians(lat)
    lonRad = math.radians(lon)

    eccPrimeSquared = (eccSquared) / (1 - eccSquared)
    N = a / math.sqrt(1 - eccSquared * math.sin(latRad)**2)
    T = math.tan(latRad)**2
    C = eccPrimeSquared * math.cos(latRad)**2
    A = math.cos(latRad) * (lonRad - LongOriginRad)

    M = a * ((1 - eccSquared / 4 - 3 * eccSquared**2 / 64 - 5 * eccSquared**3 / 256) * latRad
             - (3 * eccSquared / 8 + 3 * eccSquared**2 / 32 + 45 * eccSquared**3 / 1024) * math.sin(2 * latRad)
             + (15 * eccSquared**2 / 256 + 45 * eccSquared**3 / 1024) * math.sin(4 * latRad)
             - (35 * eccSquared**3 / 3072) * math.sin(6 * latRad))

    easting = (k0 * N * (A + (1 - T + C) * A**3 / 6
                         + (5 - 18 * T + T**2 + 72 * C - 58 * eccPrimeSquared) * A**5 / 120)
               + 500000.0)

    northing = (k0 * (M + N * math.tan(latRad) * (A**2 / 2 + (5 - T + 9 * C + 4 * C**2) * A**4 / 24
                                                  + (61 - 58 * T + T**2 + 600 * C - 330 * eccPrimeSquared) * A**6 / 720)))
    return easting, northing

class UTMLiveRecorder(Node):
    def __init__(self):
        super().__init__('utm_live_recorder')
        
        # 올려준 토픽 그대로 구독!
        self.subscription = self.create_subscription(
            NavSatFix,
            '/car1/gps/fix',
            self.listener_callback,
            10)
        
        # 결과를 저장할 새 CSV 파일 생성
        self.csv_file = open('/home/user/share/track_utm_live.csv', mode='w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(['easting', 'northing']) # X, Y 헤더 작성
        
        self.get_logger().info('🚗 실시간 UTM 기록을 시작합니다. 트랙을 주행해 주세요! (종료: Ctrl+C)')

    def listener_callback(self, msg):
        lat = msg.latitude
        lon = msg.longitude
        
        # 위도, 경도를 받자마자 UTM 좌표(X, Y)로 변환
        easting, northing = latlon_to_utm(lat, lon)
        
        # 밀리미터(소수점 3자리) 단위까지만 깔끔하게 자르기
        easting = round(easting, 3)
        northing = round(northing, 3)
        
        # 변환된 값을 파일에 쓰고 화면에 출력
        self.csv_writer.writerow([easting, northing])
        self.get_logger().info(f'저장됨: Easting(X) {easting}, Northing(Y) {northing}')

def main(args=None):
    rclpy.init(args=args)
    utm_recorder = UTMLiveRecorder()
    
    try:
        # 네가 원했던 대로 여기서 무한 대기하며 계속 실행됨
        rclpy.spin(utm_recorder)
    except KeyboardInterrupt:
        utm_recorder.get_logger().info('정지 신호 수신. 파일을 안전하게 닫고 종료합니다.')
    finally:
        utm_recorder.csv_file.close() # 종료 시 파일 닫기
        utm_recorder.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()