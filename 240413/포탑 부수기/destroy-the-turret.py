from collections import deque

N, M, K = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]

turn = [[0] * M for _ in range(N)]

def laser(si, sj, ei, ej):
    q = deque()
    # 경로 표시하기
    v = [[[] for _ in range(M)] for _ in range(N)]

    q.append((si, sj))
    v[si][sj] = (si, sj)
    damage = arr[si][sj]

    while q:
        ci, cj = q.popleft()
        # 타겟까지 도달함 !
        if (ci, cj) == (ei, ej):
            arr[ei][ej] = max(0, arr[ei][ej] - damage)
            while True:
                ci, cj = v[ci][cj]          # 돌아가면서 확인
                if (ci, cj) == (si, sj):    # 공격자 위치까지 확인 완료
                    return True
                arr[ci][cj] = max(0, arr[ci][cj] - damage//2)
                record.add((ci, cj))

        for di, dj in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            ni, nj = (ci + di) % N, (cj + dj) % M
            if len(v[ni][nj]) == 0 and arr[ni][nj] > 0:
                q.append((ni, nj))
                v[ni][nj] = (ci, cj)

    # 타겟을 찾지 못함
    return False

def bomb(si, sj, ei, ej):
    damage = arr[si][sj]
    arr[ei][ej] = max(0, arr[ei][ej] - damage)

    # 주변 8개 포탑에게 피해
    for di, dj in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
        ni, nj = (ei + di) % N, (ej + dj) % M
        if (ni, nj) != (si, sj):
            arr[ni][nj] = max(0, arr[ni][nj] - damage//2)
            record.add((ni, nj))

for T in range(1, K + 1):
    # [1] 공격자 찾기
    mini, max_turn, si, sj = 5001, 0, -1, -1
    for i in range(N):
        for j in range(M):
            # 포탑이 아닌 경우 스킵
            if arr[i][j] <= 0:
                continue
            if mini > arr[i][j] or (mini == arr[i][j] and max_turn < turn[i][j]) \
                or (mini == arr[i][j] and max_turn == turn[i][j] and si + sj < i + j) \
                or (mini == arr[i][j] and max_turn == turn[i][j] and si + sj == i + j and sj < j):
                mini, max_turn, si, sj = arr[i][j], turn[i][j], i, j    # 공격자 선택!

    # [2] 타겟 찾기
    maxi, min_turn, ei, j = 0, T, N, M
    for i in range(N):
        for j in range(M):
            # 포탑이 아닌 경우 스킵
            if arr[i][j] <= 0:
                continue
            if maxi < arr[i][j] or (maxi == arr[i][j] and min_turn > turn[i][j]) \
                    or (maxi == arr[i][j] and min_turn == turn[i][j] and ei + ej > i + j) \
                    or (maxi == arr[i][j] and min_turn == turn[i][j] and ei + ej == i + j and sj < j):
                maxi, min_turn, ei, ej = arr[i][j], turn[i][j], i, j  # 타겟 선택!

    # [3] 레이저 공격 (우하상좌 순서로 최단거리 이동)
    arr[si][sj] += (N + M)
    turn[si][sj] = T
    record = set()
    record.add((si, sj))
    record.add((ei, ej))
    if laser(si, sj, ei, ej) == False:

        # 레이저 공격 실패하는 경우
        # [4] 포탄 공격
        bomb(si, sj, ei, ej)

    # [5] 포탑 정비
    for i in range(N):
        for j in range(M):
            if arr[i][j] > 0 and (i, j) not in record:
                arr[i][j] += 1

    potap = N *M
    for p in arr:
        potap -= p.count(0)
    if potap <= 1:
        break

print(max(map(max, arr)))