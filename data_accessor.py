import sqlite3, sys
from person import Person
from pathlib import Path
from address_book import AddressBook

def get_absolute(dbfile):
    return str(Path(sys.argv[0]).parent.absolute() / dbfile)

class DataAccessor:
    def __init__(self, dbfile):
        self.dbfile = get_absolute(dbfile)

        conn = sqlite3.connect(self.dbfile)
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS persons
                    (name TEXT, role TEXT, email TEXT, github TEXT, work_area TEXT, employer TEXT)''')

        conn.commit()
        conn.close()

    # def initialize_database():
        

    def save_to_database(self, address_book):
        conn = sqlite3.connect(self.dbfile)
        c = conn.cursor()

        c.execute("DELETE FROM persons")

        for person in address_book.contacts():
            c.execute("INSERT INTO persons VALUES (?, ?, ?, ?, ?, ?)",
                    (person.name, person.role, person.email, person.github, person.work_area, person.employer))

        conn.commit()
        conn.close()

    def load_from_database(self):
        conn = sqlite3.connect(self.dbfile)
        c = conn.cursor()

        c.execute("SELECT * FROM persons")
        rows = c.fetchall()

        address_book = AddressBook()

        for row in rows:
            person = Person(*row)
            address_book.add_contact(person)

        conn.close()

        return address_book