from decimal import *
import time
from multiprocessing.connection import Client
import sys
from oortlibrary import *
import pickle
getcontext().prec = 30
print("Ginnungagap client version 1.0.0 for UCA Cluster, based in Heimdall")
#host = input("Type the master's ip: ")
host = "192.168.25.14"
#toprint = not input("Should print? (y or n)> ") == "n"
toprint = True
porta = 667
count = 0
ok = True #the ok is again, for avoid excessive printing
while True:
    time.sleep(0.1) #basic time waiting so it wont flood the connection
    while True:
        resultado = 0 #reset data
        final = 0
        resposta = 0
        inputs = []
        try: #lots of error handling and error reporting
            pass
        except socket.error:
            if ok is True:
                print ("Error in creating the socket") # Finishes with error report
            ok = False
            break
        try:
            mysock = Client((host, porta))  # connects to the host
            ok = True
        except:
            if ok is True:
                print ("Error in connecting with the master")
            ok = False
            break
        try:
            mysock.send(bytes("ready","utf-8"))  # sends the ready status to the server
            resposta0 = mysock.recv().decode("utf-8") #receives the task or the waiting command
            if resposta0 == "wait": #if it must wait, the slave will break the loop  and get inside it again
                break
            if toprint:
                print ("Got a task!") #if it received a task, it will print it
            ok = True
            resposta1 = mysock.recv()
            mysock.close()
        except:
            e = sys.exc_info()[0]
            if ok is True:
                print ("Error in communicating with master")
                print ("Error %s" % e)
            ok = False
            break
        try:
            dataagain = resposta1
            inputs = pickle.loads(dataagain)
            if toprint:
                print("------")
                print(len(inputs[0]),len(inputs[1]),sys.getsizeof(resposta1))
                print("----------")
            resultado = calc(inputs) #inputs the data into the function
            #print(resultado[0])
            ok = True
        except Exception as e:
            print(len(resposta1))
            print("**********")
            #print(resposta1)
            print("**********")
            if ok is True:
                print ("Error %s" % str(e))
                print("Error in calculating result, maybe data could not been found")
            ok = False
            break
        try:
            if toprint:
                print("Sending final")
            final = pickle.dumps(resultado) #formats the resulting data as the protocol demands
            mysock = Client((host, porta))
            mysock.send(bytes("done","utf-8"))
            mysock.send(final)
            ok = True
            if toprint: print("sent")
            count+= 1
            if toprint: print(count)
        except Exception as e:
            print(str(e))
            if ok is True:
                print ("Error in answering the master")
            ok = False
            break
        mysock.close() #closes the connections
saida = input("Type enter to exit")