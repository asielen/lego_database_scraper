# Internal
from database.info import database_info
from data.update_ternary import daily_data
import system as syt
if __name__ == "__main__": syt.setup_logger()

def main():
    """
    # Todo: make sure this runs the right update function - update inventories between the time frame
    @return:
    """
    print("Please enter the start and end years you would like to update. "
          "If left blank, it will capture everything before/after the date")
    start_year = input("What year would you like to start with? ")
    end_year = input("What year would you like to end with? ")

    database_year_range = database_info.get_set_year_range()
    if start_year is "": start_year = database_year_range[0]
    if end_year is "": end_year = database_year_range[1]
    proceed = input(
        "Would you like to update prices for all sets between {0} and {1}? Y/N?".format(start_year, end_year))
    if proceed == "y" or proceed == "Y":
        set_list = database_info.get_sets_between_years(start_year, end_year)

        daily_data.get_all_daily_set_data(set_list)


if __name__ == "__main__":
    main()
