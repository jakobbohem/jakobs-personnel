from person import Person

class AddressBook:
    def __init__(self):
        self.persons = []

    # get/set
    def contacts(self):
        return self.persons

    def append(self, persons):
        for person in persons:
            self.add_contact(person)

    def add_contact(self, person):
        if person.email:
            if self.check_existing_email(person.email):
                print("Person with the same email already exists in database.")
                return
        elif self.check_existing_github(person.github):
            print("Person with this github-username already exists in database")

        self.persons.append(person)

    def check_existing_email(self, email):
        return any(contact.email.lower() == email.lower() for contact in self.persons if contact.email)
  
    def check_existing_github(self, github_username):
        return any(contact.github.lower() == github_username.lower() for contact in self.persons)

    # search methods
    def search_field(self, field, value):
        results = [contact for contact in self.persons if contact.match_field(field, value)]
        return results

    # TODO: smarter 'searchable' containers for the Person:s
    def search_old(self, *search_tokens):
            results = []
            for person in self.persons:
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
    
    def search(self, *search_tokens, case_insensitive=True):
        matching_persons = []
            
        # Convert search tokens to lowercase if case_insensitive is True
        if case_insensitive:
            search_tokens = [token.lower() for token in search_tokens]

        for person in self.persons:
            matched_fields = []
            person_fields = {
                'first_name': person.name.split(' ')[0] if ' ' in person.name else person.name,
                'last_name': person.name.split(' ')[1] if ' ' in person.name else '',
                'email': person.email if person.email else None,
                'github': person.github,
                # 'role': person.role,
                'employer': person.employer
            }

            if case_insensitive:
                person_fields = {key: (value.lower() if type(value) == str else None) for key, value in person_fields.items()}
            
            ## IT FAILS BECAUSE THE 2nd SEARCH TOKEN (w) matches 2+ fields which are then counted against the total number of required TOKENS
            ## 'John' is never matched for e.g. 'James White'

            # Check if all search tokens are present in at least one field
            if all(any(token in field for field in person_fields.values()) for token in search_tokens):
                matching_persons.append(person)

            # Loop through all fields and check for token match
            # for field in person_fields.values():
            #     if field and any(token in field for token in search_tokens):
            #         matched_fields.append(True)

            # if len(matched_fields) == len(search_tokens):
            #     matching_persons.append(person)
                
        return matching_persons
    