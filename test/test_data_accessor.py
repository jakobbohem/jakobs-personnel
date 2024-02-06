import unittest,os, sqlite3
from data_accessor import DataAccessor
from address_book import AddressBook
from person import Person
from pathlib import Path

class TestDataAccessor(unittest.TestCase):
    db = NotImplemented
    filename = ""
    adress_book = NotImplemented

    @classmethod
    def setUpClass(cls):
        # Create sqlite db
        # note: requires using the same database file, always
        cls.filename = Path(__file__).resolve().parent / "../data/TEST.db"
        cls.filename2 = Path(__file__).resolve().parent / "../data/TEST_patchable.db"
        cls.db = DataAccessor(cls.filename, False)

        cls.address_book = AddressBook()
        persons = [
            Person("John Doe", "Developer", "john.doe@example.com", "john", "", "Developer Co", None, None),
            Person("Alice Smith", "Designer", "alice.smith@example.com", "alice1", "", "Design Co.", "TeamA", "Design"),
            Person("Bob Johnson", "Manager", "bob.johnson@example.com", "bob_git", "", "Management Corp.", "TeamA", "Management"),
            Person("Eve Doe", "Tester", "eve.doe@example.com", "eve", "", "Testing Ltd.", "TeamB", "QA"),
        ]
        for person in persons:
            cls.address_book.add_contact(person)

    def test_create_table_method(self):
        self.db.create_table_persons()
    
    def test_missing_columns(self):
        self.assertFalse(self.filename2.is_file()) 
        test_db = DataAccessor(self.filename2, False)
        conn = sqlite3.connect(test_db.dbfile)
        c = conn.cursor()   
        test_db.create_table_persons("(name TEXT, role TEXT, email TEXT, github TEXT, work_area TEXT, employer TEXT)")
        self.assertFalse(test_db.check_column_existence(c, 'team'))

        conn.commit()
        conn.close()

    def test_update_db_format(self):
        self.assertFalse(self.filename2.is_file()) 
        test_db = DataAccessor(self.filename2, False)
        conn = sqlite3.connect(test_db.dbfile)
        c = conn.cursor()   

        test_db.create_table_persons("(name TEXT, role TEXT, email TEXT, github TEXT, work_area TEXT, employer TEXT)")
        self.assertFalse(test_db.check_column_existence(c, 'team'))
        update_columns = [('team','TEXT'), ('craft', 'TEXT')]
        test_db.add_columns_if_not_exist(c, update_columns)
        self.assertTrue(test_db.check_column_existence(c, 'team'))

        conn.commit()
        conn.close()
     
    def test_write_db(self):
        # write some data to db
        self.assertTrue(os.path.exists(self.filename))
        self.db.save_to_database(self.address_book)
    
    def test_read_db(self):
        # read data from db
        self.assertTrue(os.path.exists(self.filename))
        self.assertIsNotNone(self.db)
        address_book = self.db.load_from_database()
        self.assertIsNotNone(address_book)
    
    @classmethod
    def tearDownClass(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)
        if os.path.exists(self.filename2):
            os.remove(self.filename2)

if __name__ == '__main__':
    unittest.main()
