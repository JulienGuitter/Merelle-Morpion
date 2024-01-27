from Commun import pos,cls,newInput
from colorama import Fore, Back, Style, init
from socket import AF_INET, SOCK_STREAM, socket
from multi.morpion import mainMorpion
from multi.merelle import mainMerelle

init()

# ---------- fonction de communication avec le server
def connexion():
    hote = "i-want-play-games.tk"
    port = 12800

    server = socket(AF_INET, SOCK_STREAM)
    server.connect((hote, port))
    print("Connexion avec le server etablie")
    return server

def sendData(server, dataToSend):
    dataToSend = dataToSend.encode()
    server.send(dataToSend)

# ---------- fin des fonctions de communication avec le server

def menu(server):
    cls()
    print("\n\tMenu online\n")
    print("1) Morpion")
    print("2) Merelle")
    print("3) retour menu principal")
    choix = newInput(1,3, "\nVotre choix (1 a 3) : ")
    if choix == 1:
        menuMorpion(server)
    elif choix == 2:
        menuMerelle(server)

def menuMorpion(server):
    cls()
    print("\n\tMorpion online\n")
    print("1) join")
    print("2) create")
    print("3) retour menu principal")
    choix = newInput(1,3, "\nVotre choix (1 a 3) : ")
    if choix == 1:
        menuJoinGame(server, 0)
    elif choix == 2:
        menuMorpionCreateGame(server)
    elif choix == 3:
        menu(server)

def menuMorpionCreateGame(server):
    cls()
    print("\n\tCreate morpion game\n")
    print("1) 3x3")
    print("2) 4x4")
    print("3) 5x5")
    print("4) retour")
    choix = newInput(1,4, "\nVotre choix (1 a 4) : ")
    if choix == 1:
        #create 3x3 game
        sendData(server, "c003")
    elif choix == 2:
        #create 4x4 game
        sendData(server, "c004")
    elif choix == 3:
        #create 5x5 game
        sendData(server, "c005")
    elif choix == 4:
        menu(server)
    if choix != 4:
        menuAttente(server, 0)

def menuMerelle(server):
    cls()
    print("\n\tMerelle online\n")
    print("1) join")
    print("2) create")
    print("3) retour menu principal")
    choix = newInput(1,3, "\nVotre choix (1 a 3) : ")
    if choix == 1:
        menuJoinGame(server, 1)
    elif choix == 2:
        menuMerelleCreateGame(server)
    elif choix == 3:
        menu(server)

def menuMerelleCreateGame(server):
    cls()
    print("\n\tCreate merelle game\n")
    print("1) normal")
    print("2) retour")
    choix = newInput(1,2, "\nVotre choix (1 a 2) : ")
    if choix == 1:
        #create merelle game
        sendData(server, "c100")
    elif choix == 2:
        menu(server)
    if choix != 2:
        menuAttente(server, 1)

def startParty(server, game):
    partyInfo = server.recv(1024).decode()
    if partyInfo == "notExist":
        print("Cette partie existe pas ou est deja complete")
        input("appuyer sur entrer pour afficher la list")
        if game == 0:
            menuMorpion(server)
        else:
            menuMerelle(server)
    else:
        if game == 0:
            mainMorpion(partyInfo, server)
            menuMorpion(server)
        else:
            mainMerelle(partyInfo, server)
            menuMerelle(server)

def menuAttente(server, game):
    cls()
    print("\n\n\n\tEn attente d'un joueur ...\n")
    startParty(server, game)

def menuJoinGame(server, game):
    cls()
    listGame = []
    if game == 0:
        sendData(server, "a0")
    else:
        sendData(server, "a1")
    getData = server.recv(1024).decode()
    if getData == "start":
        data = ""
        while getData[-3:] != "end":
            getData = server.recv(1024).decode()
            data+=getData
        newData = data[:-4].split("/")
        for carac in newData:
            listGame.append(carac)
    else:
        print("Service indisponible")
        input("Appuyer sur entrer pour retourner au menu")
        menu(server)
    if game == 0:
        print("\n\tJoin morpion game\n")
    else:
        print("\n\tJoin merelle game\n")
    for i in range(int(len(listGame)/4)):
        if listGame[i*4] == "0" and game == 0:
            print(i,") morpion ", listGame[i*4+2],"x",listGame[i*4+2], sep="")
        elif listGame[i*4] == "1" and game == 1:
            print(i, ") merelle", sep="")
    print(int(len(listGame)/4),") actualiser", sep="")
    print(int(len(listGame)/4)+1,") retour", sep="")
    choix = newInput(0, len(listGame)/4+1, "\nVotre choix (0 a "+str(int(len(listGame)/4)+1)+") : ")
    if choix == int(len(listGame)/4):
        menuJoinGame(server, game)
    elif choix == int(len(listGame)/4+1):
        if game == 0:
            menuMorpion(server)
        else:
            menuMerelle(server)
    else:
        dataToSend = "j/"+listGame[choix*4+1]
        server.send(dataToSend.encode())
        startParty(server, game)

def main():
    server = None
    cls()
    pos(4,6)
    print(Fore.GREEN,"Connection avec le serveur ...",Fore.RESET, sep="")
    try:
        server = connexion()
        menu(server)
    except:
        cls()
        pos(4,6)
        print(Fore.GREEN,"Une erreur est survenue avec le server", sep="")
        pos(4,7)
        input("appuyer sur entrer pour retourner au menu")
        print(Fore.RESET)


