from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='robot_localization',
            executable='navsat_transform_node',
            name='navsat_transform_node',
            output='screen',
            parameters=[{
                # 1. 제어 관련 설정
                'magnetic_declination_radians': 0.0, # 지역별 자기 편각 (서울 기준 약 8.6도 -> 라디안 변환)
                'yaw_offset': 0.0,                  # IMU의 북쪽 방향 오프셋 (보통 90도/pi/2)
                'zero_altitude': True,                 # 고도 무시 여부
                'publish_filtered_gps': True,          # 변환된 GPS 데이터를 다시 퍼블리시할지 여부
                'use_odometry_yaw': True,             # 오도메트리 대신 IMU 데이터 사용 권장
                'wait_for_datum': True,               # 특정 원점 설정을 기다릴지 여부
                'datum': [37.5665, 126.9780, 0.0],
            }],
            remappings=[
                # 실제 토픽 이름에 맞게 매핑 (Gazebo 토픽명 확인 필수)
                ('gps/fix', '/car1/gps/fix'),
                ('odometry/filtered', '/car1/odom'),
                ('odometry/gps', '/car1/utm')
            ]
        ),
        Node(
            package='gps2utm',
            executable='utm_pose_visualize.py',
            name='utm_pose_visualize',
            output='screen',
        ),
    ])