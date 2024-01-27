from Commun import pos,cls,newInput
from colorama import Fore, Back, Style
from random import randrange
from morpion import printTerrain, testEnd

def menuMerelle():
    cls()
    pos(8,2)
    #menu Pricipal
    print("Jeu de Merelles :")
    pos(4,4)
    print(Fore.YELLOW,"1)",Fore.GREEN," Jouer", sep="")
    pos(4,5)
    print(Fore.YELLOW,"2)",Fore.GREEN," Instruction", sep="")
    pos(4,6)
    print(Fore.YELLOW,"3)",Fore.GREEN," Retour au menu principale",Fore.RESET, sep="")
    pos(4,8)
    result = newInput(1,3,"Votre choix : ")
    if result == 2:
        cls()
        pos(8,2)
        print("Bienvenue dans les instruction\n")
        input("Appuyer sur entrer pour revenir au menu")
        menuMerelle()
    elif result == 1:
        modMenu()

def modMenu():
    cls()
    pos(8,2)
    print("Mode de jeu du Merelle :")
    pos(4,4)
    print(Fore.YELLOW,"1)",Fore.GREEN," Normal - 2 Joueur", sep="")
    pos(4,5)
    print(Fore.YELLOW,"2)",Fore.GREEN," Normal - Contre Ordinateur", sep="")
    pos(4,6)
    print(Fore.YELLOW,"3)",Fore.GREEN," Three Mens Morris Variante", sep="")
    pos(4,7)
    print(Fore.YELLOW,"4)",Fore.GREEN," Retour",Fore.RESET, sep="")
    pos(4,9)
    result = newInput(1, 4, "Votre choix : ")
    if result == 1:
        merellesGame()
    if result == 2:
        merellesGame(True)
    elif result == 3:
        ThreeMensMorrisVariante()
    elif result == 4:
        menuMerelle()
    if result != 4:
        modMenu()

def case(x, y, player, selected = False):
    pos(x, y)
    if selected:
        caseColor = Back.GREEN
    else:
        caseColor = Back.WHITE
    print(caseColor, "   ")
    pos(x, y+1)
    if player == 1:
        print(caseColor," ",Back.BLUE,"  ",caseColor," ", sep="")
    elif player == 2:
        print(caseColor, " ", Back.RED, "  ", caseColor, " ", sep="")
    else:
        print(caseColor, " ", Back.BLACK, "  ", caseColor, " ", sep="")
    pos(x, y+2)
    print(caseColor, "   ")
    print(Back.RESET, "")


def printBoard(board, boardTouch, error, x=-1, y=-1, z=-1):
    cls()
    for i in range(2):
        #vertical ligne
        for j in range(31):
            pos(5+i*56,5+j)
            print(Back.YELLOW,"  ", sep="")
        for j in range(21):
            pos(15+i*36,10+j)
            print(Back.YELLOW,"  ", sep="")
        for j in range(11):
            pos(25+i*16,15+j)
            print(Back.YELLOW,"  ", sep="")
        #horizontal ligne
        for j in range(56):
            pos(5+j,5+i*30)
            print(Back.YELLOW,"  ", sep="")
        for j in range(36):
            pos(15+j,10+i*20)
            print(Back.YELLOW,"  ", sep="")
        for j in range(16):
            pos(25+j,15+i*10)
            print(Back.YELLOW,"  ", sep="")
        #passage entre carre
        for j in range(19):
            pos(5+j+i*36,20)
            print(Back.YELLOW,"  ", sep="")
        for j in range(10):
            pos(33,5+j+i*20)
            print(Back.YELLOW,"  ", sep="")
    print(Back.RESET, "")
    pos(75, 11)
    print("Touhce par case :")
    for i in range(3):
        for j in range(3):
            if i != 1 or j != 1:
                if x == j and y == i and z == 0:
                    case(4 + j * 28, 4 + i * 15, board[0][j][i], True)
                else:
                    case(4+j*28,4+i*15,board[0][j][i])
                if x == j and y == i and z == 1:
                    case(14 + j * 18, 9 + i * 10, board[1][j][i], True)
                else:
                    case(14+j*18,9+i*10,board[1][j][i])
                if x == j and y == i and z == 2:
                    case(24 + j * 8, 14 + i * 5, board[2][j][i], True)
                else:
                    case(24+j*8,14+i*5,board[2][j][i])
                for k in range(3):
                    pos(75 + 2 * k + i * (8 - k * 2), 14 + 2 * k + j * (6 - k * 2))
                    print(boardTouch[k][i][j])
    pos(6, 41)
    print(Fore.RED, error, Fore.RESET, sep="")

