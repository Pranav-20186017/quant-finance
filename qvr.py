import matplotlib.pyplot as plt
import random
X = [-1] * 56 + [1] * 44
random.shuffle(X)
M = []
s = 0
for i in X:
    s += i
    M.append(s)
dif = 0
for i in range(1, 5):
    td = (M[i] - M[i - 1]) ** 2
    dif += td
print(i)
print(dif)
plt.plot(range(0,100),M)
plt.show()