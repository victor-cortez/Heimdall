import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
namei5i5 = "timesi5-35704nucleos10^5.txt"
namei5i6 = "timesi5-35704nucleos10^6.txt"
nameuca = "mergesortclean.txt"
datanamei5i6 = sorted([float(i.replace("/n","")) for i in open(namei5i6,"r").readlines()])
datanamei5i5 =sorted([float(i.replace("/n","")) for i in open(namei5i5,"r").readlines()])
datauca = [[float(n) for n in i.replace("\n","").split()] for i in open(nameuca,"r").readlines()]
datauca5 = sorted([i[3] for i in datauca if i[1] == 100000 and i[2] == 10000])
datauca6 = sorted([i[3] for i in datauca if i[1] == 1000000 and i[2] == 100000])
dxwith5i5 = 0.08
dxwith5uca = 4.0
dxwith6i5 = 0.3
dxwith6uca = 7.0
fig, ax = plt.subplots()
def histo(lis,dx):
    init = lis[0]
    final = lis[-1]
    bot = init
    top = bot + dx
    x = []
    y = []
    while bot <= final:
        x.append(bot)
        y.append(len([i for i in lis if i>= bot and i < top]))
        bot = bot + dx
        top = bot + dx
    return (x,y)
histoi5i5 = histo(datanamei5i5,dxwith5i5)
histoi5i6 = histo(datanamei5i6,dxwith6i5)
histo5uca = histo(datauca5,dxwith5uca)
histo6uca = histo(datauca6,dxwith6uca)
print(histoi5i5)
print(histoi5i6)
print(histo5uca)
print(histo6uca)
#ax.bar(histoi5i6[0],histoi5i6[1],dxwith6i5,color="r")
#ax.bar(histoi5i5[0],histoi5i5[1],dxwith5i5,color="b")
#ax.bar(histo5uca[0],histo5uca[1],dxwith5uca,color="g")
ax.bar(histo6uca[0],histo6uca[1],dxwith6uca,color="r")
plt.show()
