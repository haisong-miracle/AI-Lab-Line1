# B3736 [信息与未来 2018] 最大公约数
# https://www.luogu.com.cn/problem/B3736
x, y, z = map(int, input().split())
min_num = min(x, y, z)
for g in range(min_num, 0, -1):
    if x % g == 0 and y % g == 0 and z % g == 0:
        print(g)
        break