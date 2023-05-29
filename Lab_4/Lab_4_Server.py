import socket 
import sqlite3
import xml.etree.ElementTree as ET
import json


class Database:

    def __init__(self):
        self.connect()
        self.table()
        self.scrape_and_insert()

    def connect(self):
        try:
            sqliteConnection = sqlite3.connect('/Users/pratshan11/CIS_41B/Lab_4/SQLite_Lab_4.db')
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
            sqliteConnection = sqlite3.connect('/Users/pratshan11/CIS_41B/Lab_4/SQLite_Lab_4.db')
            sqlite_create_table_query = '''CREATE TABLE Database (
                                        Country TEXT PRIMARY KEY,
                                        Value TEXT NOT NULL
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
            sqliteConnection = sqlite3.connect('/Users/pratshan11/CIS_41B/Lab_4/SQLite_Lab_4.db')
            cursor = sqliteConnection.cursor()
            print("Connected to SQLite")
            sqlite_insert_query = """ INSERT INTO Database
                                    (Country, Value)
                                     VALUES (?, ?)"""

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

    def read(self, country):
        try:
            sqliteConnection = sqlite3.connect('/Users/pratshan11/CIS_41B/Lab_4/SQLite_Lab_4.db')
            cursor = sqliteConnection.cursor()
            print("Connected to SQLite")

            sqlite_select_query = """SELECT * from Database"""
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            print("Total rows are:  ", len(records))
            print("Printing each row")

            if country == "countries":
                vals = json.dumps(sorted([i[0] for i in records]))
            else:
                for i in range(0, len(records)):
                    if records[i][0] == country:
                        vals = records[i][1]
                        print(vals)
                        break

            cursor.close()
            return vals

        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        finally:
            if(sqliteConnection):
                sqliteConnection.close()
                print("The SQLite connection is closed")

    def scrape_and_insert(self):
        data_file = "/Users/pratshan11/CIS_41B/Lab_4/UNData.xml"
        tree = ET.parse(data_file)
        root = tree.getroot()
        countries = sorted(list(set([i.text for i in root.iter("Country")])))
        values = [float(i.text) for i in root.iter("Value")]

        for i in range(0, len(countries)):   
            self.insert((countries[i], json.dumps(values[i*28 : i*28+28])))


class Server:
    def __init__(self):
        self.host = socket.gethostname()
        self.port = 5000  # initiate port no above 1024
        self.server_socket = socket.socket()  # get instance
        self.server_socket.bind((self.host, self.port))  # bind host address and port together
        self.database = Database()

    def connect(self):
        while True:
            self.server_socket.listen(1)
            conn, address = self.server_socket.accept()  # accept new connection
                
            data = conn.recv(1024).decode()              # receive data stream. it won't accept data packet greater than 1024 bytes
            
            if data == "quit":
                conn.close()
                return

            vals = self.database.read(data)
            conn.send(vals.encode())  # send data to the client
            conn.close()  # close the connection


if __name__ == "__main__":
    server = Server()
    server.connect()