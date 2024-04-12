
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

    # roles = set(person.role for person n address_book.contacts())
    print(f"Has role matching {query}:")
    if results:
        for person in results:
            print(f"Name: {person.name}, Role: {person.role}, gh: {person.github}, (Email: {person.email})")
        else:
            print("No matching entries found.")

        print(f"total: {len(results)}")

def get_github_prs_url(person):
    # person = results[0]
    cutoff_date = gh_timestring(daysago = 21)
    print(f"... opening github.com PRs for '{person.name}'")
    gh_query=f"is:pr+updated:>={cutoff_date}+author:{person.github}" #.replace(':', '%3A')

    url = f"https://github.com/Mojang/Spicewood/pulls?q={gh_query}"

    return url

