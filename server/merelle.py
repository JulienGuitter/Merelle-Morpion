

def testCase(boardTouch, data):
    selectNotFound = True
    x, y, z = -1, -1, -1
    for i in range(3):
        for j in range(3):
            for k in range(3):
                if i != 1 or j != 1:
                    if boardTouch[k][i][j] == data[0].lower():
                        z, x, y = k, i, j
                        selectNotFound = False
    return z,x,y,selectNotFound

def sendBoard(board, client):
    for k in range(3):
        for i in range(3):
            for j in range(3):
                dataToSend = str(board[k][i][j])
                client.send(dataToSend.encode())
    client.send(b"e")

def searchEmptyCase(table, value):
    for i in range(len(table)):
        if table[i] == "":
            table[i] = value
            return table
    return table

def getPossibleMove(x,y,z,board,possibleMove):
    if (x == 0 and y == 0 and board[z][x + 1][y] == 0) or (x == 0 and y == 2 and board[z][x + 1][y] == 0) or (x == 1 and y == 0 and board[z][x + 1][y] == 0) or (x == 1 and y == 2 and board[z][x + 1][y] == 0) or ((z == 0 or z == 1) and x == 0 and y == 1 and board[z + 1][x][y] == 0) or ((z == 2 or z == 1) and x == 2 and y == 1 and board[z - 1][x][y] == 0):
        possibleMove = searchEmptyCase(possibleMove, "r")
    if (x == 0 and y == 0 and board[z][x][y + 1] == 0) or (x == 2 and y == 0 and board[z][x][y + 1] == 0) or (x == 0 and y == 1 and board[z][x][y + 1] == 0) or (x == 2 and y == 1 and board[z][x][y + 1] == 0) or ((z == 0 or z == 1) and x == 1 and y == 0 and board[z + 1][x][y] == 0) or ((z == 2 or z == 1) and x == 1 and y == 2 and board[z - 1][x][y] == 0):
        possibleMove = searchEmptyCase(possibleMove, "b")
    if (x == 2 and y == 0 and board[z][x - 1][y] == 0) or (x == 2 and y == 2 and board[z][x - 1][y] == 0) or (x == 1 and y == 0 and board[z][x - 1][y] == 0) or (x == 1 and y == 2 and board[z][x - 1][y] == 0) or ((z == 2 or z == 1) and x == 0 and y == 1 and board[z - 1][x][y] == 0) or ((z == 0 or z == 1) and x == 2 and y == 1 and board[z + 1][x][y] == 0):
        possibleMove = searchEmptyCase(possibleMove, "l")
    if (x == 0 and y == 2 and board[z][x][y - 1] == 0) or (x == 2 and y == 2 and board[z][x][y - 1] == 0) or (x == 0 and y == 1 and board[z][x][y - 1] == 0) or (x == 2 and y == 1 and board[z][x][y - 1] == 0) or ((z == 2 or z == 1) and x == 1 and y == 0 and board[z - 1][x][y] == 0) or ((z == 0 or z == 1) and x == 1 and y == 2 and board[z + 1][x][y] == 0):
        possibleMove = searchEmptyCase(possibleMove, "u")
    return possibleMove

def detectMoulin(client, board, x, y, z, playerTurn, boardTouch, pieces):
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
        client.send(b"de")
        sendBoard(board, client)
        while notDeleted:
            deletedData = client.recv(1024).decode()
            delZ, delX, delY, touchNotFind = testCase(boardTouch, deletedData)
            if touchNotFind:
                client.send(b"as")
            else:
                if board[delZ][delX][delY] != ((playerTurn + 1) % 2) + 1:
                    client.send(b"ad")
                else:
                    board[delZ][delX][delY] = 0
                    notDeleted = False
                    error = ""
                    playerTurn = (playerTurn + 1) % 2
                    pieces[playerTurn] -= 1
                    client.send(b"ok")
    else:
        client.send(b"no")
        playerTurn = (playerTurn + 1) % 2
    return playerTurn

def testCanMove(pieces, board, playerTurn):
    step = 2
    winner = -1
    error = "0"
    if pieces[0] < 3:
        step = 3
        winner = 0
        error = "0"
    elif pieces[1] < 3:
        step = 3
        winner = 1
        error = "0"

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
        error = "1"

    return step, winner, error

