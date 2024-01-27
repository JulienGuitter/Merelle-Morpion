from tkinter import *

def menuMorpion(window, frame):
    frame.destroy()
    board = [[0 for i in range(3)]for j in range(3)]
    playerTurn = [0]
    #board = [[[0,1,2],[1,0,2],[0,2,1]]]


    #frameUn
    frame = Frame(window,bg='#A6E7CD')
    frame.pack(expand=YES)

    #texte
    bienvenu = Label(frame, text="jeu de morpion",font=("arial", 40), bg='#A6E7CD')
    bienvenu.pack(expand=YES)
    #boutton
    jouerAuMorpion = Button(frame, text="réinitialiser", font=("arial",25),bg='#A6E7CD')
    jouerAuMorpion.pack()
    #plateau
    plateau = Canvas(window, width = 400, height = 400)
    plateau.create_line(20,133,380,133,fill = '#090A09',width= 5) #horizontale
    plateau.create_line(20,266,380,266,fill = '#090A09',width=5) #horizontale
    plateau.create_line(133,20,133,380,fill = '#090A09', width= 5) #
    plateau.create_line(266,20,266,380,fill= '#090A09', width = 5)
    for i in range(3):
        for j in range(3):
            if board [i][j] ==1:
                rond(65+ i*133,65+j*133 ,plateau)
            elif board[i][j] == 2:
                tracer_croix(65+ i*133,65+j*133,plateau)


    plateau.pack()
    window.bind("<Button>", lambda event, arg=board, arg2= playerTurn, arg3=plateau, arg4 = frame, arg5=window: clic(event, arg, arg2, arg3, arg4, arg5))


#rond
def rond(x, y,plateau):
    plateau.create_oval(x - 35, y - 35, x + 35, y + 35, fill = "#E61818")
#croix
def tracer_croix(x, y,plateau):
    plateau.create_line(x-35, y-35, x+35, y+35, width = 5, fill = "#1C3EE1")
    plateau.create_line(x-35, y+35, x+35, y-35, width = 5, fill = "#1C3EE1")

def testEnd(size, board, playerTurn, x, y):
    end = 0
    allWrite = True
    for k in range(4):
        testCompletedLine = True
        for i in range(size):
            if k == 0:
                if board[x][i] != playerTurn+1:
                    testCompletedLine = False
            elif k == 1:
                if board[i][y] != playerTurn+1:
                    testCompletedLine = False
            elif k == 2:
                if board[i][i] != playerTurn+1:
                    testCompletedLine = False
            elif k == 3:
                if board[size - 1 - i][i] != playerTurn+1:
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

def clic(event, board, playerTurn, plateau, frame, window):
    x = event.x
    y = event.y
    end=0
    for j in range(3):
        for i in range(3):
            if x >= 20+i*116 and x <= 130+i*116 and y >= 20+j*116 and y <= 130+j*116:
                if board[i][j] == 0:
                    if playerTurn[0] == 0:
                        rond(65+ i*133,65+j*133 ,plateau)
                        board[i][j] = playerTurn[0]+1
                    else:
                        tracer_croix(65+ i*133,65+j*133 , plateau)
                        board[i][j] = playerTurn[0]+1
                    end = testEnd(3, board, playerTurn[0], i, j)
                    playerTurn[0] = (playerTurn[0]+1)%2
                    print(board)

    if end != 0:
        endMessage = ""
        if end==1:
            endMessage = "Le Joueur "+str(((playerTurn[0]+1)%2)+1)+" a gagner"
        elif end == 2:
            endMessage = "Partie null"
        frame.destroy()
        # frameUn
        frame = Frame(window, bg='#A6E7CD')
        frame.pack(expand=YES)

        # texte
        bienvenu = Label(frame, text=endMessage, font=("arial", 40), bg='#A6E7CD')
        bienvenu.pack(expand=YES)
        # boutton
        jouerAuMorpion = Button(frame, text="retour", font=("arial", 25), bg='#A6E7CD')
        jouerAuMorpion.pack()