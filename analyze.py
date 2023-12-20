#! /usr/bin/env python

import argparse
from person import Person
from address_book import AddressBook
from data_accessor import DataAccessor

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
            
def main():
    parser = argparse.ArgumentParser(description="Address Book CLI")
    parser.add_argument("--list", action="store_true", help="List all entries in the address book")
    parser.add_argument("--roles", action="store_true", help="List all available roles")
 
 
    args = parser.parse_args()

    # init data
    db = DataAccessor('data/address_book.db')
    address_book = db.load_from_database()

    # if args.list:
    #     print_address_book(address_book)
    if args.roles:
        print_role_match(address_book, "code")
        print_role_match(address_book, "dev")



if __name__ == '__main__':
    main()