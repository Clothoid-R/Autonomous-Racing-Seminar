leo6930
leo6930.
온라인

#localization 채널의 시작이에요. 
김건호 — 오후 6:01
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import NavSatFix
import csv
import math

conv_utm.py
4KB
import csv
import math
import matplotlib.pyplot as plt

R = 6378137.0

gps_track.py
1KB
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import NavSatFix
import csv

class GPSRecorder(Node):

record_gps.py
2KB
유태현 — 오후 6:02
이사람은 왜여기다가 올림?
ㅋㅋㅋㅋㅋㅋ
김건호 — 오후 6:02
여기가 편해~
유태현 — 오후 6:02
깃헙에
올리라니깐
김건호 — 오후 6:02
음
어디 브랜치에
푸쉬할지
모르겠음
유태현 — 오후 6:03
메인 브랜치에
해
메인에
형 gps_ws
내가 만들어놧잖아
그 거기에 path_maker는 내가 만들어놓은거 잇음
김건호 — 오후 6:03
ㅇㅋ
유태현 — 오후 6:03
utm은 난 그 라이브러리 갖다 썼음
보면 알듯
김건호 — 오후 6:03
그랴?
라이브러리
유태현 — 오후 6:03
ㅇㅇㅇ
김건호 — 오후 6:03
안되서 그냥 계산하는걸로했는데
그럼 너꺼 써야겠네
유태현 — 오후 6:04
ㅇㅇ utm토픽으로 나옴
한번 코드 봐봐
자기 처음 위치를 원점으로 잡아서 0,0부터 시작할거야
x,y = 0,0 으로
김건호 — 오후 6:06
깃 클론 어디로 했음?
뭐야 왜 영어가 안쳐저
유태현 — 오후 6:06
?
ㅋㅋㅋㅋ
김건호 — 오후 6:06
그
유태현 — 오후 6:06
깃클론은 아무대나 해도 될텐데
김건호 — 오후 6:06
그랴?
유태현 — 오후 6:06
https://github.com/Clothoid-R/Autonomous-Racing-Seminar.git
GitHub
GitHub - Clothoid-R/Autonomous-Racing-Seminar: This project is an a...
This project is an autonomous racing simulator for Clothoid-R seminars. - Clothoid-R/Autonomous-Racing-Seminar
GitHub - Clothoid-R/Autonomous-Racing-Seminar: This project is an a...
김건호 — 오후 6:06
그럼 시뮬 폴더에
불러와야겠다
유태현 — 오후 6:06
이거 받고 gps_ws 폴더 내에서 형은 놀면 돼
아 그렇게 한다고??
ㅋㅋㅋㅋ
둘이 따로
하는게 나을거야
김건호 — 오후 6:07
따로따로?
ㅇㅋ
유태현 — 오후 6:07
ㅇㅇㅇㅇ
귣
나 형꺼 세미나 파일에 자료 안넣어놨다
김건호 — 오후 6:07
ㄱㅊ
유태현 — 오후 6:07
형 따로 ppt그때 만든거 잇지?
김건호 — 오후 6:07
내가 넣어놓을게
ㅇㅇ
유태현 — 오후 6:07
ㅇㅋ
﻿
import csv
import math
import matplotlib.pyplot as plt

R = 6378137.0

lats = []
lons = []

with open('/home/user/share/track_gps_waypoints.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        lats.append(float(row[0]))
        lons.append(float(row[1]))

lat0 = lats[0]
lon0 = lons[0]

x_coords = []
y_coords = []

for lat, lon in zip(lats, lons):
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)
    lat0_rad = math.radians(lat0)
    lon0_rad = math.radians(lon0)

    x = R * math.cos(lat0_rad) * (lon_rad - lon0_rad)
    y = R * (lat_rad - lat0_rad)

    x_coords.append(x)
    y_coords.append(y)

plt.figure(figsize=(8, 8))
plt.plot(x_coords, y_coords, marker='.', linestyle='-', color='b')
plt.plot(x_coords[0], y_coords[0], marker='o', color='r', markersize=10, label='Start')
plt.title('Racing Track XY Map')
plt.xlabel('X meters')
plt.ylabel('Y meters')
plt.grid(True)
plt.legend()
plt.axis('equal')
plt.show()
gps_track.py
1KB