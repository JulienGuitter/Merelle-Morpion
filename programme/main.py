from colorama import init,Fore
from Commun import pos,cls,newInput
from morpion import menuMorpion
from merelles import menuMerelle
from multi.client import main

def menuPrincipale():
    while True:
        cls()
        pos(8,2)
        #menu Pricipal
        print("Menu Principale :")
        pos(4, 4)
        print(Fore.YELLOW,"1) ",Fore.GREEN,"Jeu du morpion", sep="")
        pos(4,5)
        print(Fore.YELLOW,"2) ",Fore.GREEN,"Jeu de Merelle", sep="")
        pos(4,6)
        print(Fore.YELLOW,"3) ",Fore.GREEN,"Multi Joueur", sep="")
        pos(4,7)
        print(Fore.YELLOW,"4) ",Fore.GREEN,"Quitter",Fore.RESET, sep="")
        pos(4,9)
        result = newInput(1, 4, "Votre choix : ")
        if result == 1:
            menuMorpion()
        elif result == 2:
            menuMerelle()
        elif result == 3:
            main()
        elif result == 4:
            cls()
            pos(15,5)
            print(Fore.GREEN,"Aurevoir")
            pos(4,7)
            input("Appuyer sur entrer pour quitter")
            quit()

if __name__ == "__main__":
    init()
    menuPrincipale()