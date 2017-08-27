import timeit
import matplotlib.pyplot as plt
times = []
for i in range(0,6):
    t = timeit.Timer("pickle.dumps(list(range(" + str(10**i) + ")))","import pickle")
    times.append(t.timeit())
    print("done " + str(i))
print(times)
c = open("pickletimes.txt","w")
c.write(str(times))
c.close()

