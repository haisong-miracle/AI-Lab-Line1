# P1046 陶陶摘苹果
# https://www.luogu.com.cn/problem/P1046
apples = list(map(int,input().split()))
h = int(input())
count = 0
for i in apples:
    if i <= h + 30:
        count +=1
print(count)
