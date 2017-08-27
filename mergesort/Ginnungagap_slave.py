from multiprocessing.connection import Client
import sys
import time
from mergesort import mergesort as main
print("Ginnungagap client version 1.0.0 for UCA Cluster, based in Heimdall")
host = input("Type the master's ip: ")
toprint = not input("Should print? (y or n)> ") == "n"
porta = 666
ok = True #the ok is again, for avoid excessive printing
while True:
    time.sleep(0.1) #basic time waiting so it wont flood the connection
    while True:
        resultado = 0 #reset data
        final = 0
        resposta = 0
        inputs = []
        try:
            mysock = Client((host,porta))  # connects to the host
            ok = True
        except:
            if ok is True:
                print ("Error in connecting with the master")
            ok = False
            break
        try:
            mysock.send(bytes("ready","utf-8"))  # sends the ready status to the server
            resposta = mysock.recv().decode("utf-8") #receives the task or the waiting command
            mysock.close()
            if resposta == "wait": #if it must wait, the slave will break the loop  and get inside it again
                break
            if toprint:
                print ("Got a task!") #if it received a task, it will print it
            ok = True
        except:
            e = sys.exc_info()[0]
            if ok is True:
                print ("Error in communicating with master")
                print ("Error %s" % e)
            ok = False
            break
        try:
            inputs = [int(i) for i in resposta.split(",")] #converts the data to input
            resultado = main(inputs) #inputs the data into the ploxys function
            ok = True
        except:
            e = sys.exc_info()[0]
            if ok is True:
                print ("Error %s" % e)
                print("Error in calculating result, maybe data could not been found")
            ok = False
            break
        try:
            final = "done|" + ",".join([str(i) for i in resultado]) #formats the resulting data as the protocol demands
            mysock = Client((host,porta))
            mysock.send(final.encode("utf-8"))
            ok = True
        except:
            if ok is True:
                print ("Error in answering the master")
            ok = False
            break
        mysock.close() #closes the connections
saida = input("Type enter to exit")