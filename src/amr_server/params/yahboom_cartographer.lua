include "map_builder.lua"
include "trajectory_builder.lua"
--001 
options = {
  map_builder = MAP_BUILDER,
  trajectory_builder = TRAJECTORY_BUILDER,

  map_frame = "map",

  -- /imu의 header.frame_id
  tracking_frame = "base_footprint",

  -- 기존 wheel odometry가 odom_frame -> base_footprint를 발행하므로
  -- Cartographer는 map -> odom_frame을 발행
  published_frame = "base_footprint",
  odom_frame = "odom_frame",

  -- 기존 /odom_raw 및 TF를 사용하므로 Cartographer가
  -- odom 프레임을 별도로 만들지 않음
  provide_odom_frame = false,

  publish_frame_projected_to_2d = true,

  -- /odom_raw 사용
  use_odometry = true,

  use_nav_sat = false,
  use_landmarks = false,

  -- /scan 사용
  num_laser_scans = 1,
  num_multi_echo_laser_scans = 0,
  num_subdivisions_per_laser_scan = 1,
  num_point_clouds = 0,

  lookup_transform_timeout_sec = 0.2,

  submap_publish_period_sec = 0.3,
  pose_publish_period_sec = 5e-3,
  trajectory_publish_period_sec = 30e-3,

  rangefinder_sampling_ratio = 1.0,
  odometry_sampling_ratio = 1.0,
  fixed_frame_pose_sampling_ratio = 1.0,
  imu_sampling_ratio = 1.0,
  landmarks_sampling_ratio = 1.0,
}

MAP_BUILDER.use_trajectory_builder_2d = true

-- /scan 스펙
TRAJECTORY_BUILDER_2D.min_range = 0.12
TRAJECTORY_BUILDER_2D.max_range = 8.0
TRAJECTORY_BUILDER_2D.missing_data_ray_length = 3.0

-- /imu 사용
TRAJECTORY_BUILDER_2D.use_imu_data = false

TRAJECTORY_BUILDER_2D.use_online_correlative_scan_matching = true

TRAJECTORY_BUILDER_2D.motion_filter.max_angle_radians =
    math.rad(0.1)

POSE_GRAPH.constraint_builder.min_score = 0.65
POSE_GRAPH.constraint_builder.global_localization_min_score = 0.7

return options
