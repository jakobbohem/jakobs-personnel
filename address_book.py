from person import Person

class AddressBook:
    def __init__(self):
        self.contacts = []

    def append(self, contacts):
        for person in contacts:
            self.add_contact(person)

    def add_contact(self, person):
        if person.email:
            if self.check_existing_email(person.email):
                print("Person with the same email already exists in database.")
                return
        elif self.check_existing_github(person.github):
            print("Person with this github-username already exists in database")

        self.contacts.append(person)

    def check_existing_email(self, email):
        return any(contact.email.lower() == email.lower() for contact in self.contacts if contact.email)
  
    def check_existing_github(self, github_username):
        return any(contact.github.lower() == github_username.lower() for contact in self.contacts)

    def search_field(self, field, value):
        results = [contact for contact in self.contacts if contact.match_field(field, value)]
        return results

    # TODO: smarter 'searchable' containers for the Person:s
    def search(self, *search_tokens):
            results = []
            for person in self.contacts:
                match = True
                for token in search_tokens:
                    token_lower = token.lower()
                    if (token_lower not in person.name.lower() and
                        (person.email is None or token_lower not in person.email.lower()) and
                        token_lower not in person.github.lower() and
                        token_lower not in person.role.lower() and
                        token_lower not in person.employer.lower()):
                        match = False
                        break
                if match:
                    results.append(person)
            return results