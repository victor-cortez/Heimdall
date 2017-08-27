def merge(a,b):
    pa,pb = 0,0
    lis = []
    pa,pb = [0,len(a) > 0],[0,len(b) > 0]
    la,lb = len(a),len(b)
    for i in range(la + lb):
        if pa[1] is True:
            ta = a[pa[0]]
        else:
            ta = float("inf")
        if pb[1] is True:
            tb = b[pb[0]]
        else:
            tb = float("inf")
        if tb < ta:
            lis.append(tb)
            pb[0] = pb[0] + 1
            if pb[0] >= lb:
                pb[1] = False
        else:
            lis.append(ta)
            pa[0] = pa[0] + 1
            if pa[0] >= la:
                pa[1] = False
    return lis
def mergesort(lista):
    if len(lista) <= 1:
        return lista
    a,b = [],[]
    for i in range(len(lista)):
        [a,b][i%2].append(lista[i])
    return merge(mergesort(a),mergesort(b))