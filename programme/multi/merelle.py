from colorama import Fore, Back, Style
from Commun import pos, cls


def case(x, y, player, selected = False):
    pos(x,y)
    if selected:
        caseColor = Back.GREEN
    else:
        caseColor = Back.WHITE
    print(caseColor,"   ")
    pos(x, y+1)
    if player == "1":
        print(caseColor," ",Back.BLUE,"  ",caseColor," ", sep="")
    elif player == "2":
        print(caseColor, " ", Back.RED, "  ", caseColor, " ", sep="")
    else:
        print(caseColor, " ", Back.BLACK, "  ", caseColor, " ", sep="")
    pos(x, y+2)
    print(caseColor,"   ")
    print(Back.RESET, "")

def newInput(min, max, question):
    while True:
        try:
            x=int(input(question))
            if x >= min and x <= max:
                break
            else:
                print("Vous devez entre un nombre entre",min,"et",max,".")
        except ValueError:
            print("Entre un nombre entier")
    return x

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
    print("Touche par case :")
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

def selectCase(server, board, boardTouch):
    caseVide = False
    while not caseVide:
        case = input("Selectionner la case ou poser votre pion (voir tableau droite) : ")
        if case == "":
            case = " "
        server.send(case.encode())
        data = server.recv(1024).decode()
        if data == "ok":
            caseVide = True
        elif data == "use":
            printBoard(board, boardTouch, "Cette case est deja utiliser")
        elif data == "ass":
            printBoard(board, boardTouch, "La touche n'est pas assigner")
        else:
            testEndGameMessage(data)
    getStep = server.recv(1024).decode()
    board, end = getBoard(server, board, getStep != "", getStep[1:])
    return board

def getBoard(server, board, alrady=False, data=""):
    if not alrady:
        data = server.recv(1024).decode()
        while data[-2:-1] != "e":
            print(data)
            data += server.recv(1024).decode()
    itemPos = 0
    end = data[-1:]
    for k in range(3):
        for i in range(3):
            for j in range(3):
                board[k][i][j] = data[itemPos]
                itemPos += 1
    return board, end

