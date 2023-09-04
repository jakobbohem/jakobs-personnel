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

def extract_person_data(table_text, company_name):
    persons = []
    
    lines = table_text.strip().split("\n")
    for line in lines:
        match = re.match(r"\| \[`([^`]+)`\]\(https:\/\/github\.com\/[^)]+\)\s*\|\s*([^|]+) +\| ([^\n|]+)", line.strip())
        if match:
            github_username, name_ado, role = match.groups()
            
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

            person = Person(name, role.strip(), email, github_username.strip(), "[]", company_name)
            persons.append(person)
    
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
