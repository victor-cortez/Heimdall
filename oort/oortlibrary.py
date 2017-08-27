from decimal import *
getcontext().prec = 30
def zeroer(x):
    n = str(x)
    if len(n) < 9:
        n = ("0"*(9-len(n)))+n
    return n
def join(lis):
    n = []
    for item in lis:
        if type(item) != Decimal:
            n.append(convert(item))
        else:
            n.append(str(item))
    return ">".join(n)
def convert(lis):
    n = []
    for item in lis:
        if type(item) == tuple:
            k = tostr(item)
        else:
            k = str(item)
        n.append(k)
    return "|".join(n)
def cutter(size,n):
    a,b = divmod(size,n)
    p = [[i*a,(i+1)*a] for i in range(n)]
    p[-1][1] = p[-1][1] + b - 1
    return p
def tostr(lis):
    n = []
    for i in lis:
        n.append(str(i))
    return ",".join(n)
def rejoin(lis):
    res = []
    packs = lis.split(">")
    for item in packs:
        if "|" in item:
            res.append(invert(item))
        else:
            res.append(Decimal(item))
    return res
def invert(s):
    new = s.split("|")
    k = []
    for i in new:
        if "," in i:
            k.append(fromstr(i))
        else:
            k.append(Decimal(i))
    return tuple(k)
def fromstr(st):
    j = []
    for item in st.split(","):
        j.append(Decimal(item))
    return tuple(j)
def divider(a, l):
    pointer = 0
    k = []
    n = divmod(len(a),l)[0]
    lim = len(a)
    while pointer < lim:
        if lim - pointer >= n:
            k.append(tuple(a[pointer:pointer+n]))
        elif lim-pointer < n:
            k.append(tuple(a[pointer::]))
        pointer += n
    return tuple(k)
def calc(lis):
    universe0,universe2,cloc,G,u = lis
    print(G)
    ini,fini = universe0[0],universe0[1]
    universe1 = universe2[ini:fini+1]
    dt = Decimal(1/cloc)
    newu = []
    print(len(universe1))
    for a in range(len(universe1)):
        asx,asy = [],[]
        fused = False
        for b in range(len(universe2)):
            if universe1[a] != universe2[b]:
                ob1 = universe1[a]
                ob2 = universe2[b]
                x1,y1 = ob1[4],ob1[5]
                x2,y2 = ob2[4],ob2[5]
                r1,r2 = ob1[3],ob2[3]
                m1,m2 = ob1[0],ob2[0]
                if m1 > 10000000 or m2 > 10000000:
                    print(universe1)
                    #raise Exception("FUCK!")
                vx1,vx2 = ob1[1],ob2[1]
                vy1,vy2 = ob1[2],ob2[2]
                d = Decimal(((x1-x2)** 2) + ((y1-y2) ** 2)).sqrt()
                if d > r1 + r2:
                    ac = (G * m2) / (d**2)
                    cos = (x2-x1) / d
                    sen = (y2-y1) / d
                    acx = ac*cos
                    acy = ac*sen
                    asx.append(acx)
                    asy.append(acy)
                else:
                    print("collide")
                    print(d,r1+r2)
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
        mo = universe1[a]
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
    initiallen = len(newu)
    newu = list(set(newu))
    finallen = len(newu)
    print("xxxxx")
    print(initiallen - finallen)
    print("xxxxxx")
    if newu == universe1: raise Exception("eeeequal")
    return newu
if False:
    x = (Decimal(2),Decimal(3))
    y = (x,x)
    n = [y,y,Decimal(1)]
    print(n)
    f = join(n)
    print(f)
    print(type(f))
    k = rejoin(f)
    print(k)
    print(type(k))
    print(k == n)
    print(convert(y))
    print(invert(convert(x)) == x)
