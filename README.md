# hkit_yahboom_ws

> 한국IT교육원 자율주행 피지컬 AI 반 교구제 사용 예제

**Version:** v1  
**Last Updated:** 2026.08.06  
**Author:** 박승휘

---

## ✅ Yahboom slam, nav2 패키지

- 기존 공식 사이트에 있는 slam이나 nav는 너무 복잡해서 기본 센서 데이터로만 구현했음 강의용으로 최소한의 셋팅이니 참고하고 slam 셋서 데이터 보정은 알아서

![joseock](images/joseock.png)

---

### Slam 실행

```bash
colcon build
source install/setup.bash
ros2 launch amr_server server_slam.launch.py
```

### Nav2 실행

```bash
colcon build
source install/setup.bash
ros2 launch amr_server server_nav2.launch.py
```

---

## 📖 Notes

- docker_config 폴더는 yahboom 라즈베리파이 내부에서 도커 셋팅하기 위해 첨부한 파일입니다
- yahboom 도커 내부 셋팅은 해당 폴더의 README를 참고해주세요

![kimseongmo](images/kimsungmo.webp)

- 힘들었다

![kiriko](images/kiriko.png)

- 수업 준비하느라 고생했으면 팔로우 해주세요

![arona](images/aronaddabong.png)