import socket
from collections import OrderedDict
from random import randint
import subprocess
print("Version 1.0.1 for Uca Cluster")

s = socket.socket()         # Create a socket object and sets up the ports and population size (play with it if you want)
host = "192.168.25.14"
port = 600
quant_populacao = 8

#basic functions to limit the range of numbers

def returnvalues(x):
    valores = [i[1] for i in list(x.items())]
    return valores

def nothousand(x):
    if x >= 999:
        return 999
    else:
        return x
def nothreethousand(x):
    if x >= 2000:
        return 2000
    else:
        return x
def no500(x):
    if x >= 500:
        return 500
    else:
        return x

def maior(x,minimum):
    if x >= minimum:
        return x
    else:
        return minimum
#initializing and using the population as a ordered dict

num_rounds = int(input("Type the number of rounds: "))
populacao = OrderedDict()
filhos = []
#the children are data lists, when they get processed they turn into a ordered dict with their pontuation as key
for i in range(0,quant_populacao):
    minimal = randint(0,200)
    filhos.append([str(randint(1,999)) + "," + str(randint(30,2000)) + "," + str(minimal) + "," + str(randint(minimal,500))])
print ("Initial Population:")
print (filhos)
print ("-----")
main_count = 0

for i in range(0,num_rounds):
    if main_count != 0:
        #Order the population, filter the two more fit, and then reproduce them introducing some random mutations
        populacao = OrderedDict(reversed(sorted(populacao.items(), key=lambda x: x[1])))
        pai = populacao.popitem(last = False)
        mae = populacao.popitem(last = False)
        configs_pai = [int(i) for i in pai[0].split(",")] # turn them into lists
        configs_mae = [int(i) for i in mae[0].split(",")]
        configs_filho = [int((configs_pai [0] + configs_mae[0]) / 2),int((configs_pai [1] + configs_mae[1]) / 2),int((configs_pai [2] + configs_mae[2]) / 2),int((configs_pai [3] + configs_mae[3]) / 2)] # creates the base-child
        filhos = []
        for i in range(0,quant_populacao - 2): # creates the new children with random limited mutations
            menor = no500(configs_filho[2] + randint(-40,40))
            new_filho = [
            nothousand(configs_filho[0] + randint(-60,60)),
            nothreethousand(configs_filho[1] + randint(-120,120)),
            menor,
            no500(maior(configs_filho[3] + randint(-40,40),menor))
            ]
            filhos.append(new_filho)
        filhos.append(configs_pai) #it adds a mother and a father clone, so the population can never go worst (or can it?)
        filhos.append(configs_mae)
        print ("------------")
        print("New population:")
        print (filhos)
        print ("------------")

    populacao = OrderedDict()
    #start the multiprocessing
    conta = 0
    s = socket.socket()
    s.bind((host, port))        # Bind to the port
    s.listen(20)
    ok = True #the ok variable is the variable that allows printing, i put it here to avoid excessive printing
    while len(populacao) < len(filhos):
        if ok is True: #some data reports along the processing
            print ("----------")
            print (len(populacao))
            print(populacao)
            print (len(filhos))
            print(conta)
            print ("----------")
        try:
            if ok is True:
                print ("Wainting connections")
            c, addr = s.accept()     # Establish connection with slave.
            status = c.recv(1024).decode('utf-8') #gets the status message and then decode
            if ok is True:
                print (str(addr[0]) + " is " + str(status.split("|")[0]))
            if status == "ready" and conta < len(filhos): # checks if the slave is ready for a task and if there is tasks avaliable
                c.send (bytes(",".join([str(i) for i in filhos[conta]]),"utf-8")) # sends the next task
                conta += 1
                ok = True
            elif str(status.split("|")[0]) == "done": # if the slave is done, it means it finished a task and is returning the result data
                print(status) #gathers the data and puts into the ordered dict
                chave = status.split("|")[1]
                valor = status.split("|")[2]
                populacao.update({chave : valor})
                print (populacao)
                ok = True
            else:
                c.send(bytes("wait","utf-8")) #if the status is ready but there is no task, it orders the slave to wait and closes the connection, proceeding to process the next slave and so on
                ok = False
        except Exception as e:
            print ("An error ocurred")
            print (str(e))
    print("---------------") #prints the data and appends the data to a txt file
    valores =[int(i) for i in returnvalues(populacao)]
    media = sum(valores) / len(valores)
    arquivo = open("data.txt","a")
    arquivo.write(str(main_count) + " " + str(media) + "\n")
    print ("Round number %d finished" % main_count)
    print("The average of rounds lived is: %f" % media)
    print("---------------")
    main_count += 1
    filhos = [] #erases the children


print ("----------")
print ("The simulation is finished")
print ("The remaining population:")
print (populacao)
print("---------")
saida = input("Type enter to exit")
