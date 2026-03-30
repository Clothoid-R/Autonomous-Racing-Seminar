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

plt.figure(figsize=8, 8)
plt.plot(x_coords, y_coords, marker='.', linestyle='-', color='b')
plt.plot(x_coords[0], y_coords[0], marker='o', color='r', markersize=10, label='Start')
plt.title('Racing Track XY Map')
plt.xlabel('X meters')
plt.ylabel('Y meters')
plt.grid(True)
plt.legend()
plt.axis('equal')
plt.show()