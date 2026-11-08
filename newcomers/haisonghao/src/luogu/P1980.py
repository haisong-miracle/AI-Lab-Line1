# P1980 计数问题
# https://www.luogu.com.cn/problem/P1980
n, x = map(int, input().split())

count = 0

for i in range(1, n + 1):
    temp = i
    while temp > 0:
        if temp % 10 == x:  
            count += 1
        temp //= 10 

print(count)
