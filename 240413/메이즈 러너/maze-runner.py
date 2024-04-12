N, M, K = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]
for _ in range(M):
    i, j = map(lambda x: int(x) - 1, input().split())
    arr[i][j] -= 1

ei, ej = map(lambda x: int(x) - 1, input().split())
arr[ei][ej] = -11

def find_square(arr):
    # [1] 비상구와 모든 참가자 간의 가장 짧은 거리 구하기 -> 변의 길이 (l)
    mini = N
    for i in range(N):
        for j in range(N):
            if -11 < arr[i][j] < 0:
                mini = min(max(abs(ei - i), abs(ej - j)), mini)

    # [2] (0, 0)부터 길이가 l인 정사각형 안에 출구와 참가자가 있는지 체크
    for si in range(N - mini):
        for sj in range(N - mini):
            if si <= ei <= si + mini and sj <= ej <= sj + mini:
                for i in range(si, si + mini + 1):
                    for j in range(sj, sj + mini + 1):
                        if -11 < arr[i][j] < 0:
                            return si, sj, mini + 1

def find_exit(arr):
    for i in range(N):
        for j in range(N):
            if arr[i][j] == -11:
                return i, j

result = 0
count = M
for _ in range(K):
    # [1] 모든 참가자가 출구와의 최단거리의 방향으로 한 칸 이동
    copy = [x[:] for x in arr]
    for i in range(N):
        for j in range(N):
            if -11 < arr[i][j] < 0:
                d = abs(ei - i) + abs(ej - j)
                # 상하좌우 방향으로 확인
                for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    ni, nj = i + di, j + dj
                    if 0 <= ni < N and 0 <= nj < N and arr[ni][nj] <= 0 and d > (abs(ei - ni) + abs(ej - nj)):
                        result += arr[i][j]
                        copy[i][j] -= arr[i][j]
                        if arr[ni][nj] == -11:
                            count += arr[i][j]
                        else:
                            copy[ni][nj] += arr[i][j]
                        break
    arr = copy
    if count == 0:
        break

    # [2] 미로 회전
    # [2-1] 출구와 참가자를 한 명 이상 포함하는 가장 작은 정사각형 탐색
    si, sj, l = find_square(arr)

    copy = [x[:] for x in arr]
    for i in range(l):
        for j in range(l):
            copy[si + i][sj + j] = arr[si + l - 1 - j][sj + i]
            if copy[si + i][sj + j] > 0:
                copy[si + i][sj + j] -= 1
    arr = copy
    ei, ej = find_exit(arr)

print(-result)
print(ei + 1, ej + 1)