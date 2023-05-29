from tkinter import *

root = Tk()

root.geometry("500x300")
v = IntVar()
v.set(0)

def do_clicked():
    print("Button Checked")

def do_unclicked():
    print("Button Unchecked")

def check():
    if v.get() == 0:
        do_unclicked()
    elif v.get() == 1:
        do_clicked()
    else:
        print("Huh?")

button = Checkbutton(root, text = 'Click Here', command = check, variable = v)
button.grid(row = 0, column = 0)
root.mainloop()