def StepTwo(server, board, boardTouch):
    caseVide = False
    piecePos=""
    while not caseVide:
        case = input("Selectioner un pion a bouger : ")
        if case == "":
            case = " "
        server.send(case.encode())
        data = server.recv(1024).decode()
        if data == "ok":
            threePiece = server.recv(1024).decode()
            if threePiece[:2] == "no":
                movingPieces = False
                while not movingPieces:
                    movePiece = ""
                    moveData = ""
                    while movePiece != "moved":
                        if threePiece[-1:] != "e":
                            if moveData[-1:] != "e":
                                moveData = server.recv(1024).decode()
                            while moveData[-1:] != "e":
                                moveData += server.recv(1024).decode()
                        else:
                            moveData = threePiece[2:]
                        possibleMove = []
                        possibleMove[:0] = moveData
                        printBoard(board, boardTouch, "")
                        for i in range(len(possibleMove)-1):
                            text = ""
                            pos(6, 40 + i)
                            if possibleMove[i] == "d":
                                text = "Deselectioner"
                            elif possibleMove[i] == "r":
                                text = "Move Right"
                            elif possibleMove[i] == "b":
                                text = "Move bottom"
                            elif possibleMove[i] == "l":
                                text = "Move left"
                            elif possibleMove[i] == "u":
                                text = "Move Up"
                            print(i, ") ", text, sep="")
                        pos(6, 46)
                        selection = newInput(0, len(possibleMove)-2, "Selectioner un chois (de 0 a " + str(len(possibleMove)-2) + "): ")
                        server.send(str(selection).encode())
                        if selection == 0:
                            selectOtherPiece = False
                            error = ""
                            while not selectOtherPiece:
                                printBoard(board, boardTouch, error)
                                error = ""
                                case = input("Selectioner un pion a bouger : ")
                                if case == "":
                                    case = " "
                                server.send(case.encode())
                                data = server.recv(1024).decode()
                                if data[:2] == "ok":
                                    if data == "ok":
                                        moveData = ""
                                    else:
                                        moveData = data[2:]
                                    selectOtherPiece = True
                                    printBoard(board, boardTouch, "")
                                elif data[:2] == "me":
                                    error = "Vous devez selectionner un de vos pions"
                                elif data[:3] == "ass":
                                    error = "La touche n'est pas assigner"
                                else:
                                    testEndGameMessage(data)
                        else:
                            movePiece = server.recv(1024).decode()

                    getDelData = server.recv(1024).decode()
                    delPiece = getDelData[:2]
                    if delPiece == "de":
                        piecePos = getDelData[2:]
                    else:
                        piecePos = getDelData[3:]
                    deletedPiece = False
                    if delPiece == "de":
                        board, end = getBoard(server, board, piecePos != "", piecePos)
                        printBoard(board, boardTouch, "")
                        while not deletedPiece:
                            printBoard(board, boardTouch, "")
                            pos(6, 40)
                            case = input("Selectioner un pion adverse a suprimer : ")
                            server.send(case.encode())
                            deletedData = server.recv(1024).decode()
                            if deletedData == "ok":
                                deletedPiece = True
                                getBoardData = server.recv(1024).decode()
                                piecePos = getBoardData[1:]
                            elif deletedData == "ad":
                                printBoard(board, boardTouch, "Vous devez selectionner un pion adverse")
                            elif deletedData == "as":
                                printBoard(board, boardTouch, "La touche n'est pas assigner")
                            else:
                                testEndGameMessage(deletedData)
                    if delPiece == "no" or deletedPiece:
                        movingPieces = True
            else:
                movedPiece = False
                while not movedPiece:
                    case = input("Selectionner la case ou le deplacer : ")
                    if case == "":
                        case = " "
                    server.send(case.encode())
                    newData = server.recv(1024).decode()
                    if newData == "vi":
                        printBoard(board, boardTouch, "Vous devez selectionner une case vide")
                    elif newData == "de":
                        print("deselectionner")
                    elif newData == "ok":
                        movedPiece = True
                        getBoardData = server.recv(1024).decode()
                        if getBoardData[:2] == "de":
                            piecePos = getBoardData[2:]
                        else:
                            piecePos = getBoardData[3:]
                        delPiece = getBoardData[:2]
                        deletedPiece = False
                        if delPiece == "de":
                            board, end = getBoard(server, board, piecePos != "", piecePos)
                            printBoard(board, boardTouch, "")
                            while not deletedPiece:
                                printBoard(board, boardTouch, "")
                                pos(6, 40)
                                case = input("Selectioner un pion adverse a suprimer : ")
                                server.send(case.encode())
                                deletedData = server.recv(1024).decode()
                                if deletedData == "ok":
                                    deletedPiece = True
                                    getBoardData = server.recv(1024).decode()
                                    piecePos = getBoardData[1:]
                                elif deletedData == "ad":
                                    printBoard(board, boardTouch, "Vous devez selectionner un pion adverse")
                                elif deletedData == "as":
                                    printBoard(board, boardTouch, "La touche n'est pas assigner")
                                else:
                                    testEndGameMessage(deletedData)
                        else:
                            testEndGameMessage(newData)
                    else:
                        testEndGameMessage(newData)
            caseVide = True
        elif data == "me":
            printBoard(board, boardTouch, "Vous devez selectionner un de vos pions")
        elif data == "ass":
            printBoard(board, boardTouch, "La touche n'est pas assigner")
        else:
            testEndGameMessage(data)
    board, end = getBoard(server, board, piecePos != "", piecePos)
    testEndGameMessage(end)
    return board

# ------------------------------------------------------------ pas encore utiliser --------------------------------------------
def testEndGameMessage(validationPos):
    if validationPos == "l":
        print("vous avez perdu")
    elif validationPos == "w":
        print("vous avez gagner")
    elif validationPos == "ze":
        print("Le joueur adverse c'est deconnecter")
    if validationPos == "l" or validationPos == "w" or validationPos == "ze":
        input("appuyer sur entrer pour retourner au menu")
        menuPrincipale()


def mainMerelle(firstPlayer, server):
    board = [[[0 for i in range(3)] for i in range(3)] for i in range(3)]
    boardTouch = [[["a", "q", "w"], ["z", "null", "x"], ["e", "d", "c"]],[["r", "f", "v"], ["t", "null", "b"], ["y", "h", "n"]],[["7", "4", "1"], ["8", "null", "2"], ["9", "6", "3"]]]

    printBoard(board, boardTouch, "")
    if firstPlayer == "youStart":
        board = selectCase(server, board, boardTouch)
        printBoard(board, boardTouch, "")
    while True:
        printBoard(board, boardTouch, "")
        print("en attente du joueur adverse ...")
        step = server.recv(1024).decode()
        testEndGameMessage(step)
        board, end = getBoard(server, board)
        testEndGameMessage(end)
        printBoard(board, boardTouch, "")
        if step == "1":
            board = selectCase(server, board, boardTouch)
        elif step == "2":
            board = StepTwo(server, board, boardTouch)
            printBoard(board, boardTouch, "")