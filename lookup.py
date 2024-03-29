#! /usr/bin/env python

import argparse
from person import Person
from address_book import AddressBook
from data_accessor import DataAccessor

## Add features:
# - Sorting by role (requires data cleanup)
# - Data cleanup (import rules to interpret and categorise data)
# - Counting people per vendor 'stats'
# - Counting people per discipline 'roles'
# - Counting people per mission and role 'mission'
# - graph some of this?
# - _all these should likely go in a separate file.py_


def print_address_book(address_book):
    for person in address_book.contacts:
        print(f"Name: {person.name}, Role: {person.role}, Email: {person.email}, "
              f"GitHub: {person.github}, Work Area: {person.work_area}, Employer: {person.employer}")
        print("-------------------")


def print_roles(address_book):
    roles = set(person.role for person in address_book.contacts())
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
    parser.add_argument("-v", "--verbose", action="store_true", help="Print all matching person data (default is only github username, for scripting")
    parser.add_argument("-m", "--email", action="store_true", help="Print e-mail address (default is only github username")
    parser.add_argument("-gh", "--github-prs", action="store_true", help="Show user's open and merged PRs")
    parser.add_argument("--search-name", action="store_true", help="Search for an entry by name")
    parser.add_argument("--search-github", action = "store_true", help="Search for an entry by GitHub username")
    # TODO: let this be the DEFAULT option
    parser.add_argument("query", nargs="+", default="", help="Search for partial matches in name, email, and github-username")
    
    args = parser.parse_args()

    # init data
    db = DataAccessor('data/address_book.db')
    address_book = db.load_from_database()

    if args.list:
        print_address_book(address_book)
    elif args.roles:
        print_roles(address_book)
    elif args.query:
        ## query is now mandatory...
        results = address_book.search(*args.query)

        if results:
            if args.github_prs:
                import webbrowser
                webbrowser.open(address_book.get_github_prs_url(args.query))
            
            for person in results:
                if args.verbose:
                    print(person)
                elif args.email:
                    print(person.email)
                else:
                    print(person.github)
        else:
            print("No matching entries found.")

    elif args.search_name:
        results = address_book.search_field("name", *args.query)
        print("Search by name: ")
        if results:
            for person in results:
                print(f"Name: {person.name}, Role: {person.role}, Email: {person.email}")
        else:
            print("No matching entries found.")
    elif args.search_github:
        results = address_book.search_field("github", *args.query)
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
