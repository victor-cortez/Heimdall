import socket
import random
import os
import joblib
index = {}
anun = {}
com = {}
dirdata = os.listdir(os.getcwd())
if "index.txt" in dirdata:
    index = joblib.load("index.txt")
if "anun.txt" in dirdata:
    anun = joblib.load("anun.txt")
def addindex(data):
    header,content = data
    if header in index.keys():
        index[header].add(content)
    else:
        index[header] = set([content])
def removeindex(data):
    header,content = data
    if header in index.keys():
        index[header].remove(content)
        if len(index[header]) == 0:
            del index[header]
def ask(header):
    if header in index.keys():
        return ",".join(index[header])
    else:
        return "None"
def addanun(data):
    header,content = data
    if header in anun.keys():
        anun[header].add(content)
    else:
        anun[header] = set([content])
def removeanun(data):
    header,content = data
    if header in anun.keys():
        anun[header].remove(content)
        if len(anun[header]) == 0:
            del anun[header]
def askanun(header):
    if header in anun.keys():
        return ",".join(anun[header])
    else:
        return "None"
def giveanun():
    if len(anun.keys()) > 0:
        x = random.choice(list(anun.keys()))
        print("ok " + x)
        return str(x) + "|" + ",".join(anun[x])
    else:
        return "None"
try:
    print("Draugr server version 1.0.0 for UCA Cluster, based in Heimdall")
    s = socket.socket()
    host = input("Enter the hostname> ")
    toprint = not input("Should print? (y or n)> ") == "n"
    port = 775
    s.bind((host, port))        # Bind to the port
    s.listen(20)
    ok = True
    conti = True
    while conti:
        try:
            if ok is True and toprint:
                print ("Waiting connections")
            c, addr = s.accept()     # Establish connection with slave.
            status = c.recv(8192).decode('utf-8') #gets the status message and then decode
            if ok is True and toprint:
                print (addr,status)
            print(status)
            op,cont = status.split("|")
            if op == "addindex":
                addindex(cont.split(","))
                c.send(bytes("ok","utf-8"))
            elif op == "removeindex":
                removeindex(cont.split(","))
                c.send(bytes("ok","utf-8"))
            elif op == "ask":
                c.send(bytes(ask(cont),"utf-8"))
            elif op == "addanun":
                addanun(cont.split(","))
                c.send(bytes("ok","utf-8"))
            elif op == "removeanun":
                removeanun(cont.split(","))
                c.send(bytes("ok","utf-8"))
            elif op == "askanun":
                c.send(bytes(askanun(cont),"utf-8"))
            elif op == "giveanun":
                c.send(bytes(giveanun(),"utf-8"))
            elif op == "log":
                ip,port = cont.split(",")
                port = int(port)
                if port in com.values():
                    c.send(bytes("already","utf-8"))
                else:
                    com[ip] = port
                    c.send(bytes("ok","utf-8"))
            elif op == "asklog":
                if cont in com.keys():
                    c.send(bytes(str(com[cont]),"utf-8"))
                else:
                    c.send(bytes("not","utf-8"))
            else:
                print("Error in identifying operation")
                ok = False
        except KeyboardInterrupt:
            print("Saving the current data")
            joblib.dump(index,"index.txt")
            joblib.dump(anun,"anun.txt")
            conti = False
        except Exception as e:
            print ("An error ocurred")
            print (str(e))
            break
except Exception as e:
    print("FATAL ERROR!")
    print(str(e))
print("Saving the current data")
joblib.dump(index,"index.txt")
joblib.dump(anun,"anun.txt")