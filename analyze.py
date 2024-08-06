#! /usr/bin/env python

import argparse
from person import Person
from address_book import AddressBook
from data_accessor import DataAccessor

from source.grapher.graph_tool import GraphTool
from source.ghcli import GHCli
from source.utils import *
from source.org_utils import get_teams
from enum import Enum


# Define an Enum for actions
class Action(Enum):
    PERSONNEL = 'personnel'
    TEAMS = 'teams'
    ROLES = 'roles'
    GITHUB = 'github'
    # ACTION5 = 'install'
    # ACTION6 = 'clean'
    # ACTION7 = 'run'

def ListPersonnel(address_book, args):
    print("list people on team '{}'".format(args.filter))

    print(" -- WARNING! currently only processes 'craft==code'/ developers --")
    # if args.team:
    persons = address_book.filter_field(team=get_teams(args.filter))
    # persons = ##[p for p in address_book.filter_field("team", get_teams(args.filter))]
    for index, p in enumerate(persons, start=1):
        print(f"{index} {p}")

    if args.graph:
        graphtool = GraphTool()
        graphtool.plot_persons(column_name=args.graph)

def ListTeams(address_book, args):
    results = address_book.filter_field(team=args.team)
    print("Team members {}".format(args.team))
    print_display_persons(results)

def ListRoles(address_book, args):
    print_role_match(address_book, args.craft)
    # print_role_match(address_book, "dev")

def ListGitCommits(address_book, args):
    # todo: consider allowing filter by user/username etc
    # todo: if no --graph option, get human readable string output instead of json.. 
    if not args.filter:
        print("no filters/ set for gh, aborting")
        return
    
    cli = GHCli(args.repository_home)

    # set this here? -- write to json settings file(s)
    ## TODO: search filtering (w date) can be used for under 1000 return items,
    ## add auto-switching method based on requirements..
    args.json = True
    args.filter_main = False
    args.limit = 2000
    json_data = cli.ListPR(args=args)

    for index, item in enumerate(json_data):
        print("[{}] - {}:{} ({})".format(
            item['author']['login']
            ,item['number']
            ,item['title'][:25]
            , item['createdAt']
            ))
        if index + 1 >= 12: break # don't spam the log

    if args.graph:
        graphtool = GraphTool()
        division_name = args.filter and args.filter or "world"
        # better label? "{}\n{}".format(p.github, p.name[:15]
        persons = [p.github for p in address_book.filter_field(team=get_teams(division_name))]
        graphtool.plot_github(blob=json_data, userfilter=persons)

# Map actions to their corresponding functions
actions = {
    Action.PERSONNEL: ListPersonnel,
    Action.TEAMS: ListTeams,
    Action.ROLES: ListRoles,
    Action.GITHUB: ListGitCommits,
}

def main():
    parser = argparse.ArgumentParser(description="Address Book CLI")
    parser.add_argument("-rh", "--repository-home", default="e:/projects/Spicewood", help="The repository to query for github actions")
    parser.add_argument("--craft", default="", help="Filter input by roles variable (e.g. 'code, art, production')")
    parser.add_argument("--teams", default="", help="Filter input by teams (also checks for mission, e.g. 'world', 'gameplay', or 'tech-online')")
    parser.add_argument("-g", "--graph", default="", help="Graph the split of personnel data along some vector ('craft', 'team', 'organisation')")
    parser.add_argument("-m", "--email", action="store_true", help="get a list of e-mail addresses to paste into Outlook, for quick e-mail invite setup!")
    parser.add_argument("action", nargs="?", type=Action, choices=list(Action), help="action for desired Hermes artifact (for UE, or UE-xsx, UE-switch etc)\nassociated symbols are handled as 1 artifact")
    # // todo: add comma separated list filer?
    parser.add_argument("filter", nargs="?", default="", help="filter output by e.g. Scrum team, role or something else")
    
    args = parser.parse_args()

    # init data
    db = DataAccessor('data/address_book.db')
    address_book = db.load_from_database()

    # call the chosen action
    actions[args.action](address_book, args)


if __name__ == '__main__':
    main()