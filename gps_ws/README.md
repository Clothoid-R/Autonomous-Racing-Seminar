# GPS Seminar

## 필수!! GPS2UTM 키기
GPS to UTM 변환하는 코드 실행
```bash
ros2 launch gps2utm gps2utm.launch.py
```

## 경로 따기
시뮬레이터 폴더에서 키보드 제어 켜기 

```bash
python3 path_maker.py
```
경로 기록해주는 코드 실행

##1. 가제보를 실행시킨다.
gz sim -r ~/Autonomous-Racing-Simulator/simulate_ws/src/server/map/racemap.sdf 

##2. 차량을 스폰시킨다.
ros2 launch server spawn_car.launch.py

##3. 차량을 움직일 수 있게 파이썬 코드를 실행시킨다..
python3 src/server/src/key_teleop.py

##4. 차량에 설치된 GPS를 이용하여 맵의 경로를 추출한다.
python3 /home/user/share/Autonomous-Racing-Seminar/gps_ws/src/gps_record.py



## UTM

##1. 가제보를 실행시킨다.
gz sim -r ~/Autonomous-Racing-Simulator/simulate_ws/src/server/map/racemap.sdf 

##2. 차량을 스폰시킨다.
ros2 launch server spawn_car.launch.py

##3. 차량을 움직일 수 있게 파이썬 코드를 실행시킨다..
python3 src/server/src/key_teleop.py

##4. 차량에 설치된 GPS를 이용하여 맵의 UTM 경로를 추출한다.
Python3 /home/user/share/Autonomous-Racing-Seminar/gps_ws/src/conv_utm.py
