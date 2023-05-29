import sqlite3
import re
import matplotlib.pyplot as plt
import tkinter as tk
import numpy as np


class Database:

    def __init__(self):
        pass

    def connect(self):
        try:
            sqliteConnection = sqlite3.connect('SQLite_Python.db')
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
            sqliteConnection = sqlite3.connect('SQLite_Python.db')
            sqlite_create_table_query = '''CREATE TABLE Database (
                                        year INTEGER PRIMARY KEY,
                                        temp REAL NOT NULL);'''

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

    def insert(self, year, temp):
        try:
            sqliteConnection = sqlite3.connect('SQLite_Python.db')
            cursor = sqliteConnection.cursor()
            print("Connected to SQLite")
            sqlite_insert_query = """ INSERT INTO Database
                                    (year, temp) VALUES (?, ?)"""

            # Convert data into tuple format
            data_tuple = (year, temp)
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
            sqliteConnection = sqlite3.connect('SQLite_Python.db')
            cursor = sqliteConnection.cursor()
            print("Connected to SQLite")

            sqlite_select_query = """SELECT * from Database"""
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            print("Total rows are:  ", len(records))
            print("Printing each row")
            data = [[], []]
            for row in records:
                data[0].append(row[0])
                data[1].append(row[1])

            cursor.close()

        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        finally:
            if(sqliteConnection):
                sqliteConnection.close()
                print("The SQLite connection is closed")

        return data


class Graph:

    def __init__(self):
        pass

    def plot(self, data):
        plt.plot(data[0], data[1])
        plt.xlabel("Year")
        plt.ylabel("Median Temperature")
        plt.title("Year vs. Median Temperature Line Plot")
        plt.show()

    def bar(self, data):
        plt.xlabel("Year")
        plt.ylabel("Median Temperature")
        plt.title("Year vs. Median Temperature Bar Plot")
        plt.bar(data[0], data[1], label="median")
        plt.show()

    def lin_reg(self, data):
        x = np.array(data[0])
        y = np.array(data[1])

        plt.scatter(x, y)
        m, b = np.polyfit(x, y, 1)
        plt.xlabel("Year")
        plt.ylabel("Median Temperature")
        plt.title("Year vs. Median Temperature Linear Regression Plot")
        plt.plot(x, m*x + b, color="red")
        plt.show()


class Backend:

    def __init__(self, temp_data_file):
        self.temp_data_file = temp_data_file
        self.database = Database()
        self.database.connect()
        self.database.table()
        self.use_database()
        self.graph = Graph()

    def use_database(self):
        raw_data = []
        file = open(self.temp_data_file, "r")
        for line in file:
            raw_data.append(line)
        file.close()
        for line in raw_data:
            if len(re.findall(r"-?[0-9]+\.[0-9]+", line)) > 0 and 1850 <= int(re.findall(r"[0-9]{4}", line)[0]) <= 2018:
                self.database.insert(int(re.findall(r"[0-9]{4}", line)[0]), float(re.findall(r"-?[0-9]+\.[0-9]+", line)[0]))

    def graph_plot(self):
        self.graph.plot(self.database.read())

    def graph_bar(self):
        self.graph.bar(self.database.read())

    def graph_lin_reg(self):
        self.graph.lin_reg(self.database.read())


class Frontend:

    def __init__(self):
        self.master = tk.Tk()
        self.backend = Backend("Temperature.html")
        self.add_buttons()

    def add_buttons(self):
        self.master.geometry("500x500")
        self.master.title("CIS 41B Lab 1 - Data Visualization")
        button1 = tk.Button(self.master, text="Graph Line Plot", width=25, height=10, fg="red", command=lambda : self.backend.graph_plot())
        button1.pack(side="top")
        button2 = tk.Button(self.master, text="Graph Bar Plot", width=25, height=10, fg="red", command=lambda : self.backend.graph_bar())
        button2.pack(side="top")
        button3 = tk.Button(self.master, text="Graph Linear Regression Plot", width=25, height=10, fg="red", command=lambda : self.backend.graph_lin_reg())
        button3.pack(side="top")
        self.master.mainloop()


run = Frontend()