def selectCase(boardTouch, text, bot, playerTurn,botCase=" "):
    selectNotFound = True
    x, y, z = -1, -1, -1
    if bot and playerTurn==1:
        case = botCase
    else:
        case = input(text)
    if case == "":
        case = " "
    for i in range(3):
        for j in range(3):
            for k in range(3):
                if i != 1 or j != 1:
                    if boardTouch[k][i][j] == case[0].lower():
                        x, y, z = k, i, j
                        selectNotFound = False
    return x,y,z,selectNotFound

def searchEmptyCase(table, value):
    for i in range(len(table)):
        if table[i] == "":
            table[i] = value
            return table
    return table

def getPossibleMove(x,y,z,board,possibleMove):
    if (x == 0 and y == 0 and board[z][x + 1][y] == 0) or (x == 0 and y == 2 and board[z][x + 1][y] == 0) or (x == 1 and y == 0 and board[z][x + 1][y] == 0) or (x == 1 and y == 2 and board[z][x + 1][y] == 0) or ((z == 0 or z == 1) and x == 0 and y == 1 and board[z + 1][x][y] == 0) or ((z == 2 or z == 1) and x == 2 and y == 1 and board[z - 1][x][y] == 0):
        possibleMove = searchEmptyCase(possibleMove, "Move right")
    if (x == 0 and y == 0 and board[z][x][y + 1] == 0) or (x == 2 and y == 0 and board[z][x][y + 1] == 0) or (x == 0 and y == 1 and board[z][x][y + 1] == 0) or (x == 2 and y == 1 and board[z][x][y + 1] == 0) or ((z == 0 or z == 1) and x == 1 and y == 0 and board[z + 1][x][y] == 0) or ((z == 2 or z == 1) and x == 1 and y == 2 and board[z - 1][x][y] == 0):
        possibleMove = searchEmptyCase(possibleMove, "Move bottom")
    if (x == 2 and y == 0 and board[z][x - 1][y] == 0) or (x == 2 and y == 2 and board[z][x - 1][y] == 0) or (x == 1 and y == 0 and board[z][x - 1][y] == 0) or (x == 1 and y == 2 and board[z][x - 1][y] == 0) or ((z == 2 or z == 1) and x == 0 and y == 1 and board[z - 1][x][y] == 0) or ((z == 0 or z == 1) and x == 2 and y == 1 and board[z + 1][x][y] == 0):
        possibleMove = searchEmptyCase(possibleMove, "Move left")
    if (x == 0 and y == 2 and board[z][x][y - 1] == 0) or (x == 2 and y == 2 and board[z][x][y - 1] == 0) or (x == 0 and y == 1 and board[z][x][y - 1] == 0) or (x == 2 and y == 1 and board[z][x][y - 1] == 0) or ((z == 2 or z == 1) and x == 1 and y == 0 and board[z - 1][x][y] == 0) or ((z == 0 or z == 1) and x == 1 and y == 2 and board[z + 1][x][y] == 0):
        possibleMove = searchEmptyCase(possibleMove, "Move up")
    return possibleMove

def botGetKey():
    key = ["a","z","e","q","d","w","x","c","r","t","y","f","h","v","b","n","7","8","9","4","6","1","2","3"]
    index = randrange(0,len(key))
    return key[index]

