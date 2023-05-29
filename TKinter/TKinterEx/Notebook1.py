from tkinter import *
from tkinter import ttk 
window = Tk()
window.title("Welcome to Notebook app") 
window.geometry("500x300")

tab_control = ttk.Notebook(window)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab3 = ttk.Frame(tab_control)

tab_control.add(tab1, text='Notebook Tab1')
tab_control.add(tab2, text='Notebook Tab2')
tab_control.add(tab3, text='Notebook Tab3')

lbl1 = Label(tab1, text= 'page 1')
lbl1.grid(column=0, row=0)
lbl2 = Label(tab2, text= 'page 2')
lbl2.grid(column=0, row=0)
lbl3 = Label(tab3, text= 'page 3')
lbl3.grid(column=0, row=0)

tab_control.pack(expand=1, fill='both')
window.mainloop()

