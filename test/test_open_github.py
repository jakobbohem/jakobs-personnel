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

    def test_search_github_user(self):
        # Search for part of an email address "example"
        search_results = self.address_book.search("Alice", "S")
        self.assertEqual(search_results[0].github, "alice1")

    def test_github_url_format(self):
        # Search for part of a last name "Sm"
        github_user = self.address_book.search("Alice", "S")[0].github
        git_url = self.address_book.get_github_prs_url("Alice S")
        self.assertRegex(git_url, r'^(https:\/\/[\w]+\.[\w]{2,3}\/Mojang\/Spicewood\/pulls\/?\?q=)(.+)')
        self.assertTrue(github_user in git_url)



if __name__ == '__main__':
    unittest.main()

