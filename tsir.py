r = []
for _ in range(5):
    r.append([0] * 5)

def rate(i,j):
    if i == 0 and j == 0:
        r[0][0] = 6
        return r[i][j]    
    for j_ in range(0,i+1):
        if i == j_:
            print(i, j_)
            r[i][j_] = rate(i-1, j_-1) * 1.25
        else:
            print(i, j_)
            r[i][j_] = rate(i-1, j_) * 0.9
    return r[i][j]
def Z(i,j, n):
    if i == n:
        return 100
    qu, qd = 0.5, 0.5
    t = (1 / (1 + (r[i][j]/100))) * (qu * Z(i + 1, j+ 1,n) + (qd * Z(i+1,j,n)))
    print(i,j,t)
    return t

rate(4, 4)
print(Z(0,0,4))


