
def testEnd(size, board, playerTurn, x, y):
    end = 0
    allWrite = True
    for k in range(4):
        testCompletedLine = True
        for i in range(int(size)):
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
                if board[int(size) - 1 - i][i] != playerTurn + 1:
                    testCompletedLine = False
        if testCompletedLine:
            end = 1

    for i in range(int(size)):
        for j in range(int(size)):
            if board[i][j] == 0:
                allWrite = False
    if allWrite:
        end = 2
    return end

def sendBoard(board, client, size):
    for i in range(int(size)):
        for j in range(int(size)):
            dataToSend = str(board[i][j])
            client.send(dataToSend.encode())
    client.send(b"e")

def removeGame(gameData, party):
    party.remove(gameData)

def morpionTestPos(client, gameData, data, party):
    x = int(data[0])
    y = int(data[1])
    board = gameData["board"]
    playerTurn = gameData["turn"]
    size = gameData["size"]

    if (playerTurn == 0 and gameData["player1"] == client) or (playerTurn == 1 and gameData["player2"] == client):
        if board[x][y] == 0:
            board[x][y] = playerTurn + 1
            end = testEnd(size, board, playerTurn, x, y)
            gameData["turn"] = (playerTurn + 1) % 2
            if end == 0:
                client.send(b"ok")
                sendBoard(board, gameData["player1"], size)
                sendBoard(board, gameData["player2"], size)
            elif end == 1:
                if playerTurn == 0:
                    gameData["player1"].send(b"w")
                    gameData["player2"].send(b"l")
                elif playerTurn == 1:
                    gameData["player1"].send(b"l")
                    gameData["player2"].send(b"w")
                removeGame(gameData, party)
            elif end == 2:
                gameData["player1"].send(b"execo")
                gameData["player2"].send(b"execo")
                removeGame(gameData, party)

        else:
            client.send(b"error")
    else:
        client.send(b"notYourTurn")