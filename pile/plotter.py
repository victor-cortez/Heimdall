import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
name = "outfile5-6.txt"
name2 = "outfile.txt"
arquivo = open(name,"r")
arquivo2= open(name2,"r")
data = [[float(n) for n in i.replace("/n","").split()] for i in arquivo.readlines()]
data2 = [[float(n) for n in i.replace("/n","").split()] for i in arquivo2.readlines()]
x = [i[0] for i in data2]
y2 = [i[1] for i in data2]
y1 = [i[1] for i in data]
y = []
for i in range(len(y2)):
    if i < len(y1):
        y.append((y2[i] + y1[i])/2)
    else:
        y.append(y2[i])
#print(data)
thefit = np.polyfit(x,y,2)
#print(thefit)
def exponenial_func(x, a, b, c):
    return a*np.exp(-b*x)+c
#print(len(x),len(y))
popt, pcov = curve_fit(exponenial_func, x[:9], y[:9], p0=(1, 1e-6, 1))
xx = np.linspace(0,100000,1000)
yy2 = exponenial_func(xx, *popt)
def thevalues(xval,fitdata):
    components = []
    fitdata = np.fliplr([fitdata])[0]
    for i in range(len(fitdata)):
        value = (xval**i)*fitdata[i]
        components.append(value)
    return sum(components)
yy = [thevalues(k,thefit) for k in x]
#print(yy)
#plt.plot(x[:10],yy[:10])
plt.plot(x[:9],y[:9])
#print(yy2)
plt.plot(xx,yy2)
plt.savefig("5ucasatpile.jpg",dpi=100)
plt.show()
print(y[9])
