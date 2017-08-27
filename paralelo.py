import multiprocessing
from random import randint
from ploxys import main,populacao
from collections import OrderedDict
initial_ploxys = []
num_rounds = 1

#prototype, ignore it

if __name__ == '__main__':
    #main loop
    for i in range(0,num_rounds):
        saida = multiprocessing.Queue()
        procs = []
        #gives every setup , its fitness pontuation
        for lista in populacao:
            print (lista)
            argumentos = [int (i) for i in lista.split(",")]
            p = multiprocessing.Process(target=main, args=(argumentos[0],argumentos[1],argumentos[2],argumentos[3],saida))
            p.start()
            print (saida)
        for p in procs:
            p.join()
        print (populacao)