def merelleTestPos(client, gameData, data, party):
    board = gameData["board"]
    playerTurn = gameData["turn"]
    pieces = gameData["pieces"]
    boardTouch = [[["a", "q", "w"], ["z", "null", "x"], ["e", "d", "c"]],[["r", "f", "v"], ["t", "null", "b"], ["y", "h", "n"]],[["7", "4", "1"], ["8", "null", "2"], ["9", "6", "3"]]]

    if (playerTurn == 0 and gameData["player1"] == client) or (playerTurn == 1 and gameData["player2"] == client):
        if gameData["step"] == 1:
            z, x, y, touchNotFind = testCase(boardTouch, data)
            if touchNotFind:
                client.send(b"ass")
            else:
                if board[z][x][y] == 0:
                    board[z][x][y] = playerTurn + 1
                    pieces[playerTurn] += 1
                    gameData["turn"] = (playerTurn + 1) % 2
                    client.send(b"ok")
                    if pieces[0] >= 9 and pieces[1] >= 9:
                        gameData["step"] = 2
                    gameData["player1"].send(str(gameData["step"]).encode())
                    gameData["player2"].send(str(gameData["step"]).encode())
                    sendBoard(board, gameData["player1"])
                    sendBoard(board, gameData["player2"])
                else:
                    client.send(b"use")
        elif gameData["step"] == 2:
            z, x, y, touchNotFind = testCase(boardTouch, data)

            if touchNotFind:
                client.send(b"ass")
            else:
                if board[z][x][y] == playerTurn + 1:
                    client.send(b"ok")
                    possibleMove = ["d", "", "", "", ""]
                    if pieces[playerTurn] > 3:
                        client.send(b"no")
                        selection = 0
                        lastX, lastY, lastZ = x, y, z
                        while selection == 0:

                            possibleMove = ["d", "", "", "", ""]
                            possibleMove = getPossibleMove(x, y, z, board, possibleMove)
                            maxRep = -1
                            lastX, lastY, lastZ = x, y, z
                            for i in range(len(possibleMove)):
                                if possibleMove[i] != "":
                                    maxRep += 1
                                    client.send(possibleMove[i].encode())
                            client.send(b"e")
                            selection = int(client.recv(1024).decode())

                            if selection == 0:
                                toucheFind = False
                                while not toucheFind:
                                    data = client.recv(1024).decode()
                                    print("data : "+data)
                                    z, x, y, touchNotFind = testCase(boardTouch, data)
                                    if touchNotFind:
                                        client.send(b"ass")
                                    else:
                                        if board[z][x][y] == playerTurn + 1:
                                            toucheFind = True
                                            client.send(b"ok")
                                        else:
                                            client.send(b"me")
                            else:
                                client.send(b"moved")
                        if x != 1 and y != 1:
                            if possibleMove[selection] == "r":
                                board[z][x + 1][y] = playerTurn + 1
                                x += 1
                            elif possibleMove[selection] == "b":
                                board[z][x][y + 1] = playerTurn + 1
                                y += 1
                            elif possibleMove[selection] == "l":
                                board[z][x - 1][y] = playerTurn + 1
                                x -= 1
                            elif possibleMove[selection] == "u":
                                board[z][x][y - 1] = playerTurn + 1
                                y -= 1
                        else:
                            if possibleMove[selection] == "r":
                                if ((z == 0 or z == 1) and x == 0 and y == 1):
                                    board[z + 1][x][y] = playerTurn + 1
                                    z += 1
                                elif ((z == 2 or z == 1) and x == 2 and y == 1):
                                    board[z - 1][x][y] = playerTurn + 1
                                    z -= 1
                                elif (x == 1 and y == 0) or (x == 1 and y == 2):
                                    board[z][x + 1][y] = playerTurn + 1
                                    x += 1
                            elif possibleMove[selection] == "b":
                                if ((z == 0 or z == 1) and x == 1 and y == 0):
                                    board[z + 1][x][y] = playerTurn + 1
                                    z += 1
                                elif ((z == 2 or z == 1) and x == 1 and y == 2):
                                    board[z - 1][x][y] = playerTurn + 1
                                    z -= 1
                                elif (x == 0 and y == 1) or (x == 2 and y == 1):
                                    board[z][x][y + 1] = playerTurn + 1
                                    y += 1
                            elif possibleMove[selection] == "l":
                                if ((z == 0 or z == 1) and x == 2 and y == 1):
                                    board[z + 1][x][y] = playerTurn + 1
                                    z += 1
                                elif ((z == 2 or z == 1) and x == 0 and y == 1):
                                    board[z - 1][x][y] = playerTurn + 1
                                    z -= 1
                                elif (x == 1 and y == 0) or (x == 1 and y == 2):
                                    board[z][x - 1][y] = playerTurn + 1
                                    x -= 1
                            elif possibleMove[selection] == "u":
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
                            gameData["turn"] = detectMoulin(client, board, x, y, z, playerTurn, boardTouch, pieces)
                    else:


                        client.send(b"yes")
                        movedPiece = False
                        while not movedPiece:
                            data = client.recv(1024).decode()
                            newZ, newX, newY, touchNotFind = testCase(boardTouch, data)
                            if newZ == z and newX == x and newY == y:
                                client.send(b"de")
                            else:
                                if board[newZ][newX][newY] == 0:
                                    movedPiece = True
                                    client.send(b"ok")
                                    board[z][x][y] = 0
                                    board[newZ][newX][newY] = playerTurn + 1
                                    gameData["turn"] = detectMoulin(client, board, newX, newY, newZ, playerTurn, boardTouch, pieces)
                                else:
                                    client.send(b"vi")

                    step, winner, end = testCanMove(pieces, board, playerTurn) # a revoire

                    gameData["player1"].send(str(gameData["step"]).encode())
                    gameData["player2"].send(str(gameData["step"]).encode())
                    sendBoard(board, gameData["player1"])
                    sendBoard(board, gameData["player2"])
                else:
                    client.send(b"me")
            if pieces[0] == 2:
                gameData["player1"].send(b"l")
                gameData["player2"].send(b"w")
            elif pieces[1] == 2:
                gameData["player1"].send(b"w")
                gameData["player2"].send(b"l")
            else:
                gameData["player1"].send(b"p")
                gameData["player2"].send(b"p")



