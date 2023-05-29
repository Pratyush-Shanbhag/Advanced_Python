from tkinter import ttk
import tkinter as tk
from tkinter import *

class RadioButtonDemo:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Languages")
        self.root.geometry('600x300')  
        self.values = {"C++" : ".cpp","Java" : ".java", "Python" : ".py"}   
        self.vs = StringVar()
        self.label = Label( textvariable=self.vs, relief=SUNKEN,background = "light green" )
    def print_selection(self):
        self.label.setvar(self.vs.get())
    def Run(self): 
        for (text, value) in self.values.items():
            Radiobutton(text = text, variable = self.vs, value = value, indicator = 0,background = "light blue",command=self.print_selection).pack(fill=X)
        self.label.pack(side='top',ipady=10,fill=X)
        self.root.mainloop()    
    
rbutton = RadioButtonDemo()
rbutton.Run()