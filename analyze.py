#! /usr/bin/env python

import argparse
from person import Person
from address_book import AddressBook
from data_accessor import DataAccessor

from source.grapher.graph_tool import GraphTool
from source.ghcli import GHCli
from source.utils import *
from enum import Enum

import sqlite3

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
    print("list w/o filter from database?")
    if args.graph:
        graphtool = GraphTool()
        graphtool.plot_persons(column_name=args.graph)

def ListTeams(address_book, args):
    print("todo: impl ListTeams")

def ListRoles(address_book, args):
    # todo: add 
    print_role_match(address_book, "code")
    print_role_match(address_book, "dev")

def ListGitCommits(address_book, args):
    # todo: add 'complexity' of PR count also
    print("list GIT commits.. <-this")
    if not args.filter:
        print("no filters/ set for gh, aborting")
        return
    cli = GHCli(args.repository_home)

    # set this here? -- write to json settings file(s)
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
        world_devs = ['d11dbardsley', 'd11jameswood', 'd11lgraydon', 'petter-holmberg' 
                      ,'YiPeiTu-Netlight', 'jdarnald', 'veblmojang', 'JaredChickoreeD11'
                      ,'GabrielM-D11']
        graphtool.plot_github(blob=json_data, userfilter=world_devs)

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
    parser.add_argument("--roles", action="store_true", help="List all available roles")
    parser.add_argument("--teams", action="store_true", help="List all available teams")
    parser.add_argument("-g", "--graph", default="", help="Graph the split of personnel data along some vector ('craft', 'team', 'organisation')")
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