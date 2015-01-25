# Internal
import navigation.menu
from data.bricklink.bricklink_api import pull_set_catalog
from data.update_secondary import add_inventories_database as secondary
from data.update_secondary import add_sets_database as add_sets
from database.info import database_info


def main():
    options = {}
    options['1'] = "Update inventories in Database", update_in_database  # Working 2014-10-5
    options['2'] = "UPDATE from API get new sets AND UPDATE", update_from_api  # Working 2014-10-5
    options['9'] = "Back", navigation.menu.back

    while True:
        result = navigation.menu.options_menu(options)
        if result is 'back':
            break


def update_in_database():
    print("Please enter the start and end years you would like to update. "
          "If left blank, it will capture everything before/after the date")
    start_year = input("What year would you like to start with? ")
    end_year = input("What year would you like to end with? ")

    database_year_range = database_info.get_set_year_range()
    if start_year is "": start_year = database_year_range[0]
    if end_year is "": end_year = database_year_range[1]
    proceed = input("Would you like to update all sets between {0} and {1}? Y/N? ".format(start_year, end_year))
    if proceed == "y" or proceed == "Y":
        set_list = database_info.get_sets_between_years(start_year, end_year)

        secondary.add_bl_inventories_to_database(update=0)
        secondary.add_re_inventories_to_database(update=0)


def update_from_api():
    """
    Update the database from an public_api call to bricklink and parses it and updates based on it
    ['Category ID', 'Category Name', 'Number', 'Name', 'Year Released', 'Weight (in Grams)', 'Dimensions']
    And then update all inventories
    @return:
    """
    set_list = pull_set_catalog()
    add_sets.add_sets_to_database(set_list, id_col=2, update=0)
    secondary.add_bl_inventories_to_database(update=0)
    secondary.add_re_inventories_to_database(update=0)


# def update_from_file():
# """
# Takes a standard Sets.txt file from bricklink and parses it and updates based on it
# @return:
# """
# with open("Sets.txt", encoding='utf-8', errors='ignore') as f:
# set_list_raw = f.readlines()
#         set_list_raw = set_list_raw[3:]
#         set_list = [set.split("\t")[-2].strip().lower() for set in set_list_raw]
#
#     basics.get_all_basestats(set_list)

if __name__ == "__main__":
    main()

