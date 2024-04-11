
import matplotlib.pyplot as plt
import sqlite3

class GraphTool:
    def __init__(self, dbfile = 'data/address_book.db'):
        self.conn = sqlite3.connect(dbfile)
        self.cursor = self.conn.cursor()

    def __str__(self):
        return "GraphTool"+self.dbfile

    def plot_data(self, column_name):
        # TODO: (jakob) wrap this into the Addressbook interface!
        # Connect to SQLite database
        
        # Fetch data from the database
        table = "persons"
        # cursor.execute(f"SELECT {column_name}, COUNT(*) FROM {table} GROUP BY {column_name}")
        self.cursor.execute(f"SELECT {column_name}, COUNT(*) FROM {table} WHERE {column_name} IS NOT NULL GROUP BY {column_name}")
        data = self.cursor.fetchall()
        
        # Extract labels and values
        labels, values = zip(*data)
        
        # Plotting
        plt.bar(labels, values)
        plt.xlabel(column_name)
        plt.ylabel('People')
        plt.title(f'Team split by {column_name}')
        plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
        plt.tight_layout()
        plt.show(block=True)

        # Input the column name you want to plot
        # column_name = input("Enter the column name you want to plot: ")

    def graph(self, graph_vector):
        # graph the split between disciplines (crafts) for now
        print("to be implemented")