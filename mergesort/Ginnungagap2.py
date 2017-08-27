import socket
import random
import mergesort
import time
import pickle
import sys
print("Ginnungagap server version 1.0.0 for UCA Cluster, based in Heimdall")

s = socket.socket()         # Create a socket object and sets up the ports and population size (play with it if you want)
#host = input("Enter the hostname> ")
port = 666
host = "192.168.25.14"
lsize = 4000000
chunksize = 1000000
toprint = False
toprintresult = False
#initializing and using the population as a ordered dict

#lsize = int(input("Type the size of the list: "))
#chunksize = int(input("Enter the chunksize: "))
#toprint = not input("Should print? (y or n)> ") == "n"
#toprintresult = not input("Should print the result? (y or n)> ") == "n"
print("Generating and shuffling list")
lista = list(range(lsize))
random.shuffle(lista)
print("list shuffled, starting dividing")
subs = []
size = int(lsize/chunksize)
for i in range(size):
    subs.append(lista[i*chunksize:i*chunksize+chunksize])
print("list done, starting multiprocessing")
#start the multiprocessing
conta = 0
s = socket.socket()
s.bind((host, port))        # Bind to the port
s.listen(20)
thelis = []
start = time.time()
ok = True #the ok variable is the variable that allows printing, i put it here to avoid excessive printing
while len(thelis) < lsize:
    if ok is True and toprint: #some data reports along the processing
        print ("----------")
        print (len(thelis))
        print ("----------")
    try:
        if ok is True and toprint:
            print ("Waiting connections")
        c, addr = s.accept()     # Establish connection with slave.
        status = c.recv(40).decode('utf-8') #gets the status message and then decode
        if ok is True and toprint:
            print (str(addr[0]) + " is " + str(status.split("|")[0]))
        if status == "ready" and conta < len(subs): # checks if the slave is ready for a task and if there is tasks avaliable
            content = pickle.dumps(subs[conta])
            #print(sys.getsizeof(content))
            c.send (content) # sends the next task
            conta += 1
            ok = True
        elif status == "done": # if the slave is done, it means it finished a task and is returning the result data #gathers the data and puts into the ordered dict
            c.send(bytes("send it","utf-8"))
            resmsg = c.recv(16777216)
            resultsorted = pickle.loads(resmsg)
            #print(len(resultsorted))
            if len(resultsorted) == 0:
                print("fuuuuck")
                raise("fuck")
            if toprint:
                print("Received a sorted list")
            thelis = mergesort.merge(thelis,resultsorted)
            ok = True
        else:
            c.send(bytes("wait","utf-8")) #if the status is ready but there is no task, it orders the slave to wait and closes the connection, proceeding to process the next slave and so on
            ok = False
    except Exception as e:
        print ("An error ocurred")
        print(status)
        print (str(e))
print ("----------")
print ("The ordering is finished")
if toprintresult:
    print(thelis)
final = time.time()-start
print(final)
print("---------")
with open("times.txt", "a") as myfile:
    myfile.write(str(final)+"\n")
#saida = input("Type enter to exit")
