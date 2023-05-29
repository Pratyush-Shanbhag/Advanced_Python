import xml.etree.ElementTree as ET

data_file = "/Users/pratshan11/CIS_41B/Lab_4/UNData.xml"
tree = ET.parse(data_file)
root = tree.getroot()
countries = sorted(list(set([i.text for i in root.iter("Country")])))
print(countries)

'''
master = tk.Tk()
master.geometry("500x500")

variable = tk.StringVar(master)
variable.set("one") # default value

w = tk.OptionMenu(master, variable, "one", "two", "three")
w.pack()

tk.mainloop()
'''