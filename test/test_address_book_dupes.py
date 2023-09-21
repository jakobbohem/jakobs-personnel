import unittest
from person import Person
from address_book import AddressBook


class AddressBookDuplicatesTests(unittest.TestCase):
    def setUp(self):
        self.address_book = AddressBook()
        person1 = Person("John Doe", "Software Engineer", "john.doe@example.com", "johndoe", "Machine Learning", "ABC Inc.")
        person2 = Person("Jane Smith", "Data Scientist", "jane.smith@example.com", "janesmith", "Data Analytics", "XYZ Corp.")
        self.address_book.add_contact(person1)
        self.address_book.add_contact(person2)

    def test_add_contact_duplicate_email(self):
        person3 = Person("Alice Johnson", "Designer", "jane.smith@example.com", "alicej", "UI/UX Design", "Design Co.")
        self.address_book.add_contact(person3)
        self.assertEqual(len(self.address_book.contacts()), 2)

    def test_add_contact_unique_email(self):
        person4 = Person("Bob Brown", "Developer", "bob.brown@example.com", "bobb", "Web Development", "Web Dev Inc.")
        self.address_book.add_contact(person4)
        self.assertEqual(len(self.address_book.contacts()), 3)

if __name__ == '__main__':
    unittest.main()
