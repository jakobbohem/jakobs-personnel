
import matplotlib.pyplot as plt
import numpy as np
import sqlite3

class GraphTool:
    def __init__(self, dbfile = 'data/address_book.db'):
        self.conn = sqlite3.connect(dbfile)
        self.cursor = self.conn.cursor()

    def __str__(self):
        return "GraphTool"+self.dbfile

    def plot_github(self, blob, userfilter=[]):
        # all the commits are in the data blob

        # FILTERED! extract the present users/contributors
        users = set(item['author']['login'] for item in blob if item['author']['login'] in userfilter)

        # Split the data by user
        split_data = {user: [item for item in blob if item['author']['login'] == user] for user in users}
        user_commits = {}
        user_counts = {user: sum(1 for item in blob if item['author']['login'] == user) for user in users}
        user_lines_added = {user: sum(item['additions'] for item in blob if item['author']['login'] == user) for user in users}

        # Plotting (doubel axes)
        # Create a figure and primary axes
        fig, ax1 = plt.subplots()
        bar_width = 0.35
        x = np.arange(len(users))
        ax1.bar(x - bar_width/2, user_counts.values(), bar_width, color='b', label='merged')
        ax2 = ax1.twinx()

        # Plot the second set of bars on the secondary axes
        ax2.bar(x + bar_width/2, user_lines_added.values(), bar_width, color='r', alpha=0.5, label='additions')
        ax1.set_xlabel('User')
        ax1.set_ylabel('Number of PRs merged', color='b')
        ax2.set_ylabel('additions (accum.)', color='r')
        plt.title('Number of PRs merged per author')
        ax1.set_xticks(x)
        ax1.set_xticklabels(users, rotation=45)

        # Show legend
        plt.legend(loc='upper left')
        # plt.xticks(rotation=45)  # Rotate x-axis labels for better readability

        plt.show(block=True)

    def plot_persons(self, column_name):
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