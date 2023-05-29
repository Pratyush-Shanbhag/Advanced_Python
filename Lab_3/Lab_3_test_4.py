import multiprocessing
import requests
from bs4 import BeautifulSoup
import sqlite3
import multiprocessing
import numpy as np
import matplotlib.pyplot as plt


class Database:

    def __init__(self):
        self.data = [[] for i in range(7)]
        self.col = 0
        self.count = -1

    def connect(self):
        try:
            sqliteConnection = sqlite3.connect('SQLite_Lab_3.db')
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
            sqliteConnection = sqlite3.connect('SQLite_Lab_3.db')
            sqlite_create_table_query = '''CREATE TABLE Database (
                                        Year INTEGER PRIMARY KEY,
                                        CO2 REAL NOT NULL,
                                        CH4 REAL NOT NULL,
                                        N2O REAL NOT NULL,
                                        CFCs REAL NOT NULL,
                                        HCFCs REAL NOT NULL,
                                        HFCs REAL NOT NULL
                                        );'''

            cursor = sqliteConnection.cursor()
            print("Successfully Connected to SQLite")
            cursor.execute(sqlite_create_table_query)
            sqliteConnection.commit()
            print("SQLite table created")

            cursor.close()

        except sqlite3.Error as error:
            pass
        finally:
            if(sqliteConnection):
                sqliteConnection.close()
                print("The SQLite connection is closed")

    def insert(self, data_tuple):
        try:
            sqliteConnection = sqlite3.connect('SQLite_Lab_3.db')
            cursor = sqliteConnection.cursor()
            print("Connected to SQLite")
            sqlite_insert_query = """ INSERT INTO Database
                                    (Year, CO2, CH4, N2O,
                                     CFCs, HCFCs, HFCs)
                                     VALUES (?, ?, ?, ?, ?, ?, ?)"""

            cursor.execute(sqlite_insert_query, data_tuple)
            sqliteConnection.commit()
            print("Entry successfully inserted into table")
            cursor.close()

        except sqlite3.Error as error:
            pass
        finally:
            if(sqliteConnection):
                sqliteConnection.close()
                print("The SQLite connection is closed")

    def read(self):
        try:
            sqliteConnection = sqlite3.connect('SQLite_Lab_3.db')
            cursor = sqliteConnection.cursor()
            print("Connected to SQLite")

            sqlite_select_query = """SELECT * from Database"""
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            print("Total rows are:  ", len(records))
            print("Printing each row")

            for row in records:
                for i in range(0, len(row)):
                    self.data[i].append(row[i])

            cursor.close()

        except sqlite3.Error as error:
            pass
        finally:
            if(sqliteConnection):
                sqliteConnection.close()
                print("The SQLite connection is closed")

    def __iter__(self):
        return self

    def __next__(self):
        self.count += 1
        if self.count < len(self.data[0]):
            return self.data[self.col][self.count]
        raise StopIteration


class Graph:

    def __init__(self, years):
        self.years = np.array(years)

    def lin_reg(self, num, name, data):
        plot = plt.figure(num)
        y = np.array(data)
        title = "Year vs. " + name + " Linear Regression Plot"
        plt.scatter(self.years, y)
        m, b = np.polyfit(self.years, y, 1)
        plt.xlabel("Year")
        plt.ylabel(name)
        plt.title(title)
        plt.plot(self.years, m*self.years + b, color="red")
        

class pro(multiprocessing.Process):

    def __init__(self, args=()):
        super().__init__()

        self.num = args[0]
        self.q = args[1]
        self.backend = args[2]


    def run(self):
        self.backend.get_thread_data(self.num, self.q)



class Backend:

    def __init__(self):
        self.database = Database()
        self.use_database()
        self.ps = []
        self.data = []
        self.scrape()
        self.graph = Graph(self.database.data[0])

    def use_database(self):
        self.database.connect()
        self.database.table()

    def scrape(self):
        page = requests.get("https://gml.noaa.gov/aggi/aggi.html")
        soup = BeautifulSoup(page.text, "html.parser")
        elems = soup.select("td")
        elems = [x.text for x in elems]
        sindex = elems.index("1979")
        lindex = elems.index("2018") + 1
        for i in range(sindex, lindex, 11):
            self.database.insert((int(elems[i]), float(elems[i+1]), float(elems[i+2]),
                                 float(elems[i+3]), float(elems[i+4]), float(elems[i+5]),
                                 float(elems[i+6])))
        
        self.database.read()

    def next(self):
        return self.database.__next__()

    def get_thread_data(self, num, q):
        self.database.col = num
        data = []

        while self.database.count < 39:
            data.append(self.next())
        q.put(data)
        self.database.count = -1

    def run(self):
        q = multiprocessing.Queue()
        backend = Backend()
        for i in range(1,7):
            p = pro(args=(i, q, backend))
            self.ps.append(p)
            p.start()

        for p in self.ps:
            p.join()

        labels = ["CO2", "CH4", "N2O", "CFCS", "HCFCs", "HFCs"]
        results = 0
        while results < 6:
            self.graph.lin_reg(results+1, labels[results], q.get())
            results += 1
        plt.show()


class Main:

    def __init__(self):
        self.backend = Backend()
        self.backend.run()


if __name__ == "__main__":
    Main()