def detectMoulin(board, x, y, z, playerTurn, boardTouch, bot, selection, pieces):
    error = ""
    ligneOfThree = False
    for i in range(2):
        testLigneOfThree = True
        for j in range(3):
            if i == 0:
                if x != 1:
                    if board[z][x][j] != playerTurn + 1:
                        testLigneOfThree = False
                else:
                    if board[j][x][y] != playerTurn + 1:
                        testLigneOfThree = False
            if i == 1:
                if y != 1:
                    if board[z][j][y] != playerTurn + 1:
                        testLigneOfThree = False
                else:
                    if board[j][x][y] != playerTurn + 1:
                        testLigneOfThree = False

        if testLigneOfThree:
            ligneOfThree = True

    if ligneOfThree:
        notDeleted = True
        while notDeleted:
            if bot and playerTurn == 1:
                delZ, delX, delY, touchNotFind = selectCase(boardTouch, "", bot, playerTurn, botGetKey())
            else:
                printBoard(board, boardTouch, error)
                pos(6, 40)
                delZ, delX, delY, touchNotFind = selectCase(boardTouch, "J" + str(
                    playerTurn + 1) + " Selectioner un pion adverse a suprimer : ", bot, playerTurn)
            if touchNotFind:
                error = "La touche n'est pas assigner"
            else:
                if board[delZ][delX][delY] != ((playerTurn + 1) % 2) + 1:
                    error = "Vous devez selectionner un pion adverse"
                else:
                    board[delZ][delX][delY] = 0
                    notDeleted = False
                    error = ""
                    playerTurn = (playerTurn + 1) % 2
                    pieces[playerTurn] -= 1
    elif selection != 0:
        playerTurn = (playerTurn + 1) % 2
    return playerTurn

