import subprocess
from source.utils import TimeUtil
from pathlib import Path
import json

class GHCli:
    def __init__(self, repository_home):
        print("init GHCli")
        self.repo = repository_home
        # self.gh = Path()
        self.gh = "gh" # assumes on PATH

# Specify one or more comma-separated fields for `--json`:
# (get via `gh pr list --json` or see docs/notes_on_gitcli.md for options)
    def ListPRLarge(self, args, author=None):
         # GitHub REST API endpoint
        url = "https://api.github.com/search/issues"
        tu = TimeUtil(daysago=args.daysago)
        start_date = tu.gh_timestring()
        # Parameters for the search query
        params = {
            "q": "is:pr is:merged merged:>=" + start_date,
            "sort": "updated",
            "order": "asc",
            "per_page": 100
        }

        # Fetch data from GitHub API
        while True:
            response = requests.get(url, params=params, headers={"Authorization": "Bearer " + os.environ.get("GITHUB_TOKEN")})
            response.raise_for_status()
            data = response.json()

            # Extract relevant information from the response
            for item in data.get("items", []):
                if item.get("updated_at") >= start_date:
                    merged_prs.append(item)

            # Check if there are more pages
            if "next" in response.links:
                url = response.links["next"]["url"]
            else:
                break

        return merged_prs

        command = 'gh api -X GET "search/issues?q=is:pr is:merged merged:>=2020-01-01 sort:updated-asc" --paginate'
        # | jq '.items[] | select(.updated_at >= "2020-01-01T00:00:00Z")''

    def ListPR(self, args, author=None):
        limit = args.limit and args.limit or 50 # needs to be really high if it ALL the PR in a date range.
        daysago = 90
        tu = TimeUtil(daysago)

        ## NOTE: filtering using the github 'search' API limits output to max 1000 entries!
        ## either --search, or --label options will invoke this limit!
        # see https://github.com/cli/cli/discussions/3836
        gh_query = f'"updated:>={tu.gh_timestring()}"'
        if args.filter_main:
            gh_query += " base:main"

        # consider what options should be pre-defined here
        command = """{gh} pr list --author={author} --state merged 
            --base main 
            """.format(gh=self.gh, author=author)

        ## Try it with less than 1200
        # ADD? "--search {gh_query} " ## -- note limit (see above)
        filter = ""
        if args.json:
            filter = " --json number,title,createdAt,author,mergedAt,mergedBy,additions"
        if author:
            filter += " --author={author}"

        command = f"{self.gh} pr list --state merged --limit {limit} {filter}"
        # subprocess.call(command, cwd=self.repo)
        out = subprocess.run(command, cwd=self.repo, capture_output=True)
        blob = json.loads(out.stdout)

        # filtering after is slower, but works!
        new_items = [item for item in blob 
                          if tu.compare_time(item['createdAt'], daysago)]

        isMax = limit==len(new_items) and " MAX::LIMIT" or ""
        print("Json entries: {}{}".format(
        len(new_items)
        , isMax))
        
        return new_items
    # gh pr list --state merged --limit 25  --json number,title,createdAt,author --jq .number

    def GetPRData(self, authorList):
        print("todo, get all PR data for a set of contributors")

    