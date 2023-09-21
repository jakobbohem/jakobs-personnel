from person import Person
from address_book import AddressBook

# Example usage
address_book = AddressBook()

# Adding contacts
person1 = Person("John Doe", "Software Engineer", "john.doe@example.com", "johndoe", "Machine Learning", "ABC Inc.")
address_book.add_contact(person1)

person2 = Person("Jane Smith", "Data Scientist", "jane.smith@example.com", "janesmith", "Data Analytics", "XYZ Corp.")
address_book.add_contact(person2)

# Searching by name
name_results = address_book.search("name", "John Doe")
print("Search by name: ")
for person in name_results:
    print(f"Name: {person.name}, Role: {person.role}, Email: {person.email}")

# Searching by role
role_results = address_book.search("role", "Data Scientist")
print("Search by role: ")
for person in role_results:
    print(f"Name: {person.name}, Role: {person.role}, Email: {person.email}")

# Searching by email
email_results = address_book.search("email", "jane.smith@example.com")
print("Search by email: ")
for person in email_results:
    print(f"Name: {person.name}, Role: {person.role}, Email: {person.email}")

# Searching by GitHub username
github_results = address_book.search("github", "johndoe")
print("Search by GitHub username: ")
for person in github_results:
    print(f"Name: {person.name}, Role: {person.role}, Email: {person.email}")

# Searching by work area
work_area_results = address_book.search("work_area", "Data Analytics")
print("Search by work area: ")
for person in work_area_results:
    print(f"Name: {person.name}, Role: {person.role}, Email: {person.email}")

# Searching by employer
employer_results = address_book.search("employer", "ABC Inc.")
print("Search by employer: ")
for person in employer_results:
    print(f"Name: {person.name}, Role: {person.role}, Email: {person.email}")
