import socket
#This is the slave version of the benchmark
host = input("Digite o ip do mestre: ")
porta = 600
ok = True
finished = False
def process(item):
    alfabeto = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    for a in alfabeto:
        for b in alfabeto:
            for c in alfabeto:
                for d in alfabeto:
                    for e in alfabeto:
                        if a+b+c+d+e == item:
                            return True
while not finished:
    while not finished:
        resultado = 0
        final = 0
        resposta = 0
        inputs = []
        try:
            mysock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # cria o socket
        except socket.error:
            if ok is True:
                print ("Error in creating the socket") # Encerra com status de erro
            ok = False
            break
        try:
            mysock.connect((host,porta))  # conecta ao host
            ok = True
        except Exception as e:
            if ok is True:
                print(str(e))
                print ("Error in connecting with the master")
            ok = False
            break
        ok = False
        while not ok:
            try:
                 # Obtem os dados a serem enviados
                mysock.send(bytes("ready","utf-8"))  # envia os dados para o servidor
                resposta = mysock.recv(1024).decode("utf-8")
                mysock.close()
                if resposta == "wait":
                    break
                print ("Got a task: " + resposta)
                ok = True
            except:
                e = sys.exc_info()[0]
                if ok is True:
                    print ("Error in communicating with master")
                    print ("Error %s" % e)
                ok = False
                break
        try:
            print(resposta)
            if resposta == "wait":
                finished = True
                break
            data,number = resposta.split(":")
            number = int(number)
            data = data.split("|")
            print(data)
            resultado = process(data)
            ok = True
        except:
            e = sys.exc_info()[0]
            if ok is True:
                print ("Error %s" % e)
                print("Error in calculating result, maybe data could not been found")
            ok = False
            break
        ok = False
        while not ok:
            try:
                final = "done|" +str(number)
                mysock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                mysock.connect((host,porta))
                mysock.send(final.encode("utf-8"))
                ok = True
            except:
                if ok is True:
                    print ("Error in answering the master")
                ok = False
                break
        mysock.close()
saida = input("Digite Enter para sair")
