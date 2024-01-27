from tkinter import *
from morpionGraphique import menuMorpion
from merelleGraphique import menuMerelle


def plateau():
    window = Tk()
    window.title("Morpion et Merelle")
    window.geometry("600x600")
    window.minsize(400, 400)
    window.maxsize(960, 540)
    window.config(background='#A6E7CD')


    #frameUn
    frame = Frame(window,bg='#A6E7CD')
    frame.pack(expand=YES)

    #texte
    bienvenu = Label(frame, text="Menu Principale",font=("arial", 40), bg='#A6E7CD')
    bienvenu.pack(expand=YES)
    #boutton
    boutonMorpion = Button(frame, text="Morpion", font=("arial",25),bg='#A6E7CD', command=lambda: menuMorpion(window, frame), width=7)
    boutonMerelle = Button(frame, text="Merelle", font=("arial",25),bg='#A6E7CD', command=lambda: menuMerelle(window, frame), width=7)
    boutonQuitter = Button(frame, text="Quitter", font=("arial",25),bg='#A6E7CD', command=quit, width=7)
    boutonMorpion.pack()
    boutonMerelle.pack()
    boutonQuitter.pack()
    window.mainloop()



plateau()

