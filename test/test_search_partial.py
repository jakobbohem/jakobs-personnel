import unittest
from address_book import AddressBook
from person import Person

class TestAddressBookSearch(unittest.TestCase):
    def setUp(self):
        # Create an AddressBook instance and add some sample persons
        self.address_book = AddressBook()
        persons = [
            Person("John Doe", "Developer", "john.doe@example.com", "john", "", "Developer Co", None, None),
            Person("Alice Smith", "Designer", "alice.smith@example.com", "alice1", "", "Design Co.", "TeamA", "Design"),
            Person("Bob Johnson", "Manager", "bob.johnson@example.com", "bob_git", "", "Management Corp.", "TeamA", "Management"),
            Person("Eve Doe", "Tester", "eve.doe@example.com", "eve", "", "Testing Ltd.", "TeamB", "QA"),
        ]
        for person in persons:
            self.address_book.add_contact(person)

    def test_search_partial_last_name(self):
        # Search for part of a last name "Sm"
        search_results = self.address_book.search("Sm")
        self.assertEqual(len(search_results), 1)
        self.assertEqual(search_results[0].github, "alice1")

    def test_search_partial_email(self):
        # Search for part of an email address "example"
        search_results = self.address_book.search("example")
        self.assertEqual(len(search_results), 4)
        self.assertSetEqual({person.github for person in search_results}, {"john", "alice1", "bob_git", "eve"})

if __name__ == '__main__':
    unittest.main()
