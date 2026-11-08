# B2077 角谷猜想
# https://www.luogu.com.cn/problem/B2077
n = int(input())
while n != 1:
    if n % 2 == 1:
        print(f"{n}*3+1={n * 3 + 1}")
        n = n * 3 + 1
    else:
        print(f"{n}/2={n // 2}")
        n = n // 2
print("End")