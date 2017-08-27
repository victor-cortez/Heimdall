import socket
import sys
import time
from ploxys import main

host = input("Type the master's ip: ")
porta = 600
ok = True #the ok is again, for avoid excessive printing
while True:
    time.sleep(0.1) #basic time waiting so it wont flood the connection
    while True:
        resultado = 0 #reset data
        final = 0
        resposta = 0
        inputs = []
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
            resposta = mysock.recv(1024).decode("utf-8") #receives the task or the waiting command
            mysock.close()
            if resposta == "wait": #if it must wait, the slave will break the loop  and get inside it again
                break
            print ("Got a task: " + resposta) #if it received a task, it will print it
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
            resultado = main(inputs[0],inputs[1],inputs[2],inputs[3]) #inputs the data into the ploxys function
            ok = True
        except:
            e = sys.exc_info()[0]
            if ok is True:
                print ("Error %s" % e)
                print("Error in calculating result, maybe data could not been found")
            ok = False
            break
        try:
            final = "done|" + resposta + "|" + str(resultado) #formats the resulting data as the protocol demands
            print (resultado)
            mysock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #sets the connections, connects and sends the data
            mysock.connect((host,porta))
            mysock.send(final.encode("utf-8"))
            ok = True
        except:
            if ok is True:
                print ("Error in answering the master")
            ok = False
            break
        mysock.close() #closes the connections
saida = input("Type enter to exit")