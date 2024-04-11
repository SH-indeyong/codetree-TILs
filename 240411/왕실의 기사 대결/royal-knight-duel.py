L, N, Q = map(int, input().split())
arr = [[2] * (L + 2)] + [[2] + list(map(int, input().split())) + [2] for _ in range(L)] + [[2] * (L + 2)]

health = [0] * (N + 1)
knight = {}
for n in range(1, N + 1):
    r, c, h, w, k = map(int, input().split())
    knight[n] = [r, c, h, w, k]
    health[n] = k

di = [-1, 0, 1, 0]
dj = [0, 1, 0, -1]

def move(start, dr):
    global result
    q = []
    move_knight = set()
    damage = [0] * (N + 1)

    q.append(start)
    move_knight.add(start)

    while q:
        cur = q.pop(0)
        ci, cj, h, w, k = knight[cur]
        ni, nj = ci + di[dr], cj + dj[dr]

        # 자신의 세력 모두 탐색
        for i in range(ni, ni + h):
            for j in range(nj, nj + w):
                if arr[i][j] == 2:
                    return
                if arr[i][j] == 1:
                    damage[cur] += 1

        # 충돌하는 기사가 있는 경우 큐에 추가
        for you in knight:
            if you in move_knight:
                continue            # 이미 이동할 예정인 기사는 스킵

            yi, yj, yh, yw, yk = knight[you]
            # 충돌할 수 있는 조건
            if ni <= yi + yh - 1 and ni + h - 1 >= yi and nj <= yj + yw - 1 and nj + w - 1 >= yj:
                q.append(you)
                move_knight.add(you)

    # 움직임을 시작한 기사는 피해 초기화
    damage[start] = 0

    # 이동 / 피해 적용
    for idx in move_knight:
        si, sj, h, w, k = knight[idx]

        if k <= damage[idx]:
            knight.pop(idx)
        else:
            ni, nj = si + di[dr], sj + dj[dr]
            knight[idx] = [ni, nj, h, w, k - damage[idx]]

for _ in range(1, Q + 1):
    idx, dr = map(int, input().split())
    if idx in knight:
        move(idx, dr)

result = 0
for idx in knight:
    result += health[idx] - knight[idx][4]
print(result)