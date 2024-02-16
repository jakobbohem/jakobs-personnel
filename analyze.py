#! /usr/bin/env python

import argparse
from person import Person
from address_book import AddressBook
from data_accessor import DataAccessor

import sqlite3
import matplotlib.pyplot as plt

def print_role_has(address_book, query):
    roles = set(person.role for person in address_book.contacts())
    print(f"Has role matching {query}")
    for role in roles:
        print(role)

def print_role_match(address_book, query):
    results = address_book.search_field("role", query)

    # roles = set(person.role for person n address_book.contacts())
    print(f"Has role matching {query}:")
    if results:
        for person in results:
            print(f"Name: {person.name}, Role: {person.role}, gh: {person.github}, (Email: {person.email})")
        else:
            print("No matching entries found.")

        print(f"total: {len(results)}")


def plot_data(column_name):
    # TODO: (jakob) wrap this into the Addressbook interface!
    # Connect to SQLite database
    conn = sqlite3.connect('data/address_book.db')
    cursor = conn.cursor()
    
    # Fetch data from the database
    table = "persons"
    # cursor.execute(f"SELECT {column_name}, COUNT(*) FROM {table} GROUP BY {column_name}")
    cursor.execute(f"SELECT {column_name}, COUNT(*) FROM {table} WHERE {column_name} IS NOT NULL GROUP BY {column_name}")
    data = cursor.fetchall()
    
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

def graph(graph_vector):
    # graph the split between disciplines (crafts) for now

    print("to be implemented")

def main():
    parser = argparse.ArgumentParser(description="Address Book CLI")
    parser.add_argument("--list", action="store_true", help="List all entries in the address book")
    parser.add_argument("--roles", action="store_true", help="List all available roles")
    parser.add_argument("--teams", action="store_true", help="List all available teams")
    parser.add_argument("-g", "--graph", default="", help="Graph the split of personnel data along some vector ('craft', 'team', 'organisation')")
 
 
    args = parser.parse_args()

    # init data
    db = DataAccessor('data/address_book.db')
    address_book = db.load_from_database()

    if args.graph:
        plot_data(args.graph)
        return
    
    if args.roles:
        print_role_match(address_book, "code")
        print_role_match(address_book, "dev")



if __name__ == '__main__':
    main()