from person import Person
from source.utils import *

class AddressBook:
    def __init__(self):
        self.persons = []
        self.case_insensitive_search = True

    # get/set
    def contacts(self):
        return self.persons

    def append(self, persons):
        for person in persons:
            self.add_contact(person)

    def add_contact(self, person):
        if person.email:
            if self.check_existing_email(person.email):
                print("Person with the same email already exists in database: {}".format(person.email))
                return
        elif self.check_existing_github(person.github):
            print("Person with this github-username already exists in database: {}".format(person.github))

        self.persons.append(person)

    def check_existing_email(self, email):
        return any(contact.email.lower() == email.lower() for contact in self.persons if contact.email)
  
    def check_existing_github(self, github_username):
        return any(contact.github.lower() == github_username.lower() for contact in self.persons)

    # search methods
    def search_field(self, field, value):
        results = [contact for contact in self.persons if contact.match_field(field, value)]
        return results

    def get_github_prs_url(self, search_tokens):
        # import time
        results = self.search(*search_tokens)
        # person = results[0]
        # daysago = 21
        # cutoff_date = time.strftime('%Y-%m-%d', time.localtime(time.time()-3600*24*daysago))
        # print(f"... opening github.com PRs for '{person.name}'")
        # gh_query=f"is:pr+updated:>={cutoff_date}+author:{person.github}" #.replace(':', '%3A')
        # url = f"https://github.com/Mojang/Spicewood/pulls?q={gh_query}"
        return get_github_prs_url(results[0])
    
    def set_search_params(self, case_insensitive):
        self.case_insensitive_search = case_insensitive

    def search(self, *search_tokens):
        # if it's a single string containing spaces, assume to split it
        if len(search_tokens) == 1 and type(search_tokens[0]) is str:
            search_tokens = search_tokens[0].split(" ")
        matching_persons = []
            
        # Convert search tokens to lowercase if case_insensitive is True
        if self.case_insensitive_search:
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

            if self.case_insensitive_search:
                person_fields = {key: (value.lower() if type(value) == str else None) for key, value in person_fields.items()}
            
            # Check if all search tokens are present in at least one field
            if all(any(token in field for field in person_fields.values() if field is not None) for token in search_tokens):
                matching_persons.append(person)
                
        return matching_persons
    