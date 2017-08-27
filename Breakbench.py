#quanto tempo demora para quebrar x senhas de 5 caracteres.
#MESTRE
#Versão 1.0.0
import socket
import sys
import time
import random
import math
print("Brute force decryption benchmarker for paralel Python networks")
print("Version 1.0.0")
arquivonome = input("The name of the log file> ")
size = int(input("The number of keys to decrypt: "))
blocksize = int(input("Type the size of each block> "))
porta = 600
ok = True #the ok is again, to avoid excessive printing
conectados = set()
finished = False
log = []
tempo = time.localtime()
log.append("Benchmark ready to start, today is " + "|".join([str(tempo[2]),str(tempo[1]),str(tempo[0])]) + " and the time is " + "|".join([str(tempo[3]),str(tempo[4]),str(tempo[5])]))
def record(x,codigo,address):
    tempo = time.localtime()
    momento = "|".join([str(tempo[3]),str(tempo[4]),str(tempo[5])])
    reports = ["and received the block %d"%x,"and delivered the block %d"%x]
    texto = str(address) + " connected at "+ momento + " " + reports[codigo]
    log.append(texto)
    return True
def gen(size):
    alfabeto = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    return "".join([alfabeto[random.randint(0,len(alfabeto)-1)] for i in range(size)])
while not finished:
    try:
        s = socket.socket()         # Create a socket object and sets up the ports and population size (play with it if you want)
        host = socket.gethostname()
        port = 600
        print("Host is up!")
        log.append("Host is up!")
    except Exception as e:
        print("Fatal error N1")
        log.append("Fatal error N1")
        finished = True
        print(str(e))
        log.append(str(e))
        break
    try:
        s = socket.socket()
        s.bind(("", port))        # Bind to the port
        print("Host is now ready!")
        log.append("Host is now ready!")
    except Exception as e:
        log.append("Fatal error N2")
        log.append(str(e))
        print("Fatal error N2")
        print(str(e))
    print("Ready to generate hashes")
    hashes = [gen(5) for i in range(size)]
    blockchain = [None for i in range(int(size/blocksize) + (size%blocksize))]
    print("Hashes generated, ready to peform connections:")
    log.append("Hashes generated, ready to peform connections:")
    s.listen(20)
    count = 0
    blockcount = 0
    start = time.time()
    progress = 0
    blockquantity = math.ceil(size/blocksize)
    print(blockquantity)
    while progress < blockquantity :
        print(progress)
        try:
            if ok is True:
                print ("Waiting connections")
            c, addr = s.accept()     # Establish connection with slave.
            status = c.recv(1024).decode('utf-8') #gets the status message and then decode
            if status == "ready":
                if blockcount < blockquantity:
                    if not(count + blocksize < size):
                        blocksize = size - count
                    block = "|".join(hashes[count:count+blocksize]) + ":" + str(blockcount)
                    c.send(bytes(block,"utf-8"))
                    count += blocksize
                    blockchain[blockcount] = False
                    record(blockcount,0,addr)
                    blockcount+=1
                else:
                    c.send(bytes("wait","utf-8"))
            elif status.split("|")[0] == "done":
                finishblock = int(status.split("|")[1])
                blockchain[finishblock] = True
                record(finishblock,1,addr)
                c.send(bytes("wait","utf-8"))
                progress += 1
            conectados.add(addr[0])
        except Exception as e:
            log.append("Fatal error N3: problem in talking with servant")
            print("Fatal error N3: problem in talking with servant")
            print(str(e))
            log.append(str(e))
        if not progress < blockquantity:
            finished = True
        print(finished)
print("%d Hashes have been broken by use of bruteforce"%size)
print("Those were the servants that took part in the process:")
print(conectados)
print("A total of %d servants"%len(conectados))
finish = time.time()
deltatime = finish - start
print("it took %f seconds to process it all"%deltatime)
log.append("%d Hashes have been broken by use of bruteforce"%size)
log.append("Those were the servants that took part in the process:")
log.append(str(conectados))
log.append("A total of %d servants"%len(conectados))
log.append("it took %f seconds to process it all"%deltatime)
arquivo = open(arquivonome,"w")
arquivo.write("\n".join(log))
arquivo.close()
