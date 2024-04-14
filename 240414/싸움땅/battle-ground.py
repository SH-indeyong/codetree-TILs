N, M, K = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]
gun = [[[] for _ in range(N)] for _ in range(N)]
for i in range(N):
    for j in range(N):
        if arr[i][j] > 0:
            gun[i][j].append(arr[i][j])

arr = [[0] * N for _ in range(N)]

players = {}
for m in range(1, M + 1):
    x, y, d, p = map(int, input().split())
    # m번째 플레이어 (i, j, d, p, gun, score)
    players[m] = [x - 1, y - 1, d, p, 0, 0]
    arr[x - 1][y - 1] = m

opp = {0: 2, 1: 3, 2: 0, 3: 1}
di = [-1, 0, 1, 0]
dj = [0, 1, 0, -1]

def leave(idx, ci, cj, cd, cp, cg, cs):
    # 현재방향에서부터 시계방향 90도씬 빈 칸 찾기
    for r in range(4):
        ni, nj = ci + di[(ci + r) % 4], cj + dj[(cj + r) % 4]
        if 0 <= ni < N and 0 <= nj < N and arr[ni][nj] == 0:
            if len(gun[ni][nj]) > 0:
                cg = max(gun[ni][nj])
                gun[ni][nj].remove(cg)
            arr[ni][nj] = idx
            players[idx] = [ni, nj, (cd + r) % 4, cp, cg, cs]
            return

for _ in range(K):
    # 1 ~ m 플레이어 순차적으로 진행
    for i in players:
        # [1] 방향대로 한 칸 이동
        ci, cj, cd, cp, cg, cs = players[i]
        ni, nj = ci + di[cd], cj + dj[cd]
        # 범위를 벗어나면
        if ni < 0 or N <= ni or nj < 0 or N <= nj:
            cd = opp[cd]
            ni, nj = ci + di[cd], cj + dj[cd]
        arr[ci][cj] = 0

        # [2-1] 이동한 칸이 빈칸인 경우 -> 총이 더 강하다면 교체
        if arr[ni][nj] == 0:
            if len(gun[ni][nj]) > 0:
                maxi = max(gun[ni][nj])
                if cg < maxi:
                    if cg > 0:
                        gun[ni][nj].append(cg)      # 플레이어가 총을 가지고 있었다면 자리에 내려놓기
                    gun[ni][nj].remove(maxi)
                    cg = maxi
                arr[ni][nj] = i
                players[i] = (ni, nj, cd, cp, cg, cs)
        # [2-2] 이동한 칸에 다른 사람이 있는 경우
        else:
            # 상대방 정보
            enemy = arr[ni][nj]
            ei, ej, ed, ep, eg, es = players[enemy]
            # 자신이 이기는 경우
            if (cp + cg) > (ep + eg) or ((cp + cg) == (ep + eg) and cp > ep):
                # 파워의 차이만큼 점수 획득
                cs += (cp + cg) - (ep + eg)
                leave(enemy, ni, nj, ed, ep, 0, es) # 상대방은 총을 놓고 떠남

                # 자신은 더 강한 총으로 교체
                if cg < eg:
                    if cg > 0:
                        gun[ni][nj].append(cg)
                    cg = eg
                else:
                    if eg > 0:
                        gun[ni][nj].append(eg)
                arr[ni][nj] = i
                players[i] = [ni, nj, cd, cp, cg, cs]

            # 자신이 지는 경우
            else:
                es += (ep + eg) - (cp + cg)
                leave(i, ni, nj, cd, cp, 0, cs)     # 자신이 총을 놓고 떠남

                # 상대방을 더 강한 총으로 교체
                if eg < cg:
                    if eg > 0:
                        gun[ni][nj].append(eg)
                    eg = cg
                else:
                    if cg > 0:
                        gun[ni][nj].append(cg)
                arr[ni][nj] = enemy
                players[enemy] = [ni, nj, ed, ep, eg, es]

for i in players:
    print(players[i][5], end=' ')