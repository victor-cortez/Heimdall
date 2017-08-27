import random
import mergesort
from multiprocessing.connection import Listener
print("Ginnungagap server version 1.0.0 for UCA Cluster, based in Heimdall")

host = input("Enter the hostname> ")
port = 666

lsize = int(input("Type the size of the list: "))
chunksize = int(input("Enter the chunksize: "))
toprint = not input("Should print? (y or n)> ") == "n"
toprintresult = not input("Should print the result? (y or n)> ") == "n"
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
s = Listener((host,port))        # Bind to the port
thelis = []
ok = True #the ok variable is the variable that allows printing, i put it here to avoid excessive printing
while len(thelis) < lsize:
    if ok is True and toprint: #some data reports along the processing
        print ("----------")
        print (len(thelis))
        print ("----------")
    try:
        if ok is True and toprint:
            print ("Waiting connections")
        c = s.accept()     # Establish connection with slave.
        status = c.recv().decode('utf-8') #gets the status message and then decode
        if ok is True and toprint:
            print (str(c) + " is " + str(status.split("|")[0]))
        if status == "ready" and conta < len(subs): # checks if the slave is ready for a task and if there is tasks avaliable
            c.send (bytes(",".join([str(i) for i in subs[conta]]),"utf-8")) # sends the next task
            conta += 1
            ok = True
        elif str(status.split("|")[0]) == "done": # if the slave is done, it means it finished a task and is returning the result data #gathers the data and puts into the ordered dict
            resultsorted = [int(i) for i in status.split("|")[1].split(",")]
            if toprint:
                print("Received a sorted list")
            thelis = mergesort.merge(thelis,resultsorted)
            ok = True
        else:
            c.send(bytes("wait","utf-8")) #if the status is ready but there is no task, it orders the slave to wait and closes the connection, proceeding to process the next slave and so on
            ok = False
    except Exception as e:
        print ("An error ocurred")
        print (str(e))
print ("----------")
print ("The ordering is finished")
if toprintresult:
    print(thelis)
print("---------")
saida = input("Type enter to exit")