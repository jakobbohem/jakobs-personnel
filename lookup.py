#! /usr/bin/env python

import argparse
from person import Person
from address_book import AddressBook
from data_accessor import DataAccessor
from source.utils import *

## Add features (to analyze.py?):
# - Sorting by role (requires data cleanup)
# - Data cleanup (import rules to interpret and categorise data)
# - Counting people per vendor 'stats'
# - Counting people per discipline 'roles'
# - Counting people per mission and role 'mission'


def to_filter(query_list):
    filters = {}
    for pair in query_list:
        if '=' not in pair: continue
        key, value = pair.split('=', 1)  # Split only on the first '='
        filters[key.strip()] = [s.strip() for s in value.split(',')]
    return filters

def print_address_book(address_book, filter_query, formatstring=None):
    selection = address_book.filter_field(**filter_query)
    for person in selection:
        print(person.format_str(formatstring))
    print("-------------------")
    return formatstring and [p.format_str(formatstring) for p in selection] or selection

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
    parser.add_argument("-ado", "--workitems", action="store_true", help="Show user's ongoing work tasks (in ADO)")
    # parser.add_argument("--search-github", action = "store_true", help="Search for an entry by GitHub username")
    parser.add_argument("-cc", "--copy-output", action = "store_true", help="Copy the output of the command do clipboard")
    # TODO: let this be the DEFAULT option
    parser.add_argument("query", nargs="+", default="", help="Search for partial matches in name, email, and github-username")
    
    args = parser.parse_args()

    # init data
    db = DataAccessor('data/address_book.db')
    address_book = db.load_from_database()

    if args.list or 'list' in args.query[0].lower():
        formatstring = args.email and '{email};' or None
        outp = print_address_book(address_book, to_filter(args.query), formatstring)
        if args.copy_output:
            copy_to_clipboard(outp)
    elif args.roles:
        print_roles(address_book)
    else:
        results = address_book.search(*args.query)
        if results:
            if args.workitems:
                open_browser(get_ado_items_url(results[0]))
            if args.github_prs:
                # consider adding option for outputting to console (gh CLI)
                # always pick 1st?
                open_browser(get_github_prs_url(results[0]))
            
            for person in results:
                if args.verbose:
                    print(person)
                elif args.email:
                    print(f"{person.name}: {person.email}")
                else:
                    print(person.github)
        else:
            print("No matching entries found.")
    # elif args.search_github:
    #     results = address_book.search_field("github", *args.query)
    #     print("Search by GitHub username: ")
    #     if results:
    #         for person in results:
    #             print(f"Name: {person.name}, Role: {person.role}, Email: {person.email}")
    #     else:
    #         print("No matching entries found.")

    db.save_to_database(address_book)


if __name__ == '__main__':
    main()
