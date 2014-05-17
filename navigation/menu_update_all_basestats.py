__author__ = 'andrew.sielen'

import navigation.menu

from database_management import database_info
from get_actions import get_sets_basestats as get_basestats

def main():
    options = {}
    options['1'] = "Update In Database", update_in_database
    options['2'] = "Update from file", update_from_file
    options['3'] = "Update Scrape", update_from_scrape
    options['9'] = "Back", navigation.menu.back

    while True:
        result = navigation.menu.options_menu(options)
        if result is 'back':
            break


def update_in_database():
    print("Please enter the start and end years you would like to update. "
          "If left blank, it will capture everything before/after the date")
    start_year = input("What year would you like to start with? ")
    end_year = input("What year would you like to start with? ")

    database_year_range = database_info.get_set_year_range()
    if start_year is "": start_year = database_year_range[0]
    if end_year is "": end_year = database_year_range[1]
    proceed = input("Would you like to update all sets between {0} and {1}? Y/N?".format(start_year, end_year))
    if proceed == "y" or proceed == "Y":
        set_list = database_info.get_sets_between_years(start_year, end_year)

        get_basestats.get_all_basestats(set_list)


def update_from_file():
    """
    Takes a standard Sets.txt file from bricklink and parses it and updates based on it
    @return:
    """
    with open("Sets.txt", encoding='utf-8', errors='ignore') as f:
        set_list_raw = f.readlines()
        set_list_raw = set_list_raw[3:]
        set_list = [set.split("\t")[-2].strip() for set in set_list_raw]

    get_basestats.get_all_basestats(set_list)



def update_from_scrape():
    pass