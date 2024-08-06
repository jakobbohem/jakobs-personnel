
from datetime import datetime, timedelta

org_settings_file = "data/organisation_data.json"

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

def print_role_match(address_book, query, filter = []):
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

## helpers to create URLs for opening the browser for a certain user (usability)
# https://learn.microsoft.com/en-us/azure/devops/boards/queries/using-queries?view=azure-devops&tabs=browser#query-hyperlink-syntax
import source.data_manager as data_manager
data = data_manager.read_data_from_file(org_settings_file)

def open_browser(url):
    import webbrowser
    webbrowser.open(url)

def github_root():
    #todo: get base url from config.
    return data['github-root']

def issueTracker_root():
    #todo: get base url from config.
    return ['issueTracker-root']

def get_ado_items_url(person):
    # https://dev.azure.com/OrganizationName/ProjectName/_workitems?_a=query&wiql={Encoded WorkItemQueryLanguage}
    # https://dev.azure.com/fabrikam/FabrikamFiber/_workitems?_a=query&wiql=SELECT%20%5BSystem.ID%5D%2C%20%5BSystem.Title%5D%20FROM%20WorkItems%20WHERE%20%5BSystem.TeamProject%5D%3D'FabrikamFiber'%20AND%20%5BSystem.WorkItemType%5D%3D'Bug'%20AND%20%5BSystem.State%5D%3D'Active'%20AND%20%5BSystem.AreaPath%5D%3D'FabrikamFiber%5CWeb'
    
    import urllib
    query = {
        
    }

    url = f"{issueTracker_root()}/_workitems?_a=query&wiql={urllib.urlencode(query)}"
    return url

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
    
import sys
import subprocess

if sys.platform == 'win32': # (TEMP) broken code- Win memory..
    import ctypes

    def copy_to_clipboard(text):
        # Constants from the Windows API
        CF_TEXT = 1  # Clipboard format
        GMEM_DDESHARE = 0x2000  # Memory allocation flag

        if isinstance(text, list):
            # person_strings = map(str, text)
            text = '\n'.join([str(i) for i in text])
       
        # more to read up on: https://stackoverflow.com/questions/579687/how-do-i-copy-a-string-to-the-clipboard
        import tempfile # tempfile = 'clip.txt'
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(text.encode())
            tmp.close()
            cmd = 'type ' + tmp.name + '|clip'
            subprocess.check_call(cmd, shell=True)

elif sys.platform == 'darwin':
    def copy_to_clipboard(text):

        # macOS clipboard access using pbcopy
        process = subprocess.Popen(
            ['pbcopy'],
            stdin=subprocess.PIPE,
            close_fds=True
        )
        process.communicate(input=text.encode('utf-8'))

else:
    raise NotImplementedError("Clipboard operations are not supported on this platform.")

# Example usage
# copy_to_clipboard("Hello, Cross-Platform Clipboard!")
