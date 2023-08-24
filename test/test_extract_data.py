import unittest
from extract_data import extract_person_data

class TestExtractPersonData(unittest.TestCase):
    def test_extract_person_data(self):
        table_text = """
        | github handle | Name/ADO | Role |
        |--|--|--|
        | [`johndoe`](https://github.com/johndoe) | @<John Doe>  | Code, UX |
        | [`janedoe`](https://github.com/janedoe) | Jane Doe  | Code, Gameplay |
        | [`jakobbohem`](https://github.com/jakobbohem) | [Jakob da Munde](mailto:jakob@munde.com)  | Code, Lead |
        """
        
        company_name = "Company ABC"
        
        expected_results = [
            ("johndoe", "John Doe", "Code, UX"),
            ("janedoe", "Jane Doe", "Code, Gameplay"),
            ("jakobbohem", "Jakob da Munde", "Code, Lead"),
        ]
        
        persons = extract_person_data(table_text, company_name)
        
        self.assertEqual(len(persons), len(expected_results))
        
        for i in range(len(persons)):
            self.assertEqual(persons[i].github_username, expected_results[i][0])
            self.assertEqual(persons[i].name, expected_results[i][1])
            self.assertEqual(persons[i].role, expected_results[i][2])
            self.assertEqual(persons[i].company, company_name)

if __name__ == '__main__':
    unittest.main()
