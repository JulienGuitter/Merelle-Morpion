from tkinter import *

def menuMerelle(window, frame):
    frame.destroy()
    frame = Canvas(window, width=500, height=500)
    frame.create_line(20, 60, 480, 60, width=5)
    frame.create_line(60, 110, 440, 110, width=5)
    frame.create_line(100, 160, 400, 160, width=5)
    frame.create_line(20, 270, 100, 270, width=5)
    frame.create_line(60, 430, 440, 430, width=5)
    frame.create_line(100, 390, 400, 390, width=5)
    frame.create_line(400, 270, 480, 270, width=5)

    frame.create_line(20, 480, 480, 480, width=5)
    frame.create_line(20, 60, 20, 480, width=5)
    frame.create_line(480, 60, 480, 480, width=5)
    frame.create_line(60, 110, 60, 430, width=5)
    frame.create_line(440, 430, 440, 110, width=5)
    frame.create_line(100, 160, 100, 390, width=5)
    frame.create_line(400, 160, 400, 390, width=5)
    frame.create_line(250, 60, 250, 160, width=5)
    frame.create_line(250, 390, 250, 480, width=5)
    # ---------       75 + 2 * k + i * (8 - k * 2), 14 + 2 * k + j * (6 - k * 2)
    for i in range(3):
        for j in range(3):
            if i != 1 or j != 1:
                frame.create_oval(10+i*230, 50+j*210, 30+i*230, 70+j*210, fill="#E61818")
                frame.create_oval(50+i*190, 100+j*160, 70+i*190, 120+j*160, fill="#E61818")
                frame.create_oval(90+i*150, 150+j*115, 110+i*150, 170+j*115, fill="#E61818")
    """
    frame.create_oval(10, 50, 30, 70, fill="#E61818")
    frame.create_oval(240, 50, 260, 70, fill="#E61818")
    frame.create_oval(470, 50, 490, 70, fill="#E61818")
    frame.create_oval(50, 100, 70, 120, fill="#E61818")
    frame.create_oval(240, 100, 260, 120, fill="#E61818")
    frame.create_oval(430, 100, 450, 120, fill="#E61818")
    frame.create_oval(90, 150, 110, 170, fill="#E61818")
    frame.create_oval(240, 150, 260, 160, fill="#E61818")
    frame.create_oval(10, 50, 30, 70, fill="#E61818")

    frame.create_oval(390, 260, 410, 280, fill="#E61818")
    """

    frame.pack()
    window.mainloop()