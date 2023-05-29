import requests
from bs4 import BeautifulSoup
import json
import sqlite3
import threading
import pandas as pd
import matplotlib.pyplot as plt

class Database:

    def __init__(self):
        self.data = []
        self.count = -1

    def connect(self):
        try:
            sqliteConnection = sqlite3.connect('/Users/pratshan11/CIS_41B/Lab_3/Midterm_2.db')
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
            sqliteConnection = sqlite3.connect('/Users/pratshan11/CIS_41B/Lab_3/Midterm_2.db')
            sqlite_create_table_query = '''CREATE TABLE Database (
                                        Country TEXT PRIMARY KEY
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
            sqliteConnection = sqlite3.connect('/Users/pratshan11/CIS_41B/Lab_3/Midterm_2.db')
            cursor = sqliteConnection.cursor()
            print("Connected to SQLite")
            sqlite_insert_query = """ INSERT INTO Database
                                    (Country) VALUES (?)"""

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
            sqliteConnection = sqlite3.connect('/Users/pratshan11/CIS_41B/Lab_3/Midterm_2.db')
            cursor = sqliteConnection.cursor()
            print("Connected to SQLite")

            sqlite_select_query = """SELECT * from Database"""
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            print("Total rows are:  ", len(records))
            print("Printing each row")

            cursor.close()
            self.data = [''.join(row) for row in records]

        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        finally:
            if(sqliteConnection):
                sqliteConnection.close()
                print("The SQLite connection is closed")

    def __iter__(self): 
        return self

    def __next__(self):
        self.count += 1
        if self.count < len(self.data):
            return self.data[self.count]
        raise StopIteration


db = Database()
db.connect()
db.table()

page = requests.get("https://worldpopulationreview.com/country-rankings/pollution-by-country")
soup = BeautifulSoup(page.text, "html.parser")

elems = soup.select("li")
elems = [x.text for x in elems]
json_elems = json.dumps(elems[elems.index("China") : elems.index("Italy/San Marino/Vatican City") + 1])

sorted_json_elems = json.dumps(sorted(json.loads(json_elems)))

def insert_into_db(sorted_json_elems): 
    for country in json.loads(sorted_json_elems):
        db.insert((country,))

#lock = threading.Lock()

insert_into_db(sorted_json_elems)
db.read()
data = []
def get_country(data):
    #lock.acquire()
    data.append(db.__next__())

    #lock.release()



def thread_and_plot():
    ts = []
    for i in range(19):
        t = threading.Thread(target=get_country,args=(data,))
        ts.append(t)
        t.start()

    for thread in ts:
        thread.join()

    df = pd.DataFrame({"Countries":data})
    length = df.shape[0]

    plt.pie([length/100 for i in range(length)], labels=df["Countries"].to_list())
    plt.show()
    



if __name__ == "__main__":
    thread_and_plot()

