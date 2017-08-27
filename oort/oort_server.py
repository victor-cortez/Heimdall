from decimal import *
import random
import time
import socket
from oortlibrary import *
import pickle
import sys
s = socket.socket()         # Create a socket object and sets up the ports and population size (play with it if you want)
#host = input("Enter the hostname> ")
host = "192.168.25.14"
port = 667
#nblocks = int(input("Enter the quantity of blocks> "))
nblocks = 10
s = socket.socket()
s.bind((host, port))        # Bind to the port
s.listen(20)
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
framerate = 1
universe = []
u = Decimal(1)
xcm,ycm,vxcm,vycm,vcm = 0,0,0,0,0
framestaken = 0
limite = 600
now = time.time()
print("Initial Setup is finished, starting the creation of the universe.")
for i in range(size):
    r = Decimal(random.randint(1,10)) / Decimal(7)
    m = u * (r **3)
    obj = (m,Decimal(random.randint(-10,10)),Decimal(random.randint(-10,10)),r,Decimal(random.randint(0,initx-1)),Decimal(random.randint(0,inity-1)))
    universe.append(obj)
while not done:
    multiverse = cutter(len(universe),nblocks)
    responses = 0
    limit = len(multiverse)
    tupleuniverse = tuple(universe)
    given = 0
    newu = []
    while responses < limit:
        #print ("Waiting connections")
        c, addr = s.accept()     # Establish connection with slave.
        status = c.recv(1024).decode('utf-8') #gets the status message and then decode
        if status == "ready" and given < limit:
            c.send(bytes("start","utf-8"))
            c.recv(1024)
            pack = [multiverse[given],universe,cloc,G,u]
            data1 = pickle.dumps(pack)
            c.send(data1)
            given += 1
        elif status == "done":
            c.send(bytes("ready","utf-8"))
            received = c.recv(1048576)
            confirm = c.send(bytes("ok","utf-8"))
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
            print("1 done")
        else:
            c.send(bytes("wait","utf-8"))
        c.close()
    dt = 1/cloc
    universe = list(set(newu))
    oxcm = float(xcm)
    oycm = float(ycm)
    xcm = sum([n[4] * n[0] for n in newu]) / sum([m[0] for m in newu])
    ycm = sum([n[5] * n[0] for n in newu]) / sum([m[0] for m in newu])
    ovxcm = Decimal(vxcm)
    ovycm = Decimal(vycm)
    ovcm = Decimal(vcm)
    vxcm = (Decimal(xcm) - Decimal(oxcm)) / dt
    vycm = (Decimal(ycm) - Decimal(oycm)) / dt
    vcm = Decimal(vxcm ** 2 + vycm ** 2).sqrt()
    acm = (Decimal(vcm) - Decimal(ovcm)) / dt
    if count % framerate == 0:
        xcm = sum([n[4] * n[0] for n in newu]) / sum([m[0] for m in newu])
        ycm = sum([n[5] * n[0] for n in newu]) / sum([m[0] for m in newu])
        deltatime = float(time.time() - now)
        print(deltatime)
        print(len(universe))
        now = time.time()
        cps = 1/deltatime
        framestaken += 1
        if framestaken >= limite:
            done = True
        #pygame.display.flip()
        print(framestaken)
    count += 1
totaltime = time.time() - start
print("Total time elapsed: " + str(totaltime) + " seconds")
