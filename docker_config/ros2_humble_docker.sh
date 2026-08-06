docker run -it \
  --name yahboomcar \
  --privileged \
  --net=host \
  -e ROS_DOMAIN_ID=20 \
  -v "$(pwd)":/root/shared \
  -v /dev:/dev \
  ros:humble \
  /bin/bash
  