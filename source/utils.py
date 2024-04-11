
def print_role_has(address_book, query):
    roles = set(person.role for person in address_book.contacts())
    print(f"Has role matching {query}")
    for role in roles:
        print(role)

def print_role_match(address_book, query):
    results = address_book.search_field("role", query)

    # roles = set(person.role for person n address_book.contacts())
    print(f"Has role matching {query}:")
    if results:
        for person in results:
            print(f"Name: {person.name}, Role: {person.role}, gh: {person.github}, (Email: {person.email})")
        else:
            print("No matching entries found.")

        print(f"total: {len(results)}")