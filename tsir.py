# r = [[6],[5.4,7.5],[4.86,6.75,9.38],[4.37,6.08,8.44,11.72],[3.94,5.47,7.59,10.55,14.65]]
r = []
for _ in range(5):
    r.append([0] * 5)


def rate(i,j):
    # print(r)
    # print("*" * 7)

    if i == 0 and j == 0:
        # print("HERE")
        r[0][0] = 6
        return r[i][j]
    
    for j_ in range(0,i+1):
        # print(i,j)
        if i == j_:
            print(i, j_)
            r[i][j_] = rate(i-1, j_-1) * 1.25
        # elif j_ == 0:
        #     r[i][j_]  = r[i-1][j_] * 0.9
        else:
            print(i, j_)
            r[i][j_] = rate(i-1, j_) * 0.9
    
    # exit()
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


