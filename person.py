class Person:
    def __init__(self, name, role, email, github, work_area, employer, team, craft):
        self.name = name
        self.role = role
        self.email = email
        self.github = github
        self.work_area = work_area
        self.employer = employer
        self.team = team
        self.craft = craft
        # self.active = True # make sure to separate current and previous memberse (no team == not active)

    def is_active(self):
        return not not self.team

    def match_field(self, field, value):
        return value.lower() in str(getattr(self, field)).lower()

    def match_field_exact(self, field, value):
        return str(getattr(self, field)).lower() == value.lower()
    
    def filter_by(self, field, options):
        attribute_value = str(getattr(self, field)).lower()
        return any(attribute_value == option.lower() for option in options)
    
    def __str__(self):
        email = f" ({self.email})" if self.email else ""
        return f"{self.name}: [{self.github}]{email} at {self.employer} | {self.role} | {self.team} | {self.craft}"