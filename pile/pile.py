import random
def pile(n):
    if n == 1:
        return 0
    j = random.randint(1,n-1)
    k = n - j
    prod = j * k
    return prod + pile(j) + pile(k)