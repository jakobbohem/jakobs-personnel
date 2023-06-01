import argparse
import sqlite3
from person import Person
from address_book import AddressBook


def print_address_book(address_book):
    for person in address_book.contacts:
        print(f"Name: {person.name}, Role: {person.role}, Email: {person.email}, "
              f"GitHub: {person.github}, Work Area: {person.work_area}, Employer: {person.employer}")
        print("-------------------")


def print_roles(address_book):
    roles = set(person.role for person in address_book.contacts)
    print("Available Roles:")
    for role in roles:
        print(role)


def initialize_database():
    conn = sqlite3.connect("address_book.db")
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS persons
                (name TEXT, role TEXT, email TEXT, github TEXT, work_area TEXT, employer TEXT)''')

    conn.commit()
    conn.close()


def save_to_database(address_book):
    conn = sqlite3.connect("address_book.db")
    c = conn.cursor()

    c.execute("DELETE FROM persons")

    for person in address_book.contacts:
        c.execute("INSERT INTO persons VALUES (?, ?, ?, ?, ?, ?)",
                  (person.name, person.role, person.email, person.github, person.work_area, person.employer))

    conn.commit()
    conn.close()


def load_from_database():
    conn = sqlite3.connect("address_book.db")
    c = conn.cursor()

    c.execute("SELECT * FROM persons")
    rows = c.fetchall()

    address_book = AddressBook()

    for row in rows:
        person = Person(*row)
        address_book.add_contact(person)

    conn.close()

    return address_book


def main():
    initialize_database()

    address_book = load_from_database()

    # Adding contacts
    person1 = Person("John Doe", "Software Engineer", "john.doe@example.com", "johndoe", "Machine Learning", "ABC Inc.")
    person2 = Person("Jane Smith", "Data Scientist", "jane.smith@example.com", "janesmith", "Data Analytics", "XYZ Corp.")
    address_book.add_contact(person1)
    address_book.add_contact(person2)

    parser = argparse.ArgumentParser(description="Address Book CLI")
    parser.add_argument("--list", action="store_true", help="List all entries in the address book")
    parser.add_argument("--roles", action="store_true", help="List all available roles")
    parser.add_argument("--search-name", help="Search for an entry by name")
    parser.add_argument("--search-github", help="Search for an entry by GitHub username")

    args = parser.parse_args()

    if args.list:
        print_address_book(address_book)
    elif args.roles:
        print_roles(address_book)
    elif args.search_name:
        results = address_book.search("name", args.search_name)
        print("Search by name: ")
        if results:
            for person in results:
                print(f"Name: {person.name}, Role: {person.role}, Email: {person.email}")
        else:
            print("No matching entries found.")
    elif args.search_github:
        results = address_book.search("github", args.search_github)
        print("Search by GitHub username: ")
        if results:
            for person in results:
                print(f"Name: {person.name}, Role: {person.role}, Email: {person.email}")
        else:
            print("No matching entries found.")
    else:
        parser.print_help()

    save_to_database(address_book)


if __name__ == '__main__':
    main()