def merellesGame(bot=False):
    board = [[[0 for i in range(3)] for i in range(3)] for i in range(3)] #-------------------------------------------------
    boardTouch = [[["a", "q", "w"], ["z", "null", "x"], ["e", "d", "c"]],[["r", "f", "v"], ["t", "null", "b"], ["y", "h", "n"]],[["7", "4", "1"], ["8", "null", "2"], ["9", "6", "3"]]]

    error = ""
    playerTurn = randrange(0, 2)
    pieces = [0, 0]
    winner = -1

    step = 1
    while step == 1:
        if bot and playerTurn==1:
            x,y,z,touchNotFind = selectCase(boardTouch,"",bot,playerTurn,botGetKey())
        else:
            printBoard(board, boardTouch, error)
            error = ""
            pos(6, 40)
            x, y, z, touchNotFind = selectCase(boardTouch, "J" + str(playerTurn + 1) + " Selectionner la case ou poser votre pion (voir tableau droite) : ",bot,playerTurn)
        if touchNotFind:
            error = "La touche n'est pas assigner"
        else:
            if board[x][y][z] == 0:
                board[x][y][z] = playerTurn + 1
                pieces[playerTurn] += 1
                playerTurn = (playerTurn + 1) % 2
            else:
                touchNotFind = True
                error = "Cette case est deja utiliser"
        if pieces[0] >= 9 and pieces[1] >= 9:
            step = 2
        if bot and playerTurn == 1:
            error = ""
    while step == 2:
        if bot and playerTurn==1:
            z, x, y, touchNotFind = selectCase(boardTouch, "", bot,playerTurn, botGetKey())
        else:
            printBoard(board, boardTouch, error)
            error = ""
            # selection pion a bouger
            pos(6, 40)
            z, x, y, touchNotFind = selectCase(boardTouch, "J" + str(playerTurn + 1) + " Selectioner un pion a bouger : ",bot,playerTurn)

        if board[z][x][y] == playerTurn + 1:
            selection = 0
            if pieces[playerTurn] > 3:
                possibleMove = ["Deselectionner le pion", "", "", "", ""]
                possibleMove = getPossibleMove(x, y, z, board, possibleMove)
                maxRep = -1
                lastX, lastY, lastZ = x, y, z
                if bot and playerTurn == 1:
                    for i in range(len(possibleMove)):
                        if possibleMove[i] != "":
                            maxRep+=1
                    selection = randrange(0, maxRep+1)
                else:
                    printBoard(board, boardTouch, error, x, y, z)
                    for i in range(len(possibleMove)):
                        if possibleMove[i] != "":
                            maxRep += 1
                            pos(6, 40 + i)
                            print(i, ") ", possibleMove[i], sep="")

                    # mouvement du pion selectionner
                    pos(6, 46)
                    selection = newInput(0, maxRep,"J" + str(playerTurn + 1) + " Selectioner un chois (de 0 a " + str(maxRep) + "): ")
                if x != 1 and y != 1:
                    if possibleMove[selection] == "Move right":
                        board[z][x + 1][y] = playerTurn + 1
                        x += 1
                    elif possibleMove[selection] == "Move bottom":
                        board[z][x][y + 1] = playerTurn + 1
                        y += 1
                    elif possibleMove[selection] == "Move left":
                        board[z][x - 1][y] = playerTurn + 1
                        x -= 1
                    elif possibleMove[selection] == "Move up":
                        board[z][x][y - 1] = playerTurn + 1
                        y -= 1
                else:
                    if possibleMove[selection] == "Move right":
                        if ((z == 0 or z == 1) and x == 0 and y == 1):
                            board[z + 1][x][y] = playerTurn + 1
                            z += 1
                        elif ((z == 2 or z == 1) and x == 2 and y == 1):
                            board[z - 1][x][y] = playerTurn + 1
                            z -= 1
                        elif (x == 1 and y == 0) or (x == 1 and y == 2):
                            board[z][x + 1][y] = playerTurn + 1
                            x += 1
                    elif possibleMove[selection] == "Move bottom":
                        if ((z == 0 or z == 1) and x == 1 and y == 0):
                            board[z + 1][x][y] = playerTurn + 1
                            z += 1
                        elif ((z == 2 or z == 1) and x == 1 and y == 2):
                            board[z - 1][x][y] = playerTurn + 1
                            z -= 1
                        elif (x == 0 and y == 1) or (x == 2 and y == 1):
                            board[z][x][y + 1] = playerTurn + 1
                            y += 1
                    elif possibleMove[selection] == "Move left":
                        if ((z == 0 or z == 1) and x == 2 and y == 1):
                            board[z + 1][x][y] = playerTurn + 1
                            z += 1
                        elif ((z == 2 or z == 1) and x == 0 and y == 1):
                            board[z - 1][x][y] = playerTurn + 1
                            z -= 1
                        elif (x == 1 and y == 0) or (x == 1 and y == 2):
                            board[z][x - 1][y] = playerTurn + 1
                            x -= 1
                    elif possibleMove[selection] == "Move up":
                        if ((z == 0 or z == 1) and x == 1 and y == 2):
                            board[z + 1][x][y] = playerTurn + 1
                            z += 1
                        elif ((z == 2 or z == 1) and x == 1 and y == 0):
                            board[z - 1][x][y] = playerTurn + 1
                            z -= 1
                        elif (x == 0 and y == 1) or (x == 2 and y == 1):
                            board[z][x][y - 1] = playerTurn + 1
                            y -= 1

                if selection != 0:
                    board[lastZ][lastX][lastY] = 0
                    playerTurn = detectMoulin(board, x, y, z, playerTurn, boardTouch, bot, selection, pieces)
            else:
                # Si le joeur na que trois piece
                if bot and playerTurn==1:
                    newZ, newX, newY, touchNotFind = selectCase(boardTouch, "", bot,playerTurn, botGetKey())
                else:
                    printBoard(board, boardTouch, error, x, y, z)
                    newZ, newX, newY, touchNotFind = selectCase(boardTouch, "J" + str(playerTurn + 1) + " Selectionner la case ou le deplacer (\"" + boardTouch[z][x][y] + "\" pour le deselectionner) : ",bot,playerTurn)
                if newZ == z and newX == x and newY == y:
                    print("deselectionner")
                else:
                    if board[newZ][newX][newY] == 0:
                        board[z][x][y] = 0
                        board[newZ][newX][newY] = playerTurn + 1
                        selection = 1
                        playerTurn = detectMoulin(board, newX, newY, newZ, playerTurn, boardTouch, bot, selection, pieces)
                    else:
                        error = "Vous devez selectionner une case vide"


        else:
            error = "Vous devez selectionner un de vos pions"
            print("error")

        # test fin partie
        if pieces[0] < 3:
            step = 3
            winner = 0
            error = ""
        elif pieces[1] < 3:
            step = 3
            winner = 1
            error = ""

        haveAnyMove = True
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    if board[k][j][i] == playerTurn + 1:
                        possibleMove = ["null", "", "", "", ""]
                        possibleMove = getPossibleMove(j, i, k, board, possibleMove)
                        if possibleMove[1] != "":
                            haveAnyMove = False
        if haveAnyMove:
            step = 3
            winner = ((playerTurn + 1) % 2) + 1
            error = "(le J" + str(playerTurn + 1) + " ne peut deplacer aucun pion)"
        if bot and playerTurn == 1:
            error = ""

    cls()
    pos(40, 20)
    print("Le gagnant est J", winner, sep="")
    pos(33, 22)
    print(error)
    pos(30, 26)
    input("Appuyer sur entrer pour retourner au menu")


