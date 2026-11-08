# P1420 最长连续自然数
# https://www.luogu.com.cn/problem/P1420
n = int(input())
a = list(map(int, input().split()))
max_len = 1
current_len = 1
for i in range(1, n):
    if a[i] == a[i - 1] + 1:
        current_len += 1 
    else:
        if current_len > max_len:
            max_len = current_len
        current_len = 1 
if current_len > max_len:
    max_len = current_len

print(max_len)
