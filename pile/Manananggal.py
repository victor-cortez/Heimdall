import socket
import random
import time
print("Manananggal server version 1.0.0 for UCA Cluster, based in Heimdall")

s = socket.socket()         # Create a socket object and sets up the ports and population size (play with it if you want)
host = input("Enter the hostname> ")
port = 666

#initializing and using the population as a ordered dict
def cutter(tsize,dsize):
    p = [tsize]
    soma = 0
    for i in range(dsize):
        update = []
        for n in p:
            if n == 1:
                soma += 0
            else:
                a = random.randint(1,n-1)
                b = n - a
                soma += a*b
                update.append(a)
                update.append(b)
        p = list(update)
    return(p,soma)
lsize = int(input("Type the size of the pile: "))
chunksize = int(input("Enter the depth: "))
toprint = not input("Should print? (y or n)> ") == "n"
toprintresult = not input("Should print the result? (y or n)> ") == "n"
print("Generating and shuffling list")
lista,total = cutter(lsize,chunksize)
print("list shuffled and cutted")
print("list done, starting multiprocessing")
#start the multiprocessing
conta = 0
s = socket.socket()
s.bind((host, port))        # Bind to the port
s.listen(20)
received = 0
thesize = len(lista)
print(lista)
print(total)
didstart = False
ok = True #the ok variable is the variable that allows printing, i put it here to avoid excessive printing
while received < thesize:
    if ok is True and toprint: #some data reports along the processing
        print ("----------")
        print (received)
        print ("----------")
    try:
        if ok is True and toprint:
            print ("Waiting connections")
        c, addr = s.accept()     # Establish connection with slave.
        status = c.recv(1048576).decode('utf-8') #gets the status message and then decode
        if not didstart:
            start = time.time()
            didstart = True
        if ok is True and toprint:
            print (str(addr[0]) + " is " + str(status.split("|")[0]))
        if status == "ready" and conta < thesize: # checks if the slave is ready for a task and if there is tasks avaliable
            c.send (bytes(str(lista[conta]),"utf-8")) # sends the next task
            conta += 1
            ok = True
        elif str(status.split("|")[0]) == "done": # if the slave is done, it means it finished a task and is returning the result data #gathers the data and puts into the ordered dict
            resultsorted = int(status.split("|")[1])
            if toprint:
                print("Received a result")
            received += 1
            print(resultsorted)
            total += resultsorted
            ok = True
        else:
            c.send(bytes("wait","utf-8")) #if the status is ready but there is no task, it orders the slave to wait and closes the connection, proceeding to process the next slave and so on
            ok = False
    except Exception as e:
        print ("An error ocurred")
        print (str(e))
final = time.time()
delta = final - start
print ("----------")
print ("The ordering is finished")
if toprintresult:
    print(total)
print("It lasted " + str(delta))
print("---------")
saida = input("Type enter to exit")