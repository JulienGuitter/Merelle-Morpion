from Commun import cls, pos, newInput
from colorama import Fore, Back, Style


def printCircle(x,y):
    x=x*9+4
    y=y*8+3
    for j in range(2):
        for i in range(3):
            pos(2+x+i,1+y+j*4)
            print(Back.BLUE," ",sep="")
            pos(1+x+j*4,2+y+i)
            print(Back.BLUE," ",sep="")

def printCross(x,y):
    x=x*9+4
    y=y*8+3
    for i in range(5):
        pos(1+x+i,1+y+i)
        print(Back.RED," ", sep="")
        pos(5+x-i,1+y+i)
        print(Back.RED," ", sep="")

def printBoard(size):
    for i in range(size-1):
        for j in range(size*7+2+(size-3)):
            pos(11+i*9,j+3)
            print(Back.GREEN,"  ", sep="")
        for j in range(size*8+1+(size-3)):
            pos(4+j,10+i*8)
            print(Back.GREEN," ", sep="")

def morpionInterface(error ,board, size):
    cls()
    printBoard(size)
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == "1":
                printCircle(i, j)
            elif board[i][j] == "2":
                printCross(i, j)
    pos(3, 29 + (size - 3) * 8)
    print(Fore.RED, error, Style.RESET_ALL, sep="")

def getBoard(server, size, board):
    data = server.recv(1024).decode()
    if data == "l" or data == "w" or data == "error" or data == "dec" or data == "execo":
        canPlaced, finish = testEndGameMessage(data, server, size, board)
        return 1
    else:
        while data[-1:] != "e":
            data += server.recv(1024).decode()
        itemPos = 0
        for i in range(size):
            for j in range(size):
                board[i][j] = data[itemPos]
                itemPos+=1
    return 0

def testEndGameMessage(validationPos, server, size, board):
    canPlaced = False
    if validationPos == "ok":
        canPlaced = True
        getBoard(server, size, board)
    elif validationPos == "l":
        print("vous avez perdu")
    elif validationPos == "w":
        print("vous avez gagner")
    elif validationPos == "execo":
        print("La partie est nul")
    elif validationPos == "error":
        print("Cette case est deja prise")
    elif validationPos == "ze":
        print("Le joueur adverse c'est deconnecter")
    if validationPos != "error" and validationPos != "ok":
        input("appuyer sur entrer pour retourner au menu")
        return canPlaced, 1
    return canPlaced, 0

def getPlayerPos(server, size, board):
    canPlaced = False
    while not canPlaced:
        pos(3, 28 + (size - 3) * 8)
        x = newInput(0, size - 1,"Choisiser la case pour X (0 a " + str(size - 1) + ") : ")
        error = ""
        morpionInterface(error, board, size)
        pos(3, 28 + (size - 3) * 8)
        y = newInput(0, size - 1,"Choisiser la case pour Y (0 a " + str(size - 1) + ") : ")
        posData = str(x)+str(y)
        server.send(posData.encode())
        validationPos = server.recv(1024).decode()
        canPlaced, finish = testEndGameMessage(validationPos, server, size, board)
        if finish == 1:
            return 1
    return 0

def mainMorpion(firstPlayer, server):
    size = int(server.recv(1024).decode())
    board = [[0 for i in range(size)] for i in range(size)]
    morpionInterface("", board, size)
    end = 0
    if firstPlayer == "youStart":
        end = getPlayerPos(server, size, board)
    while end == 0:
        cls()
        morpionInterface("", board, size)
        print("En attente de l'autre joueur ...")
        end = getBoard(server, size, board)
        if end == 0:
            cls()
            morpionInterface("", board, size)
            end = getPlayerPos(server, size, board)