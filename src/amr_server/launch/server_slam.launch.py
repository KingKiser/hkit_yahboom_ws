#!/usr/bin/env python3
#001
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    pkg_share = get_package_share_directory('amr_server')

    urdf_path = os.path.join(pkg_share, 'urdf', 'MicroROS_slam.urdf')
    rviz_config_path = os.path.join(pkg_share, 'rviz', 'spb_urdf_map.rviz')
    cartographer_config_dir = os.path.join(pkg_share, 'params')
    cartographer_config_file = 'yahboom_cartographer.lua'

    use_sim_time = LaunchConfiguration('use_sim_time')

    with open(urdf_path, 'r', encoding='utf-8') as urdf_file:
        robot_description = urdf_file.read()

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='실제 기기에서는 false를 사용합니다.',
        ),

        # URDF의 고정 조인트를 통해
        # base_footprint -> base_link -> laser_frame / imu_frame TF 발행
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{
                'use_sim_time': use_sim_time,
                'robot_description': robot_description,
            }],
        ),

        # /odom_raw 메시지를 odom_frame -> base_footprint TF로 변환하는 사용자 노드
        Node(
            package='amr_server',
            executable='odom_tf_broadcaster',
            name='odom_tf_broadcaster',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time}],
            remappings=[('odom', '/odom_raw')],
        ),

        # yahboom_cartographer.lua 기준:
        # map -> odom_frame은 Cartographer가 발행하고,
        # odom_frame -> base_footprint는 위 odom_tf_broadcaster가 발행
        Node(
            package='cartographer_ros',
            executable='cartographer_node',
            name='cartographer_node',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time}],
            arguments=[
                '-configuration_directory', cartographer_config_dir,
                '-configuration_basename', cartographer_config_file,
            ],
            remappings=[
                ('scan', '/scan'),
                ('odom', '/odom_raw'),
            ],
        ),

        Node(
            package='cartographer_ros',
            executable='cartographer_occupancy_grid_node',
            name='cartographer_occupancy_grid_node',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time}],
            arguments=[
                '-resolution', '0.05',
                '-publish_period_sec', '1.0',
            ],
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time}],
            arguments=['-d', rviz_config_path],
        ),
    ])
