from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='controller',
            executable='pid_control.py',
            name='pid_control',
            output='screen',

        ),
        Node(
            package='controller',
            executable='supervisor.py',
            name='supervisor',
            output='screen',
        ),
        Node(
            package='controller',
            executable='pure_pursuit.py',
            name='pure_pursuit',
            output='screen',
        ),
    ])