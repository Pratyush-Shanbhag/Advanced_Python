import requests
from bs4 import BeautifulSoup
import sqlite3
import matplotlib.pyplot as plt
import tkinter as tk


class Database:

    def __init__(self):
        pass

    def connect(self):
        try:
            sqliteConnection = sqlite3.connect('SQLite_Lab_2.db')
            cursor = sqliteConnection.cursor()
            print("Database created and Successfully Connected to SQLite")
            cursor.close()
        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
        finally:
            if(sqliteConnection):
                sqliteConnection.close()
                print("The SQLite connection is closed")
            
    def table(self):
        try:
            sqliteConnection = sqlite3.connect('SQLite_Lab_2.db')
            sqlite_create_table_query = '''CREATE TABLE Database (
                                        Country TEXT PRIMARY KEY,
                                        Fossil_CO2_Emissions_1990 REAL NOT NULL,
                                        Fossil_CO2_Emissions_2007 REAL NOT NULL,
                                        Fossil_CO2_Emissions_2017 REAL NOT NULL,
                                        Fossil_CO2_Emissions_pct_of_World_2017 REAL NOT NULL,
                                        Fossil_CO2_Emissions_pct_change_2017_vs_1990 REAL NOT NULL,
                                        Fossil_CO2_Emissions_Per_Land_Area_2017 REAL NOT NULL,
                                        Fossil_CO2_Emissions_Per_Capita_2017 REAL NOT NULL,
                                        CO2_Emissions_Total_Including_LUCF_2018 REAL NOT NULL,
                                        CO2_Emissions_Total_Excluding_LUCF_2018 REAL NOT NULL
                                        );'''

            cursor = sqliteConnection.cursor()
            print("Successfully Connected to SQLite")
            cursor.execute(sqlite_create_table_query)
            sqliteConnection.commit()
            print("SQLite table created")

            cursor.close()

        except sqlite3.Error as error:
            print("Error while creating a sqlite table", error)
        finally:
            if(sqliteConnection):
                sqliteConnection.close()
                print("The SQLite connection is closed")

    def insert(self, data_tuple):
        try:
            sqliteConnection = sqlite3.connect('SQLite_Lab_2.db')
            cursor = sqliteConnection.cursor()
            print("Connected to SQLite")
            sqlite_insert_query = """ INSERT INTO Database
                                    (Country, Fossil_CO2_Emissions_1990,
                                     Fossil_CO2_Emissions_2007,
                                     Fossil_CO2_Emissions_2017,
                                     Fossil_CO2_Emissions_pct_of_World_2017,
                                     Fossil_CO2_Emissions_pct_change_2017_vs_1990,
                                     Fossil_CO2_Emissions_Per_Land_Area_2017,
                                     Fossil_CO2_Emissions_Per_Capita_2017,
                                     CO2_Emissions_Total_Including_LUCF_2018,
                                     CO2_Emissions_Total_Excluding_LUCF_2018)
                                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

            cursor.execute(sqlite_insert_query, data_tuple)
            sqliteConnection.commit()
            print("Entry successfully inserted into table")
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to insert blob data into sqlite table", error)
        finally:
            if(sqliteConnection):
                sqliteConnection.close()
                print("The SQLite connection is closed")

    def read(self):
        try:
            sqliteConnection = sqlite3.connect('SQLite_Lab_2.db')
            cursor = sqliteConnection.cursor()
            print("Connected to SQLite")

            sqlite_select_query = """SELECT * from Database"""
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            print("Total rows are:  ", len(records))
            print("Printing each row")

            data = [[] for i in range(10)]
            for row in records:
                for i in range(0, len(row)):
                    data[i].append(row[i])

            cursor.close()
            return data

        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        finally:
            if(sqliteConnection):
                sqliteConnection.close()
                print("The SQLite connection is closed")


class Graph:

    def __init__(self, data):
        self.data = data

    def pie_chart(self):
        total = sum(self.data[4])
        plt.pie(self.data[4], labels=self.data[0], autopct=lambda x: '{:.2f}%'.format(x * total / 100))
        plt.title("Top 10 Countries with Most CO2 Fuel Emissions\nPercent of the World in 2017")
        plt.show()


class Backend:

    def __init__(self, co2_data_file):
        self.co2_data_file = co2_data_file
        self.database = Database()
        self.use_database()
        self.scrape()
        self.graph = Graph(self.extract())        

    def use_database(self):
        self.database.connect()
        self.database.table()

    def scrape(self):
        page = requests.get(self.co2_data_file)
        soup = BeautifulSoup(page.text, "html.parser")
        elems = soup.select("td")
        sindex = 0
        lindex = 0
        for i in range(0, len(elems)):
            if elems[i].text.find("Afghanistan") >= 0:
                sindex = i
            if elems[i].text.find("Zimbabwe") >= 0:
                lindex = i
                break

        elems = [x.text.replace(",", "").replace("%", "") for x in elems]
        for i in range(sindex, lindex+1):
            if len(elems[i]) == 0:
                elems[i] = "0"

        for i in range(sindex,lindex+1, 10):     
            if elems[i+8].find("/") >= 0:
                elems[i+8] = elems[i+8][:elems[i+8].find("/")]
                elems[i+9] = elems[i+8][:elems[i+9].find("/")]
                
            self.database.insert((elems[i].replace(u"\xa0", u""), float(elems[i+1]), float(elems[i+2]),
                                 float(elems[i+3]), float(elems[i+4]), float(elems[i+5]),
                                 float(elems[i+6]), float(elems[i+7]), float(elems[i+8]),
                                 float(elems[i+9].replace("\n", "0"))))

    def extract(self):
        data = self.database.read()
        low = 0
        for i in range(0, len(data[4])):
            low = i
            for j in range(i+1, len(data[4])):
                if data[4][low] > data[4][j]:
                    low = j
            for y in data:
                y[i], y[low] = y[low], y[i]
                
        top_10 = [x[-10:] for x in data]

        return top_10
        
    def graph_pie_chart(self):
        self.graph.pie_chart()


class Frontend:

    def __init__(self):
        self.backend = Backend("https://en.wikipedia.org/wiki/List_of_countries_by_carbon_dioxide_emissions")
        self.master = tk.Tk()
        self.add_buttons()

    def add_buttons(self):
        self.master.geometry("500x500")
        self.master.title("CIS 41B Lab 2 - Web Scraping")
        button1 = tk.Button(self.master, text="Graph Line Plot", width=25, height=10, fg="red", command=lambda : self.backend.graph_pie_chart(), pady=15)
        button1.pack(side="top", pady=150)
        self.master.mainloop()


run = Frontend()