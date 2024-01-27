def pos(x, y):
    print("\x1b[" + str(y) + ";" + str(x) + "H", end="")

def cls():
    print("\x1b[2J\x1b[H",end="")

def newInput(min, max, question):
    x = -1
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