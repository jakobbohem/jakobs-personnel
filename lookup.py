import argparse
# import sqlite3
from person import Person
from address_book import AddressBook
from data_accessor import DataAccessor


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

def search_persons(address_book, search_term):
    matching_github_usernames = []
    search_term = search_term.lower()
    
    for person in address_book.persons():
        if (search_term in person.name.lower() or
            search_term in person.email.lower() if person.email else False or
            search_term in person.github_username.lower()):
            matching_github_usernames.append(person.github_username)
    
    return matching_github_usernames

def main():
    parser = argparse.ArgumentParser(description="Address Book CLI")
    parser.add_argument("--list", action="store_true", help="List all entries in the address book")
    parser.add_argument("--roles", action="store_true", help="List all available roles")
    parser.add_argument("--search-name", help="Search for an entry by name")
    parser.add_argument("--search-github", help="Search for an entry by GitHub username")
    # TODO: let this be the DEFAULT option
    parser.add_argument("--search", help="Search for partial matches in name, email, and github-username")
    
    args = parser.parse_args()

    # init data
    db = DataAccessor('data/adress_book.db')
    address_book = db.load_from_database()

    if args.list:
        print_address_book(address_book)
    elif args.roles:
        print_roles(address_book)
    elif args.search:
        results = address_book.search(*args.search.split())

        if results:
            print("Matches: ")
            for person in results:
                print("gh:", person.github_username)
        else:
            print("No matching entries found.")
    elif args.search_name:
        results = address_book.search_field("name", args.search_name)
        print("Search by name: ")
        if results:
            for person in results:
                print(f"Name: {person.name}, Role: {person.role}, Email: {person.email}")
        else:
            print("No matching entries found.")
    elif args.search_github:
        results = address_book.search_field("github", args.search_github)
        print("Search by GitHub username: ")
        if results:
            for person in results:
                print(f"Name: {person.name}, Role: {person.role}, Email: {person.email}")
        else:
            print("No matching entries found.")
    else:
        parser.print_help()

    db.save_to_database(address_book)


if __name__ == '__main__':
    main()
