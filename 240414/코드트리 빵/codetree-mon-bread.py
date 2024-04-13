from collections import deque

N, M = map(int, input().split())
arr = [[1] * (N + 2)] + [[1] + list(map(int, input().split())) + [1] for _ in range(N)] + [[1] * (N + 2)]

basecamp = set()
for i in range(1, N + 1):
    for j in range(1, N + 1):
        if arr[i][j] == 1:
            basecamp.add((i, j))
            arr[i][j] = 0

store = {}
for m in range(1, M + 1):
    i, j = map(int, input().split())
    store[m] = (i, j)

def find(ei, ej, dirs):
    q = deque()
    v = [[0] * (N + 2) for _ in range(N + 2)]
    next = []

    q.append((ei, ej))
    v[ei][ej] = 1

    while q:
        qq = deque()
        for ci, cj in q:
            if (ci, cj) in dirs:
                next.append((ci, cj))
            else:
                for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    ni, nj = ci + di, cj + dj
                    if v[ni][nj] == 0 and arr[ni][nj] == 0:
                        qq.append((ni, nj))
                        v[ni][nj] = v[ci][cj] + 1

        # 이동할 칸이 결정된 경우 (하나 이상)
        if len(next) > 0:
            next.sort()
            return next[0]
        q = qq
    return -1

def solve():
    q = deque()
    time = 1
    arrived = [0] * (M + 1)

    while q or time == 1:
        qq = deque()
        lst = []

        # [1] 이동 가능한 모든 사람 편의점까지의 최단거리 방향으로 한 칸 이동
        for ci, cj, idx in q:
            if arrived[idx] == 0:
                # 다음 이동할 칸 찾기
                ni, nj = find(store[idx][0], store[idx][1], set(((ci - 1, cj), (ci + 1, cj), (ci, cj - 1), (ci, cj + 1))))
                if (ni, nj) == store[idx]:
                    arrived[idx] = time
                    lst.append((ni, nj))        # 통행 금지
                else:
                    qq.append((ni, nj, idx))

        q = qq

        # [2] 편의점 도착한 경우
        if len(lst) > 0:
            for ri, rj in lst:
                arr[ri][rj] = 1         # 지나온 칸은 앞으로 이동 불가

        # [3] idx == time 인 사람이 베이스캠프로 순간이동
        if time <= M:
            ei, ej = store[time]
            bi, bj = find(ei, ej, basecamp)
            basecamp.remove((bi, bj))
            arr[bi][bj] = 1
            q.append((bi, bj, time))

        time += 1

    return max(arrived)

result = solve()
print(result)