from multiprocessing.connection import Listener
import random
import time
print("Manananggal AUTO server version 1.0.0 for UCA Cluster, based in Heimdall")
         # Create a socket object and sets up the ports and population size (play with it if you want)
#host = input("Enter the hostname> ")
host = "192.168.102"
port = 666
maxpower = 6
minpower = 4
d = 5

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
toprint = False
toprintresult = True
#print("Generating and shuffling list")
#lista,total = cutter(lsize,chunksize)
#print("list shuffled and cutted")
#print("list done, starting multiprocessing")
#start the multiprocessing
times = []
s = Listener((host, port))
for b in range(minpower,maxpower+1):
    for a in range(1,10):
        used = set()
        conta = 0
       # Bind to the port
        #s = Listener((host, port))
        chunksize = d
        lsize = a * (10**b)
        received = 0
        lista,total = cutter(lsize,chunksize)
        thesize = len(lista)
        #print(lista)
        #print(total)
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
                c = s.accept()     # Establish connection with slave.
                used.add(c.address)
                print(c.address)
                status = c.recv().decode('utf-8') #gets the status message and then decode
                if not didstart:
                    start = time.time()
                    didstart = True
                if ok is True and toprint:
                    print (str(c) + " is " + str(status.split("|")[0]))
                if status == "ready" and conta < thesize: # checks if the slave is ready for a task and if there is tasks avaliable
                    c.send (bytes(str(lista[conta]),"utf-8")) # sends the next task
                    conta += 1
                    ok = True
                elif str(status.split("|")[0]) == "done": # if the slave is done, it means it finished a task and is returning the result data #gathers the data and puts into the ordered dict
                    resultsorted = int(status.split("|")[1])
                    if toprint:
                        print("Received a result")
                    received += 1
                    #print(resultsorted)
                    total += resultsorted
                    ok = True
                else:
                    c.send(bytes("wait","utf-8")) #if the status is ready but there is no task, it orders the slave to wait and closes the connection, proceeding to process the next slave and so on
                    ok = False
                c.close()
            except Exception as e:
                print ("An error ocurred")
                print (str(e))
        final = time.time()
        delta = final - start
        print ("----------")
        print(str(a),str(b))
        print ("The ordering is finished")
        if toprintresult:
            print(total)
        print("It lasted " + str(delta))
        print(str(len(used)))
        print("---------")
        times.append([lsize,delta])
outfile = open("outfile.txt","w")
strtimes = [str(i[0]) + " " + str(i[1]) for i in times]
outfile.write("\n".join(strtimes))
outfile.close()
saida = input("Type enter to exit")