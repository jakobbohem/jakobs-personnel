import unittest
from person import Person
from address_book import AddressBook


class AddressBookTests(unittest.TestCase):
    def setUp(self):
        self.address_book = AddressBook()
        person1 = Person("John Doe", "Software Engineer", "john.doe@example.com", "johndoe", "Machine Learning", "ABC Inc.")
        person2 = Person("Jane Smith", "Data Scientist", "jane.smith@example.com", "janesmith", "Data Analytics", "XYZ Corp.")
        self.address_book.add_contact(person1)
        self.address_book.add_contact(person2)

    def test_search_by_name(self):
        results = self.address_book.search_field("name", "John Doe")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "John Doe")

    def test_search_by_role(self):
        results = self.address_book.search_field("role", "Data Scientist")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].role, "Data Scientist")

    def test_search_by_email(self):
        results = self.address_book.search_field("email", "jane.smith@example.com")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].email, "jane.smith@example.com")

    def test_search_by_github(self):
        results = self.address_book.search_field("github", "johndoe")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].github, "johndoe")

    def test_search_by_work_area(self):
        results = self.address_book.search_field("work_area", "Data Analytics")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].work_area, "Data Analytics")

    def test_search_by_employer(self):
        results = self.address_book.search_field("employer", "ABC Inc.")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].employer, "ABC Inc.")


if __name__ == '__main__':
    unittest.main()
