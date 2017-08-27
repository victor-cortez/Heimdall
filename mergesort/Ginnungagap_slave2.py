import socket
import sys
import time
from mergesort import mergesort as main
import pickle
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
        inputs = [1,2]
        try: #lots of error handling and error reporting
            mysock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # creates the socket
        except socket.error:
            if ok is True:
                print ("Error in creating the socket") # Finishes with error report
            ok = False
            break
        try:
            mysock.connect((host,porta))  # connects to the host
            ok = True
        except socket.error:
            if ok is True:
                print ("Error in connecting with the master")
            ok = False
            break
        try:
            mysock.send(bytes("ready","utf-8"))  # sends the ready status to the server
            ans = mysock.recv(16777216) #receives the task or the waiting command
            mysock.close()
            if sys.getsizeof(ans) <= 40: #if it must wait, the slave will break the loop  and get inside it again
                print(sys.getsizeof(resposta))
                print(resposta)
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
            inputs = pickle.loads(ans)
            print("ok")
            print(len(inputs))
            print("ok 2")
            if len(inputs) == 0:
                raise("fuck")
            print("ok 3")
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
            mysock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #sets the connections, connects and sends the data
            mysock.connect((host,porta))
            mysock.send(bytes("done","utf-8"))
            r = mysock.recv(40)
            mysock.send(pickle.dumps(resultado))
            ok = True
        except:
            if ok is True:
                print ("Error in answering the master")
            ok = False
            break
        mysock.close() #closes the connections
saida = input("Type enter to exit")
