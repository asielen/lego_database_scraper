# Internal
import system as syt
from data.bricklink.bricklink_api import pull_set_catalog
from data import update_secondary as secondary
from database.info import database_info


def main():
    options = (
        ("Update In Database", update_in_database),
        ("Update from API", update_from_api)
    )

    syt.Menu("– Update Basestats –", choices=options).run()

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

        secondary.add_sets_to_database(set_list, update=1)


def update_from_api():
    """
    Update the database from an public_api call to bricklink and parses it and updates based on it
    ['Category ID', 'Category Name', 'Number', 'Name', 'Year Released', 'Weight (in Grams)', 'Dimensions']
    @return:
    """
    set_list = pull_set_catalog()
    proceed = input("What Level of Update (-1 no check, 0 check 90 days, 1 check base data, 2 update all)? ")
    if proceed not in ('-1', '0', '1', '2'):
        proceed = 0
    else:
        proceed = int(proceed)
    secondary.add_sets_to_database(set_list, id_col=2, update=proceed)


# def update_from_file():
# """
# Takes a standard Sets.txt file from bricklink and parses it and updates based on it
# @return:
# """
# with open("Sets.txt", encoding='utf-8', errors='ignore') as f:
# set_list_raw = f.readlines()
#         set_list_raw = set_list_raw[3:]
# set_list = [_set.split("\t")[-2].strip().lower() for _set in set_list_raw]
#
#     basics.get_all_basestats(set_list)

if __name__ == "__main__":
    main()

