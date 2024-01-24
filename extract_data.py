#! /usr/bin/env python

import re
from person import *
import address_book
from data_accessor import DataAccessor

# class Person:
#     def __init__(self, github_username, name, role, company, email=None):
#         self.github_username = github_username
#         self.name = name
#         self.role = role
#         self.company = company
#         self.email = email

def get_person(github_username, name_ado, role, company, team = None, craft = None):            
    name_match = re.search(r"@<([^>]+)>", name_ado)
    email = None
    if name_match:
        name = name_match.group(1)
    else:
        email_match = re.search(r"\[([^]]+)\]\(mailto:([^)]+)\)", name_ado)
        if email_match:
            name, email = email_match.groups()
        else:
            name = name_ado.strip()
    team = team and team.strip() or None
    craft = craft and craft.strip() or None
    return Person(name, role.strip(), email, github_username.strip(), "[]", company, team, craft)

def extract_person_data(table_text, company):
    persons = []
    ln_match = re.compile(r"\| \[`([^`]+)`\]\(https:\/\/github\.com\/[^)]+\)\s*\|\s*([^|]+)\s*+\| ([^\n|]+)\|\s*([\w\s]+)\s*\|\s*([\w\s]+)\s*\|")
    ln_match_legacy = re.compile(r"\| \[`([^`]+)`\]\(https:\/\/github\.com\/[^)]+\)\s*\|\s*([^|]+) +\| ([^\n|]+)")


    lines = table_text.strip().split("\n")
    for line in lines:
        match = ln_match.match(line.strip())
        match_legacy = ln_match_legacy.match(line.strip())
        if match:
            github_username, name_ado, role, team, craft = match.groups()
            persons.append(get_person(github_username, name_ado, role, company, team, craft))
        elif match_legacy:
            github_username, name_ado, role = match_legacy.groups()
            persons.append(get_person(github_username, name_ado, role, company))
        else:
            print(f"could not match line: {line}, will not write to db.")
    return persons

def extract_person_data_from_tables(markdown_text):
    verbose = False
    table_divide_re = re.compile(r"(\|--){3,5}\|\n?")
    table_section_re = re.compile(r"\n(?=\s?###.+\n)")
    tables = table_section_re.split(markdown_text)
    
    persons = []
    
    for table in tables:
        if not table_divide_re.search(table):
            continue
        header_match = re.search(r"^\s?###\s*([^\n]+)", table)
        if header_match:
            company_name = header_match.group(1)
            company_name = company_name.split("(")[0].strip()  # Extracting the company name from the header
            table_text = table_divide_re.split(table)[2] #[1]  # Removing the header part

            persons.extend(extract_person_data(table_text, company_name))
    
        if verbose:
            for person in persons:
                print("Company:", person.company)
                print("GitHub Username:", person.github_username)
                print("Name/ADO:", person.name)
                print("Role:", person.role)
                print()

    return persons

def main():
    # TODO: allow input args to set the source file path
    md_file_path = "rawdata/Team-github-reference.md"

    with open(md_file_path, "r") as md_file:
        markdown_text = md_file.read()

    # Split the markdown into separate tables
    addressBook = address_book.AddressBook()
    addressBook.append(extract_person_data_from_tables(markdown_text))

    # note: requires using the same database file, always
    db = DataAccessor("data/address_book.db")
    db.save_to_database(addressBook)

if __name__ == '__main__':
    main()
