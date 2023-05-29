import xml.etree.ElementTree as ET
import sqlite3
import socket
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
import json
import sys


class Client:
    def __init__(self):
        self.host = socket.gethostname()  # as both code is running on same pc
        self.port = 5000  # socket server port number

    def connect(self, query):
        client_socket = socket.socket()  # instantiate
        client_socket.connect((self.host, self.port))  # connect to the server
        client_socket.send(query.encode())  # send message
        if query != "quit":
            data = client_socket.recv(1024).decode()  # receive response
            client_socket.close()  # close the connection
            return json.loads(data)
        client_socket.close()  # close the connection


class Graph:

    def __init__(self):
        pass

    def plot(self, country, data):
        data.reverse()
        plt.plot(np.array([num for num in range(1990, 2018)]), np.array(data))
        plt.xlabel("Year")
        plt.ylabel("Values")
        plt.title(f"{country} Line Plot")
        plt.show()


class Backend:

    def __init__(self):
        self.client = Client()
        self.graph = Graph()

    def get_countries(self):
        return self.client.connect("countries")

    def graph_plot(self, country):
        self.graph.plot(country, self.client.connect(country))

    def close(self):
        self.client.connect("quit")


class Frontend:

    def __init__(self):
        self.backend = Backend()
        self.master = tk.Tk()
        self.master.geometry("300x250")
        self.master.title("Lab 4")
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.add_dropdown()

    def add_dropdown(self):
        variable = tk.StringVar(self.master)
        countries = self.backend.get_countries()
        variable.set(countries[0]) # default value
        w = tk.OptionMenu(self.master, variable, *countries)
        w.pack(pady=60)
        button = tk.Button(self.master, text="Submit", height=3, width=10, command=lambda : self.click(variable))
        button.pack()
        self.master.mainloop()

    def on_closing(self):
        self.backend.close()
        self.master.destroy()       

    def click(self, variable):
        return self.backend.graph_plot(variable.get())


run = Frontend()