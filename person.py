class Person:
    def __init__(self, name, role, email, github, work_area, employer, team, craft, alumn = False):
        self.name = name
        self.role = role
        self.email = email or ''
        self.github = github
        self.work_area = work_area
        self.employer = employer
        self.team = team
        self.craft = craft
        self.alumn = alumn
        # self.active = True # make sure to separate current and previous memberse (no team == not active)

    def is_active(self):
        return not self.alumn

    def match_field(self, field, value):
        return value.lower() in str(getattr(self, field)).lower()

    def match_field_exact(self, field, value):
        return str(getattr(self, field)).lower() == value.lower()
    
    # default filter, hold:
    def filter_by(self, field, options):
        if not hasattr(self, field): return False
        attribute_value = str(getattr(self, field)).lower()
        return any(attribute_value == option.lower() for option in options)
    
    ## outputting to console:
    def format_str(self, formatstring):
        """Format the object based on the given format string."""
        if not formatstring: return self
        try:
            return formatstring.format(**vars(self))
        except KeyError as e:
            raise ValueError(f"Invalid format string: missing attribute {e}")

    def __str__(self):
        email = f" ({self.email})" if self.email else ""
        alumn = self.alumn and "| [alumn]" or ""
        return f"{self.name}: [{self.github}]{email} at {self.employer} | {self.role} | {self.team} | {self.craft}{alumn}"