import socket
import sys
import random
import joblib
mem = {}
server = "192.168.25.14"
porta = 775
def comserver(host,porta,message):
    ok = True
    while True:
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
            mysock.send(bytes(message,"utf-8"))  # sends the ready status to the server
            resposta = mysock.recv(8192).decode("utf-8") #receives the task or the waiting command
            mysock.close()
            ok = True
        except:
            e = sys.exc_info()[0]
            if ok is True:
                print ("Error in communicating with master")
                print ("Error %s" % e)
            ok = False
            break
        mysock.close() #closes the connections
        return resposta
    return None
def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]
def upload(filename):
    f = open(filename,"rb")
    archive = f.read()
    packs = list(chunks(archive,16384))
    lh = 100
    hsheader = ''.join(chr(random.randint(97,122)) for i in range(lh))
    size = len(packs)
    IP = socket.gethostbyname(socket.gethostname())
    for i in range(size):
        header = hsheader+"/"+str(size)+"/"+str(i)
        ms = "addindex|"+header+","+IP
        mem[header] = packs[i]
        comserver(server,porta,ms)
    joblib.dump(hsheader+"/"+str(size),filename.split(".")[0] + ".dr")
    return hsheader+"/"+str(size)
def log(ip):
    print("Starting logging the computer to the network")
    finished = False
    while not finished:
        port = random.randint(800,2000)
        res = comserver(server,porta,"log|"+ip+","+str(port))
        if res == "ok":
            finished = True
    print("Login finished")
    return port
giving = False
def give():
    s = socket.socket()         # Create a socket object and sets up the ports and population size (play with it if you want)
    host = input("Enter yout hostname> ")
    port = log(host)
    s.bind((host, port))        # Bind to the port
    s.listen(20)
    ok = True
    toprint = True
    while True:
        try:
            if ok is True and toprint:
                print ("Waiting connections")
            c, addr = s.accept()     # Establish connection with slave.
            status = c.recv(1048576).decode('utf-8') #gets the status message and then decode
            if status in mem.keys():
                c.send(bytes("found","utf-8"))
                c.recv(1024).decode("utf-8")
                c.sendall(mem[status])
            else:
                c.send(bytes("404","utf-8"))
        except Exception as e:
            print ("An error ocurred")
            print (str(e))

def download(filename):
    if "." in filename:
        preheader = joblib.load(filename)
    else:
        preheader = filename
    failed = []
    size = int(preheader.split("/")[1])
    ok = True
    for i in range(size):
        header = preheader + "/" + str(i)
        beholders = comserver(server,porta,"ask|"+header)
        if beholders == "None":
            failed.append(i)
        else:
            beholders = beholders.split(",")
            target = random.choice(beholders)
            port = int(comserver(server,porta,"asklog|"+target))
            if port == "not":
                failed.append(i)
            else:
                try: #lots of error handling and error reporting
                    mysock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # creates the socket
                except socket.error:
                    if ok is True:
                        print ("Error in creating the socket") # Finishes with error report
                    ok = False
                    break
                try:
                    mysock.connect((target,port))  # connects to the host
                    ok = True
                except socket.error:
                    if ok is True:
                        print ("Error in connecting with the source")
                    ok = False
                    break
                try:
                    mysock.send(bytes(header,"utf-8"))  # sends the header
                    resposta = mysock.recv(1048576).decode("utf-8") #receives the answer
                    if resposta == "found": #if it must wait, the slave will break the loop  and get inside it again
                        mysock.send(bytes("ok","utf-8"))#sends confirmation
                        arcfile = mysock.recv(16384)#receives the file
                        mem[header] = arcfile
                    else:
                        failed.append(i)
                    ok = True
                except Exception as e:
                    if ok is True:
                        print("Problem in data transfer")
                        print(str(e))
    return failed
def harden(filename,name):
    if "." in filename:
        preheader = joblib.load(filename)
    else:
        preheader = filename
    failed = []
    size = int(preheader.split("/")[1])
    data = []
    for i in range(size):
        header = preheader + "/" + str(i)
        if header in mem.keys():
            data.append(mem[header])
        else:
            failed.append(i)
    if len(failed) == 0:
        d = b"".join(data)
        ar = open(name,"wb")
        ar.write(d)
        ar.close()
        print("lol")
        return True
    else:
        print(failed)
        return False


#upload("image.jpg")
#harden("image.dr","image2.jpg")


