import unittest
from extract_data import extract_person_data_from_tables

class TestExtractPersonData(unittest.TestCase):
    def test_extract_person_data(self):
        md_file_path = "data/employees.md"

        with open(md_file_path, "r") as md_file:
            markdown_text = md_file.read()
        
        expected_results = [
            ("johndoe", "John Doe", "Code, UX"),
            ("janedoe", "Jane Doe", "Code, Gameplay"),
            ("jakobbohem", "Jakob da Munde", "Code, Lead"),
            ("BillySprung", "Billy Kirk", "UI Script"),
            ("nela-doe", "Nela Doe", "UI Script"),
        ]
        
        persons = extract_person_data_from_tables(markdown_text)
        
        self.assertEqual(len(persons), len(expected_results))
        
        for i in range(len(persons)):
            self.assertEqual(persons[i].github, expected_results[i][0])
            self.assertEqual(persons[i].name, expected_results[i][1])
            self.assertEqual(persons[i].role, expected_results[i][2])
            self.assertIn(persons[i].employer, ["Company employees", "SPRUNG Employees"])  # Verify company name

if __name__ == '__main__':
    unittest.main()
