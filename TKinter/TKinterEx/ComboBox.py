import tkinter as tk
from tkinter import ttk

tkwindow = tk.Tk()
tkwindow.geometry("500x300")

def Selected(event):
    print(type(event))

cbox = ttk.Combobox(tkwindow, values = ["Alpha","Beta","Gamma"], state='readonly')
cbox.grid(column=0, row=0)
cbox.current(0)
cbox.bind("<<ComboboxSelected>>", Selected)
tkwindow.mainloop()
