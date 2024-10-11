R, C, K = map(int, input().split())
unit = [list(map(int, input().split())) for _ in range(K)]  # si, sj, d
map = [[1] + [0] * C + [1] for _ in range(R + 3)] + [[1] * (C + 2)]
exit_set = set()

# 상 우 하 좌
di = [-1, 0, 1, 0]
dj = [0, 1, 0, -1]

def bfs(si, sj):
    q = []
    visited = [[0] * (C + 2) for _ in range(R + 4)]
    max_i = 0

    q.append((si, sj))
    visited[si][sj] = 1

    while q:
        ci, cj = q.pop(0)
        max_i = max(ci, max_i)

        # 조건: 같은 값 또는 자신이 출구
        for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            ni, nj = ci + di, cj + dj
            if visited[ni][nj] == 0 and (map[ci][cj] == map[ni][nj] or ((ci, cj) in exit_set and map[ni][nj] > 1)):
                q.append((ni, nj))
                visited[ni][nj] = 1

    return max_i - 2

answer = 0
num = 2
for cj, d in unit:
    ci = 1
    while True:
        # 남쪽으로 이동
        if (map[ci + 1][cj - 1] + map[ci + 2][cj] + map[ci + 1][cj + 1]) == 0:
            ci += 1
        # 서쪽으로 회전하면서 남쪽으로 이동
        elif (map[ci - 1][cj - 1] + map[ci][cj - 2] + map[ci + 1][cj - 1] + map[ci + 2][cj - 1] + map[ci + 1][cj - 2]) == 0:
            ci += 1
            cj -= 1
            d = (d - 1) % 4
        # 동쪽으로 회전하면서 남쪽으로 이동
        elif (map[ci - 1][cj + 1] + map[ci][cj + 2] + map[ci + 1][cj + 1] + map[ci + 2][cj + 1] + map[ci + 1][cj + 2]) == 0:
            ci += 1
            cj += 1
            d = (d + 1) % 4
        else:
            break

    # 위치가 범위 밖인 경우 초기화
    if ci < 4:
        map = [[1] + [0] * C + [1] for _ in range(R + 3)] + [[1] * (C + 2)]
        exit_set = set()
        num = 2
    else:
        # 위치 표시, 비상구 위치 추가
        map[ci + 1][cj] = map[ci - 1][cj] = num
        map[ci][cj - 1: cj + 2] = [num] * 3
        num += 1

        exit_set.add((ci + di[d], cj + dj[d]))
        answer += bfs(ci, cj)

print(answer)