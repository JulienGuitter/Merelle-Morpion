from colorama import Fore,Back,Style
from Commun import cls, pos, newInput
from random import randrange

def menuMorpion():
    cls()
    print("\t",Back.BLUE,"_____morpion_____",Back.RESET)
    pos(5,5)
    print(Fore.RED,"1) selectioner un mode",Fore.RESET, sep="")
    pos(5,6)
    print(Fore.RED,"2) instruction",Fore.RESET, sep="")
    pos(5,7)
    print(Fore.RED,"3) retour au menu",Fore.RESET, sep="")
    print(Fore.RED, sep="")
    pos(5,9)
    choixmenu = newInput(1,3,"que voulez vous faire : ")
    print(Fore.RESET, sep="", end="")
    if choixmenu == 1:
        modMenu()
    elif choixmenu == 2:
        cls()
        instruction()

def modMenu():
    cls()
    pos(8,2)
    print(Back.BLUE,"Selection du mode de jeu",Back.RESET, sep="")
    pos(4,4)
    print(Fore.RED,"1) Basic (3x3) - 2 Joueur",Fore.RESET, sep="")
    pos(4,5)
    print(Fore.RED,"2) Basic (3x3) - Contre ordinateur",Fore.RESET, sep="")
    pos(4,6)
    print(Fore.RED,"3) 4x4",Fore.RESET, sep="")
    pos(4,7)
    print(Fore.RED,"4) 5x5",Fore.RESET, sep="")
    pos(4,8)
    print(Fore.RED,"5) Retour",Fore.RESET, sep="")
    pos(4,10)
    result = newInput(1, 5, "Votre choix : ")
    if result == 1:
        jeumorpion(3)
    elif result == 2:
        jeumorpion(3, True)
    elif result == 3:
        jeumorpion(4)
    elif result == 4:
        jeumorpion(5)
    elif result == 5:
        menuMorpion()
    if result != 5:
        modMenu()

def printCircle(x,y):
    x=x*9+4
    y=y*8+3
    for j in range(2):
        for i in range(3):
            pos(2+x+i,1+y+j*4)
            print(Back.BLUE," ",Back.RESET,sep="")
            pos(1+x+j*4,2+y+i)
            print(Back.BLUE," ",Back.RESET,sep="")

def printCross(x,y):
    x=x*9+4
    y=y*8+3
    for i in range(5):
        pos(1+x+i,1+y+i)
        print(Back.RED," ",Back.RESET, sep="")
        pos(5+x-i,1+y+i)
        print(Back.RED," ",Back.RESET, sep="")

def printBoard(size):
    for i in range(size-1):
        for j in range(size*7+2+(size-3)):
            pos(11+i*9,j+3)
            print(Back.GREEN,"  ", sep="")
        for j in range(size*8+1+(size-3)):
            pos(4+j,10+i*8)
            print(Back.GREEN," ", sep="")

def printTerrain(error ,board, size):
    cls()
    printBoard(size)
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 1:
                printCircle(i, j)
            elif board[i][j] == 2:
                printCross(i, j)
    pos(3,29+(size-3)*8)
    print(Fore.RED, error, Style.RESET_ALL, sep="")

def testEnd(size, board, playerTurn, x, y):
    end = 0
    allWrite = True
    for k in range(4):
        testCompletedLine = True
        for i in range(size):
            if k == 0:
                if board[x][i] != playerTurn + 1:
                    testCompletedLine = False
            elif k == 1:
                if board[i][y] != playerTurn + 1:
                    testCompletedLine = False
            elif k == 2:
                if board[i][i] != playerTurn + 1:
                    testCompletedLine = False
            elif k == 3:
                if board[size - 1 - i][i] != playerTurn + 1:
                    testCompletedLine = False
        if testCompletedLine:
            end = 1

    for i in range(size):
        for j in range(size):
            if board[i][j] == 0:
                allWrite = False
    if allWrite:
        end = 2
    return end

def jeumorpion(size, bot=False):
    print("1 contre 1 : morpion")
    error = " "
    playerTurn = randrange(0, 2)
    board = [[0 for i in range(size)] for i in range(size)]
    end = 0
    while end == 0:
        if bot and playerTurn+1 == 2:
            x = randrange(0,3)
            y = randrange(0,3)
        else:
            printTerrain(error, board, size)
            pos(3, 28+(size-3)*8)
            x=newInput(0,size-1,"J"+str(playerTurn+1)+" Choisiser la case pour X (0,1 ou "+str(size-1)+") : ")
            error = ""
            printTerrain(error, board, size)
            pos(3, 28+(size-3)*8)
            y=newInput(0,size-1,"J"+str(playerTurn+1)+" Choisiser la case pour Y (0,1 ou "+str(size-1)+") : ")
        if board[x][y] == 0:
            board[x][y] = playerTurn+1
            end = testEnd(size, board, playerTurn, x, y)
            playerTurn = (playerTurn+1)%2
        else:
            if bot and playerTurn+1 == 1 or not bot:
                error = "Cette case est deja prise"
    printTerrain("", board, size)
    if end == 1:
        pos(3, 28+(size-3)*8)
        print("le gagnant est le joueur"+str(((playerTurn+1)%2)+1))
    elif end == 2:
        pos(3, 28+(size-3)*8)
        print("pas de vainqueur ")
    pos(3, 29+(size-3)*8)
    input("Appuyez sur une touche pour retourner au menu")

def instruction():
    cls()
    print(Fore.YELLOW,"bienvenue dans les instructions")
    pos(5,5)
    print(Fore.GREEN,"Le but du jeu est d’aligner avant son adversaire",Fore.RED," 3 symboles identiques",Fore.GREEN," horizontalement, verticalement ou en diagonale")
    pos(5,6)
    print(Fore.GREEN,"choisissez votre mode de jeu dans le menu")
    pos(6,7)
    print(Fore.GREEN,"1) 3 par 3 | 2 joueurs")
    pos(6,8)
    print(Fore.GREEN,"2) 3 par 3 | jouer contre l'ordinateur")
    pos(6,9)
    print(Fore.GREEN,"3) 4 par 4 | 2 joueurs")
    pos(6,10)
    print(Fore.GREEN,"4) 5 par 5 | 2 joueurs")
    pos(5,12)
    input("Appuyer sur entrer pour retourner au menu")
    return menuMorpion()
