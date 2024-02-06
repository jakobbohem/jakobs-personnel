import sqlite3, sys
from person import Person
from pathlib import Path
from address_book import AddressBook

class DataAccessor:
    def __init__(self, dbfile, create_table=True):
        self.dbfile = get_absolute(dbfile)
        self.table_name = "persons" # should there ever be more?
        print(f"debug:: DB-file {self.dbfile}")
        if(create_table):
            self.create_table_persons()

            update_columns = [('team','TEXT'), ('craft', 'TEXT')]
            self.add_columns_if_not_exist(c, update_columns)

    # def initialize_database():
    def create_table_persons(self, columns="(name TEXT, role TEXT, email TEXT, github TEXT, work_area TEXT, employer TEXT, team TEXT, craft TEXT)"):
        conn = sqlite3.connect(self.dbfile)
        c = conn.cursor()
        # print("DEBUG")
        # for col in columns.split(', '):
        #     print (col)
        c.execute(f'''CREATE TABLE IF NOT EXISTS {self.table_name}
                    {columns}''')

        # print(f"# columns {len(c.fetchall())}")

        conn.commit()
        conn.close()
    
    def save_to_database(self, address_book):
        conn = sqlite3.connect(self.dbfile)
        c = conn.cursor()

        c.execute("DELETE FROM persons")

        for person in address_book.contacts():
            c.execute("INSERT INTO persons VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (person.name, person.role, person.email, person.github, person.work_area, person.employer, person.team, person.craft))

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
    
    # helpers to ensure relevant columns exist
    def check_column_existence(self, cursor, column_name):
        cursor.execute(f"PRAGMA table_info({self.table_name})")
        columns = cursor.fetchall()
        for col in columns:
            print(col)
        return any(column[1] == column_name for column in columns)

    def add_columns_if_not_exist(self, cursor, columns):
        for column_name, column_type in columns:
            if not self.check_column_existence(cursor, column_name):
                cursor.execute(f"ALTER TABLE {self.table_name} ADD COLUMN {column_name} {column_type};")


def get_absolute(dbfile):
    return str(Path(sys.argv[0]).parent.absolute() / dbfile)
