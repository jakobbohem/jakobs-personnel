class Person:
    def __init__(self, name, role, email, github, work_area, employer):
        self.name = name
        self.role = role
        self.email = email
        self.github = github
        self.work_area = work_area
        self.employer = employer

    def match_field(self, field, value):
        return str(getattr(self, field)).lower() == value.lower()