from person import Person

class AddressBook:
    def __init__(self):
        self.contacts = []

    def add_contact(self, person):
        self.contacts.append(person)

    def search(self, field, value):
        results = [contact for contact in self.contacts if contact.match_field(field, value)]
        return results
