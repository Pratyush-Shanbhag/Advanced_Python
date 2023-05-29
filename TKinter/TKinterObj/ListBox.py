import os
import re
from pathlib import Path
from tkinter import ttk
import tkinter as tk
from tkinter import *

class ListBoxDemo():
        def __init__(self):
                self.root = tk.Tk()
                self.root.title("Files")
                self.root.geometry('600x300')    
                self.listbox = Listbox(height = 10, width = 15, bg = "light blue", activestyle = 'dotbox', font = "Helvetica", fg = "black", selectmode='SINGLE')
                self.listbox.bind('<<ListboxSelect>>', self.getElement) #Select click
                self.label = Label(text = "TXT Files")   
                self.selection = Label(text="")
                self.text = tk.Text(height=10, width=25, bg='orange',wrap=WORD)                
                # pack the widgets
                self.listbox.selection_set(0)
                self.label.pack()
                self.selection.pack()
                self.listbox.pack()
                self.text.pack()
        def getElement(self,event):
                selection = event.widget.curselection()
                index = selection[0]
                value = event.widget.get(index)
                self.selection = value
                self.text.insert(tk.END,self.selection)
        def getFiles(self):
                # insert elements by their index and names.
                path = Path(os.getcwd())
                for file in path.iterdir():
                        # screen .cpp file
                        match = re.search("\.txt$", file.name)
                        if match:
                                self.listbox.insert(END,file.name)   
        def Run(self):
                self.getFiles()
                self.root.mainloop()        

lbox = ListBoxDemo()
lbox.Run()
