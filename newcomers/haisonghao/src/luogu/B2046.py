# B2046 骑车与走路
# https://www.luogu.com.cn/problem/B2046
s = float(input())
bike_time = 50 + s / 3.0
walk_time = s / 1.2
if bike_time < walk_time:
    print("Bike")
elif bike_time > walk_time:
    print("Walk")
else:
    print("All")
