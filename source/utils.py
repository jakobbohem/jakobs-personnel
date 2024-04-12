
from datetime import datetime, timedelta

class TimeUtil:
    def __init__(self, daysago = 90):
        self.daysago = daysago
        self.timeago = datetime.now() - timedelta(days=daysago)

    def set_days_ago(self, daysago):
        self.daysago = daysago

    def gh_timestring(self, daysago = 0):
        import time
        daysago = daysago and daysago or self.daysago
        return time.strftime('%Y-%m-%d', time.localtime(time.time()-3600*24*daysago))

    def compare_time(self, timestring, days):
        # check if greater than
        tformat = '%Y-%m-%dT%H:%M:%SZ'

        ## optimise/cache?
        return datetime.strptime(timestring,tformat) >= self.timeago

def print_role_has(address_book, query):
    roles = set(person.role for person in address_book.contacts())
    print(f"Has role matching {query}")
    for role in roles:
        print(role)

def print_role_match(address_book, query):
    results = address_book.search_field("role", query)
    print(f"Has role matching {query}:")
    print_display_persons(results)

def print_display_persons(persons):
    # roles = set(person.role for person n address_book.contacts())
    if persons:
        for person in persons:
            print(f"Name: {person.name}, Role: {person.role}, gh: {person.github}, (Email: {person.email})")
        else:
            print("No matching entries found.")

        print(f"total: {len(persons)}")

def github_root():
    #todo: get base url from config.
    return 'https://github.com/Mojang/Spicewood'

def get_github_prs_url(person):
    # person = results[0]
    tu = TimeUtil()
    cutoff_date = tu.gh_timestring(daysago = 21)
    print(f"... opening github.com PRs for '{person.name}'")
    gh_query=f"is:pr+updated:>={cutoff_date}+author:{person.github}" #.replace(':', '%3A')
    url = f"{github_root()}/pulls?q={gh_query}"

    return url

class WorkItemIntegration:
    def __init__(self):
        # support fot github issues?
        self.provider = "ado"

    def get_workitem_tasks_url(self, person):
        # append query to base URL (build URL)
        return issue_tracker_base()
    
    def issue_tracker_base(self):
        # add nicer switcher w Enum?
        if self.provider == "ado":
            return 'https://dev.azure.com/dev-mc/Spicewood/_queries/query-edit/?newQuery=true&parentId=e82cdffb-f816-470b-98a7-f131723bf786'
        return ""