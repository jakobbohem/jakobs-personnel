from address_book import AddressBook
from person import Person

def get_test_AddressBook():
    address_book = AddressBook()
    persons = [
        Person("John Doe", "Developer", "john.doe@example.com", "john", "", "Developer Co", None, None),
        Person("Alice Smith", "Designer", "alice.smith@example.com", "alice1", "", "Design Co.", "TeamA", "Design"),
        Person("Bob Johnson", "Manager", "bob.johnson@example.com", "bob_git", "", "Management Corp.", "TeamA", "Management"),
        Person("Eve Doe", "Tester", "eve.doe@example.com", "eve", "", "Testing Ltd.", "TeamB", "QA"),
    ]
    for person in persons:
        address_book.add_contact(person)

    return address_book