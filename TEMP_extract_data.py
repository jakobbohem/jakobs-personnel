import re

class Person:
    def __init__(self, name_ado_id, role, github_username, email=None):
        self.name_ado_id = name_ado_id
        self.role = role
        self.github_username = github_username
        self.email = email

    def __repr__(self):
        return f"Person(name_ado_id='{self.name_ado_id}', role='{self.role}', github_username='{self.github_username}', email='{self.email}')"

def read_markdown_file(filename):
    with open(filename, 'r') as file:
        return file.read()

# Read data from markdown file
data = read_markdown_file('employees.md')

# Split data by lines and initialize an empty list to store Person objects
lines = data.strip().split('\n')
persons = []

# Regex patterns to extract GitHub usernames, Names/ADO IDs, Roles, and Emails
github_pattern = r'\[`(.+?)`\]'
name_ado_pattern = r'\| ([^\|]+) \|'
role_pattern = r'\| ([^\|]+)  \|'
email_pattern = r'\[.+\]\(mailto:(.+)\)'

for i, line in enumerate(lines[3:], start=3):  # Skip headers
    if line.startswith('|--'):  # Skip separator line
        continue

    github_match = re.search(github_pattern, line)
    name_ado_match = re.search(name_ado_pattern, line)
    role_match = re.search(role_pattern, line)
    email_match = re.search(email_pattern, line)

    if github_match and name_ado_match and role_match:
        github_username = github_match.group(1)
        name_ado_id = name_ado_match.group(1).strip()
        role = role_match.group(1).strip()
        email = email_match.group(1) if email_match else None

        person = Person(name_ado_id, role, github_username, email)
        persons.append(person)
    else:
        print(f"Data on line {i} could not be parsed.")

# Display extracted data
for person in persons:
    print(person)
