#! /usr/bin/env python

import argparse
from person import Person
from address_book import AddressBook
from data_accessor import DataAccessor

from source.grapher.graph_tool import GraphTool
from source.ghcli import GHCliHelper
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
    # if args.graph:
    #     graphtool = GraphTool()
    #     graphtool.plot_data(args.filter)

def ListTeams(address_book, args):
    print("todo: impl ListTeams")

def ListRoles(address_book, args):
    # todo: add 
    print_role_match(address_book, "code")
    print_role_match(address_book, "dev")

def ListGitCommits(address_book, args):
    print("list GIT commits.. <-this")

# Map actions to their corresponding functions
actions = {
    Action.PERSONNEL: ListPersonnel,
    Action.TEAMS: ListTeams,
    Action.ROLES: ListRoles,
    Action.GITHUB: ListGitCommits,
}

def main():
    parser = argparse.ArgumentParser(description="Address Book CLI")
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