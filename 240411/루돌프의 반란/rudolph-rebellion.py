N, M, P, C, D = map(int, input().split())
v = [[0] * N for _ in range(N)]

# 루돌프
Ri, Rj = map(lambda x: int(x) - 1, input().split())
v[Ri][Rj] = -1

score = [0] * (P + 1)
status = [1] * (P + 1)
status[0] = 0
santa_turn = [1] * (P + 1)

# 산타
Santa = [[N] * 2 for _ in range(P+1)]
for _ in range(1, P + 1):
    i, Si, Sj = map(int, input().split())
    Santa[i] = [Si - 1, Sj - 1]
    v[Si - 1][Sj - 1] = i

# 거리 구하는 함수
def distance(a, b):
    ai, aj, bi, bj = a[0], a[1], b[0], b[1]
    d = (ai - bi) ** 2 + (aj - bj) ** 2
    return d

# 산타가 밀리는 함수
def flyingSanta(idx, si, sj, di, dj, add):
    q = [(idx, si, sj, add)]

    while q:
        idx, si, sj, add = q.pop(0)
        ni, nj = si + di * add, sj + dj * add
        if 0 <= ni < N and 0 <= nj < N:
            if v[ni][nj] == 0:
                v[ni][nj] = idx
                Santa[idx] = [ni, nj]
                return
            else:
                q.append((v[ni][nj], ni, nj, 1))
                v[ni][nj] = idx
                Santa[idx] = [ni, nj]
        else:
            status[idx] = 0
            return

for turn in range(1, M + 1):
    # [0] 남은 산타가 0명이면 종료
    if status.count(1) == 0:
        continue

    # [1] 루돌프 이동
    # [1-1] 가까운 산타 탐색
    mini = 2 * N ** 2
    for idx in range(1, P + 1):
        if status[idx] == 0:
            continue
        Si, Sj = Santa[idx]
        d = distance((Ri, Rj), (Si, Sj))
        if mini > d:
            mini = d
            shortest = [(Si, Sj, idx)]
        elif mini == d:
            shortest.append((Si, Sj, idx))
        shortest.sort(reverse=True)     # 내림차순으로 하여 행, 열 순서로 비교
        Si, Sj, target = shortest[0]    # 목표 산타

    # [1-2] 산타 방향으로 이동: 루돌프 좌표 변화
    Rdi, Rdj = 0, 0
    if Ri > Si:
        Rdi = -1
    elif Ri < Si:
        Rdi = 1
    if Rj > Sj:
        Rdj = -1
    elif Rj < Sj:
        Rdj = 1
    v[Ri][Rj] = 0
    Ri, Rj = Ri + Rdi, Rj + Rdj
    v[Ri][Rj] = -1

    # [1-3] 충돌하는 경우 산타 밀림
    if (Ri, Rj) == (Si, Sj):
        score[target] += C
        santa_turn[target] = turn + 2
        flyingSanta(target, Si, Sj, Rdi, Rdj, C)

    # [2] 산타 순서대로 이동
    # [2-1] 모든 산타를 순서대로 실행 (기절하지 않은 산타)
    for idx in range(1, P + 1):
        if status[idx] == 0:
            continue
        if santa_turn[idx] > turn:
            continue

        Si, Sj = Santa[idx]
        mini = distance((Ri, Rj), (Si, Sj))
        shortest = []
        for di, dj in ((-1, 0), (0, 1), (1, 0), (0, -1)):
            ni, nj = Si +di, Sj + dj
            d = distance((Ri, Rj), (ni, nj))
            if 0 <= ni < N and 0 <= nj < N and v[ni][nj] <= 0 and d < mini:
                mini = d
                shortest.append((ni, nj, di, dj))
        if len(shortest) == 0:
            continue
        ni, nj, di, dj = shortest[-1]       # 마지막에 추가된(최소거리)

        # [2-2] 충돌하는 경우 산타 밀림
        if (Ri, Rj) == (ni, nj):
            score[idx] += D
            santa_turn[idx] = turn + 2
            v[Si][Sj] = 0
            flyingSanta(idx, ni, nj, -di, -dj, D)
        # [2-3] 빈칸인 경우 산타의 이동 처리만 실행
        else:
            v[Si][Sj] = 0
            v[ni][nj] = idx
            Santa[idx] = [ni, nj]

    # [3] 점수 획득
    for i in range(1, P + 1):
        if status[i] == 1:
            score[i] += 1

print(*score[1:])