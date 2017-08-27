import pygame
import zipfile
import pickle
import os
from decimal import *
from oortlibrary import *
name = "frames.zip"
arch = zipfile.ZipFile(name)
lista = arch.namelist()
print(lista)
count = 0
outname = "processed.zip"
#pygame stuff
initx = 1280
inity = 720
pygame.init()
screen = pygame.display.set_mode((initx, inity))
myfont = pygame.font.SysFont("monospace", int(initx / 70))
for framearch in lista:
    frame = pickle.load(arch.open(framearch))
    newu,deltatime,cps,vcm,acm,cloc = frame
    screen.fill((0, 0, 0))
    print(newu[0])
    [pygame.draw.circle(screen,(255,0,0),(int(ab[4]),int(ab[5])),ab[3]) for ab in newu]
    xcm = sum([n[4] * n[0] for n in newu]) / sum([m[0] for m in newu])
    ycm = sum([n[5] * n[0] for n in newu]) / sum([m[0] for m in newu])
    pygame.draw.circle(screen,(0,255,0),(int(xcm),int(ycm)),10)
    label = myfont.render("Precision: " + str(round(cloc,5)) + "| Calculations per second: " + str(round(cps,5)) + " | Speed: " + str(round(vcm,5)) + " | Aceleration: " + str(round(acm,5)),1,(0,0,255))
    screen.blit(label,(100,100))
    #save the frame to harddisk
    filename = zeroer(count)+".png"
    pygame.image.save(screen,filename)
    z = zipfile.ZipFile(outname, "a",zipfile.ZIP_DEFLATED)
    z.write(filename)
    z.close()
    os.remove(filename)
    count += 1
