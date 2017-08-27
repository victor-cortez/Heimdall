from decimal import *
import random
import time
import os
from multiprocessing.connection import Listener
from oortlibrary import *
import pickle
import sys
import zipfile
toprint = False
#host = input("Enter the hostname> ")
host = "192.168.25.14"
port = 667
#nblocks = int(input("Enter the quantity of blocks> "))
nblocks = 1
s = Listener((host, port))
print("Host stablished")
getcontext().prec = 30
initx = 1280
inity = 720
start = time.time()
done = False
size = 100
G = Decimal(100)
cloc = Decimal(300)
pressionou = False
count = 0
framerate = 30
universe = []
u = Decimal(1)
xcm,ycm,vxcm,vycm,vcm = 0,0,0,0,0
framestaken = 0
limite = 100
now = time.time()
adress = os.getcwd()
nameofmem = "frames.zip"
os.chdir(adress)
print("Initial Setup is finished, starting the creation of the universe.")
for i in range(size):
    r = Decimal(random.randint(1,10)) / Decimal(1)
    m = u * (r **3)
    obj = (m,Decimal(random.randint(-10,10)),Decimal(random.randint(-10,10)),r,Decimal(random.randint(0,initx-1)),Decimal(random.randint(0,inity-1)))
    universe.append(obj)
newu = []
while not done:
    multiverse = cutter(len(universe),nblocks)
    responses = 0
    limit = len(multiverse)
    tupleuniverse = tuple(universe)
    given = 0
    old = list(newu)
    newu = []
    while responses < limit:
        #print ("Waiting connections")
        c = s.accept()     # Establish connection with slave.
        status = c.recv().decode('utf-8') #gets the status message and then decode
        if status == "ready" and given < limit:
            c.send(bytes("start","utf-8"))
            pack = [multiverse[given],universe,cloc,G,u]
            data1 = pickle.dumps(pack)
            c.send(data1)
            given += 1
        elif status == "done":
            received = c.recv()
            try:
                newuniverse = pickle.loads(received)
            except Exception as e:
                print("-----------")
                print(len(received))
                print(sys.getsizeof(received))
                print ("Error %s" % str(e))
                print("-----------")
            newu += newuniverse
            responses += 1
            if toprint:
                print("1 done")
        else:
            c.send(bytes("wait","utf-8"))
        c.close()
    dt = 1/cloc
    initiallen = len(newu)
    newu = list(set(newu))
    finallen = len(newu)
    print("***")
    print(initiallen - finallen)
    print("***")
    universe = list(newu)
#    if newu == old: raise Exception("equality")
    summass = sum([i[0] for i in newu])
    print(summass)
    oxcm = Decimal(xcm)
    oycm = Decimal(ycm)
    xcm = Decimal(sum([n[4] * n[0] for n in newu])) / Decimal(sum([m[0] for m in newu]))
    ycm = Decimal(sum([n[5] * n[0] for n in newu])) / Decimal(sum([m[0] for m in newu]))
    ovxcm = Decimal(vxcm)
    ovycm = Decimal(vycm)
    ovcm = Decimal(vcm)
    vxcm = (Decimal(xcm) - Decimal(oxcm)) / dt
    vycm = (Decimal(ycm) - Decimal(oycm)) / dt
    vcm = Decimal(vxcm ** 2 + vycm ** 2).sqrt()
    acm = (Decimal(vcm) - Decimal(ovcm)) / dt
    print("^^^^")
    print(acm)
    print("vvvvv")
    if count % framerate == 0:
        deltatime = float(time.time() - now)
        if toprint: print(deltatime)
        if toprint: print(len(universe))
        now = time.time()
        cps = 1/deltatime
        framestaken += 1
        if framestaken >= limite:
            done = True
        #pygame.display.flip()
        #Ready to save the frame
        struct = [newu,deltatime,cps,vcm,acm,cloc]
        filename = zeroer(framestaken)+".fra"
        pickle.dump(struct,open(filename,"wb"))
        z = zipfile.ZipFile(nameofmem, "a",zipfile.ZIP_DEFLATED)
        z.write(filename)
        z.close()
        os.remove(filename)
        print(framestaken)
    count += 1
totaltime = time.time() - start
print("Total time elapsed: " + str(totaltime) + " seconds")
