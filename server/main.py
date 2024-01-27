from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread, get_ident
from random import randrange
from morpion import morpionTestPos
from merelle import merelleTestPos
from colorama import init, Back, Fore, Style

def connexion():
    hote = ""
    port = 12800

    server = socket(AF_INET, SOCK_STREAM)
    server.bind((hote, port))
    server.listen(5)
    return server

def pos(x, y):
    print("\x1b[" + str(y) + ";" + str(x) + "H", end="")

def cls():
    print("\x1b[2J\x1b[H",end="")

def cyanLigne(height, posY):
    for j in range(1,height+1):
        for i in range(100):
            pos(i,j+posY)
            print(Back.CYAN," ",Back.RESET,sep="")

def jolieAffichage(printSetting, party):
    cls()
    cyanLigne(2, 0)
    pos(3,1)
    print(Back.CYAN, Fore.BLACK,"Serveur de jeux pour morpion et merelle",sep="")
    pos(3,2)
    print("Player connected : ",printSetting["user"],Style.RESET_ALL, sep="")
    pos(4,5)
    print("Morpion Game : ",printSetting["morpionGame"], sep="")
    pos(40,5)
    print("Merelle Game : ",printSetting["merelleGame"], sep="")
    iMorp = 0
    iMere = 0
    for i in range(len(party)):
        textToPrint = ""
        if party[i]["game"] == "0":
            textToPrint += "ID:"+str(party[i]["id"])+", "+str(party[i]["size"])+"x"+str(party[i]["size"])
            if party[i]["player2"] != None:
                textToPrint += ", en cours"
            else:
                textToPrint += ", en attente"
            pos(4, 7+iMorp)
            iMorp += 1
        if party[i]["game"] == "1":
            textToPrint += "ID:"+str(party[i]["id"])+", Normal"
            if party[i]["player2"] != None:
                textToPrint += ", en cours"
            else:
                textToPrint += ", en attente"
            pos(40, 7+iMere)
            iMere+=1
        print(textToPrint)
    cyanLigne(2, 21)
    pos(3,22)
    print(Back.CYAN, Fore.BLACK,"Created by : Julien Guitter, Matthieu Menager",sep="")
    pos(3,23)
    print("Version : 1.0",Style.RESET_ALL,sep="")

def acceptConnexion(server):
    party = []
    partyIdByClient = {}
    printSetting = {"user":0, "morpionGame":0, "merelleGame":0}
    jolieAffichage(printSetting, party)
    while True:
        client, clientInfo = server.accept()
        Thread(target=clientAction, args=(client, party, partyIdByClient, printSetting)).start()

def sendData(client, data):
    client.send(b"start")
    for content in data:
        client.send(str(content).encode())
        client.send(b"/")
    client.send(b"end")

def configParty(party, client, data, partyIdByClient, printSetting):
    # data info par index : 0 = creer ou rejoindre, 1 = jeux, 2 = variante, 3 = size du plateau
    if data[0] == "c":
        # create party
        if data[1] == "0":
            board = [[0 for i in range(int(data[3]))] for i in range(int(data[3]))]
            printSetting["morpionGame"] += 1
        else:
            board = [[[0 for i in range(3)] for i in range(3)] for i in range(3)]
            printSetting["merelleGame"] += 1
        game = {"id":get_ident(), "player1": client, "player2": None, "game":data[1], "variante": data[2], "size": data[3], "private":False, "turn":randrange(0,2), "board":board, "step":1, "pieces":[0,0]}
        party.append(game)
    elif data[:2] == "j/":
        # join party
        clientSendID = data[2:]
        gameId = None
        for i in range(len(party)):
            if party[i]["id"] == int(clientSendID) and party[i]["player2"] == None:
                gameId = i
        if gameId != None:
            if party[gameId]["player1"] != None:
                party[gameId]["player2"] = client
                if party[gameId]["turn"] == 0:
                    party[gameId]["player1"].send(b"youStart")
                    client.send(b"youWait")
                else:
                    party[gameId]["player1"].send(b"youWait")
                    client.send(b"youStart")
                partyIdByClient[party[gameId]["player1"]] = gameId
                partyIdByClient[client] = gameId
                if party[gameId]["game"] == "0":
                    party[gameId]["player1"].send(party[gameId]["size"].encode())
                    client.send(party[gameId]["size"].encode())
            else:
                client.send(b"notExist")
        else:
            client.send(b"notExist")
    elif data[0] == "a":
        #send list party
        sendListGame = []
        if party:
            for i in range(len(party)):
                if party[i]["player2"] == None and party[i]["player1"] != None and party[i]["game"] == data[1]:
                    sendListGame.append(party[i]["game"])
                    sendListGame.append(party[i]["id"])
                    sendListGame.append(party[i]["size"])
                    sendListGame.append(party[i]["variante"])
        sendData(client, sendListGame)

def clientAction(client, party, partyIdByClient, printSetting):
    printSetting["user"] += 1
    while True:
        jolieAffichage(printSetting, party)
        try:
            data = client.recv(1024).decode()
            if data:
                if party:
                    # des party existe, il faut tester si le joueur est dans une
                    id = -1
                    for i in range(len(party)):
                        if party[i]["player1"] == client or party[i]["player2"] == client:
                            id = i
                    if id >= 0:
                        #le joueur est deja dans une party
                        gameId = partyIdByClient[client]
                        if party[gameId]["game"] == "0":
                            morpionTestPos(client,party[gameId], data, party)
                        else:
                            merelleTestPos(client,party[gameId], data, party)
                    else:
                        #le joueur est dans aucune des party
                        configParty(party, client, data, partyIdByClient, printSetting)
                else:
                    #aucune party n'existe
                    configParty(party, client, data, partyIdByClient, printSetting)
            else:
                if party:
                    for i in range(len(party)):
                        if party[i]["player1"] == client and party[i]["player2"] != None:
                            party[i]["player2"].send(b"ze")
                        elif party[i]["player2"] == client and party[i]["player1"] != None:
                            party[i]["player1"].send(b"ze")

                        if party[i]["player1"] == client or party[i]["player2"] == client:
                            if party[i]["game"] == "0":
                                printSetting["morpionGame"] -= 1
                            elif party[i]["game"] == "1":
                                printSetting["merelleGame"] -= 1
                            party.remove(party[i])
                client.close()
                printSetting["user"] -= 1
                jolieAffichage(printSetting, party)
                break
        except:
            continue

if __name__ == "__main__":
    init()
    server = connexion()
    acceptConenxionThread = Thread(target=acceptConnexion, args=(server,))
    acceptConenxionThread.start()
    acceptConenxionThread.join()
    server.close()


