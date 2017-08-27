import pile
import matplotlib.pyplot as plt
import time
import random
x,y = [],[]
for i in range(0,10):
    p = 10 ** i
    print(i)
    start = time.time()
    pile.pile(p)
    final = time.time()
    delta = final - start
    x.append(p)
    y.append(delta)
plt.plot(x,y)
plt.ylabel("The time taken to compute the pile splitting of a pile os size n")
print(y)
plt.show()
plt.savefig("data.jpg")
def cutter(tsize,dsize):
    p = [tsize]
    soma = 0
    size = 1
    for i in range(dsize):
        if size == 0:
            break
        update = []
        for n in p:
            if n == 1:
                soma += 0
            else:
                a = random.randint(1,n-1)
                b = n - a
                soma += a*b
                update.append(a)
                update.append(b)
        p = list(update)
        size = len(p)
        print(update,soma)
    return(p,soma)
print(cutter(30,99))
