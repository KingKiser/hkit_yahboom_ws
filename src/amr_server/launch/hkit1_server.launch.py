#!/usr/bin/env python3

import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # 1. 패키지 이름 설정: 우리가 만든 패키지 이름을 변수로 지정
    package_name = 'amr_server'
    # 패키지가 설치된 실제 경로(공유 디렉토리)를 가져옵니다.
    pkg_share = get_package_share_directory(package_name)

    # 2. 경로 설정: 각 폴더에 들어있는 설정 파일들의 절대 경로를 생성합니다.
    cartographer_config = os.path.join(pkg_share, 'params') # SLAM 설정 폴더 경로
    lua_config = 'yahboom_cartographer.lua' # SLAM 설정 파일 이름

    # 6. Cartographer 노드: 라이다 데이터를 분석하여 로봇의 현재 위치를 추정(SLAM)
    cartographer_cmd = Node(
        package='cartographer_ros',
        executable='cartographer_node',
        output='screen',
        parameters=[{'use_sim_time': False}], # 실제 시간 사용
        arguments=[
            '-configuration_directory', cartographer_config, # 설정 파일이 들어있는 폴더 경로
            '-configuration_basename', lua_config             # 실제 사용할 .lua 파일 이름
        ],
        remappings=[
        ('scan', '/hkit1/scan'),
        ('imu', '/hkit1/imu'),
        ('odom', '/hkit1/odom_raw'),
        ]
    )

    # 7. Occupancy Grid 노드: SLAM 결과를 우리가 볼 수 있는 흑백 지도(Grid Map)로 변환
    occupancy_grid_cmd = Node(
        package='cartographer_ros',
        executable='cartographer_occupancy_grid_node',
        output='screen',
        parameters=[{'use_sim_time': False}],
        arguments=['-resolution', '0.05', '-publish_period_sec', '1.0'] # 5cm 해상도로 1초마다 지도 갱신
    )
    odom_tf_cmd = Node(
    package='amr_server',
    executable='odom_tf_broadcaster',
    output='screen'
    )

    laser_static_tf_cmd = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=[
            '0', '0', '0.15',
            '0', '0', '0',
            'base_footprint',
            'laser_frame'
        ]
    )

    imu_static_tf_cmd = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=[
            '0', '0', '0.10',
            '0', '0', '0',
            'base_footprint',
            'imu_frame'
        ]
    )


    # 실행할 명령 목록(LaunchDescription) 생성 및 노드 추가
    ld = LaunchDescription()

    ld.add_action(cartographer_cmd) # SLAM 엔진 켜기
    ld.add_action(occupancy_grid_cmd) # 지도 변환기 켜기
    ld.add_action(odom_tf_cmd) 
    ld.add_action(laser_static_tf_cmd) 
    ld.add_action(imu_static_tf_cmd) 

    return ld
