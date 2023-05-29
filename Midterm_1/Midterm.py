import requests
from bs4 import BeautifulSoup
import pandas as pd
from tkinter import *



class Presidents:
    
    def __init__(self):
        page = requests.get("https://www.thoughtco.com/presidents-and-vice-presidents-chart-4051729")
        soup = BeautifulSoup(page.text, "html.parser")
        elems = soup.select("td")

        pres_list = [elems[i].text for i in range(0, len(elems)) if not elems[i].text[0].isnumeric()]
        pres_dict = {"Presidents": [pres_list[i] for i in range(0, len(pres_list), 3)],
            "Vice-Presidents": [pres_list[i] for i in range(1, len(pres_list), 3)]}

        self.df = pd.DataFrame.from_dict(pres_dict)
        self.index = -1

    def __iter__(self):
        return self

    def __next__(self):
        self.index += 1
        if self.index < self.df.shape[0]:
            return self.df.loc[self.index].at["Presidents"]
        raise StopIteration

    def frontend(self):
        master = Tk()
        master.geometry("500x500")
                
        lbox=Listbox(master, background="white", selectbackground="yellow")
        for i in range(0, self.df.shape[0]):
            lbox.insert("end", self.df.loc[i].at["Vice-Presidents"])
        lbox.bind("<Double-Button-1>", self.OnDouble)
        lbox.pack(side="top", fill="both", expand=True)

        master.mainloop()

    def OnDouble(self, event):
            widget = event.widget
            selection = widget.curselection()
            value = widget.get(selection[0])
            print(f"{value} is Vice-President #{selection[0]+1}")

    def sort(self):
        self.df.sort_values(by=["Presidents"], inplace=True)
        print(self.df)
    
        

pres = Presidents()
i = 1
'''for p in pres:
    print(i, p)
    i += 1'''

while i < 4:
    print(i, pres.__next__())
    i += 1

#pres.sort()

