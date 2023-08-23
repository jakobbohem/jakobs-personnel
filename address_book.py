from person import Person

class AddressBook:
    def __init__(self):
        self.contacts = []

    def add_contact(self, person):
        if self.check_existing_email(person.email):
            print("Person with the same email already exists.")
            return

        self.contacts.append(person)

    def check_existing_email(self, email):
        return any(contact.email.lower() == email.lower() for contact in self.contacts)


    def search(self, field, value):
        results = [contact for contact in self.contacts if contact.match_field(field, value)]
        return results
