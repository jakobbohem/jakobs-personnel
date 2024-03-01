import unittest
import source.test_helpers
from address_book import AddressBook
from person import Person

class TestAddressBookSearch(unittest.TestCase):
    def setUp(self):
        # Create an AddressBook instance and add some sample persons
        self.address_book = source.test_helpers.get_test_AddressBook()

    def test_search_text_string(self):
        # Search for part of a last name "Sm"
        print("Searching for 'Alice Smith'")
        search_results = self.address_book.search("Alice Smith")
        self.assertEqual(len(search_results), 1)
        self.assertEqual(search_results[0].github, "alice1")


if __name__ == '__main__':
    unittest.main()
