#!/usr/bin/env python3

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    pkg_share = get_package_share_directory('amr_server')
    nav2_share = get_package_share_directory('nav2_bringup')

    default_urdf = os.path.join(pkg_share, 'urdf', 'MicroROS_slam.urdf')
    default_map = os.path.join(pkg_share, 'maps', 'map.yaml')
    default_params = os.path.join(pkg_share, 'params', 'nav2_params.yaml')
    default_rviz = os.path.join(pkg_share, 'rviz', 'nav2_config.rviz')

    use_sim_time = LaunchConfiguration('use_sim_time')
    autostart = LaunchConfiguration('autostart')
    map_yaml = LaunchConfiguration('map')
    params_file = LaunchConfiguration('params_file')
    rviz_config = LaunchConfiguration('rviz_config')
    use_rviz = LaunchConfiguration('use_rviz')
    use_robot_state_publisher = LaunchConfiguration('use_robot_state_publisher')

    with open(default_urdf, 'r', encoding='utf-8') as urdf_file:
        robot_description = urdf_file.read()

    nav2_bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_share, 'launch', 'bringup_launch.py')
        ),
        launch_arguments={
            'namespace': '',
            'use_namespace': 'False',
            'slam': 'False',
            'map': map_yaml,
            'use_sim_time': use_sim_time,
            'params_file': params_file,
            'autostart': autostart,
            'use_composition': 'False',
        }.items(),
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='False',
            description='실기 로봇에서는 false',
        ),
        DeclareLaunchArgument(
            'autostart',
            default_value='True',
            description='Nav2 lifecycle 노드 자동 활성화',
        ),
        DeclareLaunchArgument(
            'map',
            default_value=default_map,
            description='map_server가 읽을 지도 YAML 파일',
        ),
        DeclareLaunchArgument(
            'params_file',
            default_value=default_params,
            description='Nav2 파라미터 YAML 파일',
        ),
        DeclareLaunchArgument(
            'rviz_config',
            default_value=default_rviz,
            description='Nav2 RViz 설정 파일',
        ),
        DeclareLaunchArgument(
            'use_rviz',
            default_value='True',
            description='RViz 실행 여부',
        ),
        DeclareLaunchArgument(
            'use_robot_state_publisher',
            default_value='True',
            description='URDF 고정 TF 발행 여부',
        ),

        # base_footprint -> base_link -> laser_frame / imu_frame
        Node(
            condition=IfCondition(use_robot_state_publisher),
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{
                'use_sim_time': use_sim_time,
                'robot_description': robot_description,
            }],
        ),

        # /odom_raw 메시지로 odom_frame -> base_footprint TF 발행
        Node(
            package='amr_server',
            executable='odom_tf_broadcaster',
            name='odom_tf_broadcaster',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time}],
            remappings=[('odom', '/odom_raw')],
        ),

        # map_server + AMCL + planner/controller/BT navigator 등
        nav2_bringup,

        Node(
            condition=IfCondition(use_rviz),
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time}],
            arguments=['-d', rviz_config],
        ),
    ])