#Variante : Three Mens Morris
def rectSelection(x,y):
    x=x*9+4
    y=y*8+3
    for i in range(2):
        for j in range(7):
            pos(x+j,y+i*6)
            print(Back.WHITE," ",Back.RESET,sep="")
        for j in range(7):
            pos(x+i*6,y+j)
            print(Back.WHITE, " ", Back.RESET, sep="")

def getPos(error, board, playerTurn,etape):
    printTerrain(error, board, 3)
    pos(6,27)
    print(etape)
    pos(3,30)
    print(Fore.RED, error, Style.RESET_ALL, sep="")
    pos(3, 29)
    x = newInput(0, 2, "J" + str(playerTurn + 1) +" Choisiser la case pour X (0 a 2) : ")
    error = ""
    printTerrain(error, board, 3)
    pos(6,27)
    print(etape)
    pos(3, 29)
    y = newInput(0, 2, "J" + str(playerTurn + 1) +" Choisiser la case pour Y (0 a 2) : ")
    return x,y

def ThreeMensMorrisVariante():
    board = [[0 for i in range(3)] for i in range(3)]
    playerTurn = randrange(2)
    pieces = [0,0]

    error = ""
    step = 1
    while step == 1:
        x, y = getPos(error, board, playerTurn,"Etape : Pose de pion")
        if board[x][y] == 0:
            board[x][y] = playerTurn + 1
            pieces[playerTurn]+=1
            playerTurn = (playerTurn+1)%2
        else:
            error = "Veuillez selectionner une case vide"
        if pieces[0] == pieces[1] == 3:
            step = 2
    while step == 2:
        cls()
        x, y = getPos(error, board, playerTurn,"Etape : Deplacement des pions")
        if board[x][y] == playerTurn+1:
            possibleMove = ["Deselectionner le pion","","","",""]
            if x!=2 and board[x+1][y] == 0:
                possibleMove = searchEmptyCase(possibleMove, "Move right")
            if x!=0 and board[x-1][y] == 0:
                possibleMove = searchEmptyCase(possibleMove, "Move left")
            if y!=2 and board[x][y+1] == 0:
                possibleMove = searchEmptyCase(possibleMove, "Move down")
            if y!=0 and board[x][y-1] == 0:
                possibleMove = searchEmptyCase(possibleMove, "Move up")

            printTerrain(error, board, 3)
            rectSelection(x, y)
            maxRep = -1
            for i in range(len(possibleMove)):
                if possibleMove[i] != "":
                    maxRep += 1
                    pos(6, 40 + i)
                    print(i, ") ", possibleMove[i], sep="")

            # mouvement du pion selectionner
            pos(6, 46)
            lastX, lastY = x, y
            selection = newInput(0, maxRep,"J" + str(playerTurn + 1) + " Selectioner un chois (de 0 a " + str(maxRep) + "): ")
            if possibleMove[selection] == "Move right":
                board[x+1][y] = playerTurn+1
                x+=1
            if possibleMove[selection] == "Move left":
                board[x-1][y] = playerTurn+1
                x-=1
            if possibleMove[selection] == "Move down":
                board[x][y+1] = playerTurn+1
                y+=1
            if possibleMove[selection] == "Move up":
                board[x][y-1] = playerTurn+1
                y-=1

            if selection != 0:
                board[lastX][lastY] = 0
                end = testEnd(3, board, playerTurn, x, y)
                playerTurn = (playerTurn+1)%2
                if end == 1:
                    step = 3

        else:
            error = "Veuillez selectionner un de vos pion"

    printTerrain(error, board, 3)
    pos(3, 28)
    print("le gagnant est le joueur" + str(((playerTurn + 1) % 2) + 1))
    pos(3, 30)
    input("Appuis sur entrer pour retourner au menu")