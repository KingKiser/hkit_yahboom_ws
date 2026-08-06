# yahboom Docker 셋팅 가이드

---

## 📖 Notes

- [yahboom 공식사이트 주소](https://www.yahboom.net/study/MicroROS-Pi5)
- 제어기 보드와 연동 방법은 위 주소에서 가이드 된 대로 reset 버튼을 눌러 config_robot.py를 실행하시면 됩니다
- start_agent_rpi5.sh 는 기존에 공식에서는 rm 으로 도커를 1회성으로 사용하지만 첨부된 sh는 1회성이 아닙니다
- ros2_humble_docker.sh는 카메라 노드를 실행하기 위한 도커 컨테이너 생성입니다

---

### 초기 라즈베리파이 설정

- vnc나 ssh연결 및 기본적인 보드 이미지 설치는 생략합니다

---
### 팁 라즈베리파이에 vscode를 설치하면 꽤 편하다

```bash
sudo apt update
sudo apt install code
```

![arona](images/aronaddabong.png)

---

```bash
sudo apt-get update
sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

sudo usermod -aG docker $user_name

sudo reboot
```
- 재부팅 후에 다시

```bash

sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) \
  signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

sudo usermod -aG docker $user_name

sudo reboot
```
- 재부팅 후 제어기 리셋 버튼 눌러서 부저 소리 들리면

```bash
python3 config_robot.py

sudo code /etc/udev/rules.d/99-yahboom.rules
```
- vscode로 99-yahboom.rules를 생성하여 값을 하단의 값을 넣는다

```bash
KERNEL=="ttyUSB[0-9]*", MODE="0666"
KERNEL=="ttyACM[0-9]*", MODE="0666"
KERNEL=="video[0-9]*", MODE="0666"
```
- 이후 vscode를 이용해 저장 후 해당 rules를 적용한다

```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
sudo reboot
```
- 재부팅 후 아래 sh 실행해서 제어기 MCU와 접속 확인할것

```bash
sh start_agent_rpi5.sh
```
- 다른 터미널에서 컨테이너 새로 만듦

```bash
sh ros2_humble_docker.sh
```

- 새로 만든 컨테이너 yahbommcar에 카메라 관련 내용 설치

```bash
docker exec -it yahboomcar bash

apt update
apt install -y ros-humble-usb-cam
source /opt/ros/humble/setup.bash

echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc

sudo apt install ros-humble-compressed-image-transport

```
- 이후 해당 컨테이너에서 다음과 같이 카메라 노드 실행해야 병목이 없을 것임 구독도 image_raw/compresed로 할것


```bash
ros2 run usb_cam usb_cam_node_exe --ros-args \
  -p video_device:=/dev/video0 \
  -p image_width:=640 \
  -p image_height:=480 \
  -p framerate:=30.0 \
  -p pixel_format:=mjpeg2rgb

```

- 서버에서는 다음과 같은 것을 설치하여 rqt에서 모니터링 할 것


```bash
sudo apt update
sudo apt install --reinstall \
  ros-humble-rqt-image-view \
  ros-humble-image-transport-plugins
```
---

- rqt 실행 시 카메라 덤프될 경우

```bash
rqt --clear-config
```