import pygame
from decimal import *
from math import sqrt
import random
import cv2
import time
getcontext().prec = 30
pygame.init()
initx = 1280
inity = 720
start = time.time()
done = False
fourcc = cv2.VideoWriter_fourcc("M","J","P","G")
out = cv2.VideoWriter('output.avi',fourcc, 30.0, (initx,inity),True)
size = 500
G = Decimal(100)
cloc = Decimal(300)
screen = pygame.display.set_mode((initx, inity))
clock = pygame.time.Clock()
pressionou = False
count = 0
framerate = 1
universe = []
u = Decimal(1)
xcm,ycm,vxcm,vycm,vcm = 0,0,0,0,0
myfont = pygame.font.SysFont("monospace", int(initx / 70))
framestaken = 0
limit = 32
now = time.time()
#cria os corpos aleatorios que possuem massa aleatoria, velocidade x aleatoria, velocidade y aleatoria,raio aleatorio e posição aleatoria
for i in range(size):
    r = Decimal(random.randint(1,10)) / Decimal(0.7)
    m = u * (r **3)
    obj = (m,Decimal(random.randint(-10,10)),Decimal(random.randint(-10,10)),r,Decimal(random.randint(0,initx-1)),Decimal(random.randint(0,inity-1)))
    universe.append(obj)
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                done = True
    dt = Decimal(1/cloc)
    newu = []
    for a in range(len(universe)):
        asx,asy = [],[]
        fused = False
        for b in range(len(universe)):
            if a != b:
                ob1 = universe[a]
                ob2 = universe[b]
                x1,y1 = ob1[4],ob1[5]
                x2,y2 = ob2[4],ob2[5]
                r1,r2 = ob1[3],ob2[3]
                m1,m2 = ob1[0],ob2[0]
                vx1,vx2 = ob1[1],ob2[1]
                vy1,vy2 = ob1[2],ob2[2]
                d = Decimal((x1-x2)** 2 + (y1-y2) ** 2).sqrt()
                if d > r1 + r2:
                    ac = (G * m2) / (d**2)
                    cos = (x2-x1) / d
                    sen = (y2-y1) / d
                    acx = ac*cos
                    acy = ac*sen
                    asx.append(acx)
                    asy.append(acy)
                else:
                    vxf = (m1*vx1 + m2*vx2)/ (m1 + m2)
                    vyf = (m1*vy1 + m2 * vy2) / (m1 + m2)
                    acx = vxf/dt
                    acy = vyf/dt
                    xcmf = ((x1 * m1) + (x2 * m2))/(m1 + m2)
                    ycmf = ((y1 * m1) + (y2 * m2))/(m1 + m2)
                    fus = (m1 + m2,vxf,vyf,((m1+m2)/u)** Decimal(1/3),xcmf,ycmf)
                    fused = True
                    #asx.append(acx)
                    #asy.append(acy)
        axr = sum(asx)
        ayr = sum(asy)
        mo = universe[a]
        m,vx,vy,r,x,y = mo
        vxf = vx + axr * dt
        vyf = vy + ayr * dt
        xf = x + vx * dt + ((axr * (dt**2)) / 2)
        yf = y + vy * dt + ((ayr * (dt**2)) / 2)
        fo = (m,vxf,vyf,r,xf,yf)
        if fused:
            newu.append(fus)
        else:
            newu.append(fo)
    universe = list(set(newu))
    newu = list(universe)
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
        screen.fill((0, 0, 0))
        [pygame.draw.circle(screen,(255,0,0),(int(ab[4]),int(ab[5])),ab[3]) for ab in newu]
        xcm = sum([n[4] * n[0] for n in newu]) / sum([m[0] for m in newu])
        ycm = sum([n[5] * n[0] for n in newu]) / sum([m[0] for m in newu])
        deltatime = time.time() - now
        now = time.time()
        cps = 1/deltatime
        pygame.draw.circle(screen,(0,255,0),(int(xcm),int(ycm)),10)
        label = myfont.render("Precision: " + str(round(cloc,5)) + "| Calculations per second: " + str(round(cps,5)) + " | Speed: " + str(round(vcm,5)) + " | Aceleration: " + str(round(acm,5)),1,(0,0,255))
        screen.blit(label,(100,100))
        #save the frame to harddisk
        pygame.image.save(screen,"frame.png")
        img = cv2.imread("frame.png",1)
        out.write(img)
        framestaken += 1
        if framestaken >= limit:
            done = True
        #pygame.display.flip()
        print(framestaken)
    count += 1
totaltime = time.time() - start
print("Total time elapsed: " + str(totaltime) + " seconds")
cv2.destroyAllWindows()
out.release()
