# System
import system as syt

if __name__ == "__main__": syt.setup_logger()

# Main Menu
from navigation.M1_quick_data_menu import quick_data_menu
from navigation.M2_reports_menu import make_report_menu
from navigation.M3_update_database_menu import database_update_menu
from navigation.M4_system_menu import system_menu

# Price capture
from database.info import database_info
from data.update_ternary import daily_data


def main_menu():
    def daily_update():
        price_capture_menu()

    def quick_data():
        quick_data_menu()

    def make_reports():
        make_report_menu()  # Todo

    def update_database():
        database_update_menu()  # Todo

    def system():
        system_menu()  # Todo

    options = (
        ("Run Daily Update", daily_update),
        ("Quick Data", quick_data),
        ("Make Reports", make_reports),
        ("Update Database", update_database),
        ("System", system)
    )
    syt.Menu(name="- Lego Brick Evaluator -", choices=options, quit_tag="Exit").run()


def price_capture_menu():
    # Todo, should this be in this file?
    # Todo: make sure this runs the right update function - update inventories between the time frame

    print("Please enter the start and end years you would like to update. "
          "If left blank, it will capture everything before/after the date")
    start_year = input("What year would you like to start with? ")
    end_year = input("What year would you like to end with? ")

    database_year_range = database_info.get_set_year_range()
    if start_year is "": start_year = database_year_range[0]
    if end_year is "": end_year = database_year_range[1]
    proceed = input(
        "Would you like to update get_prices for all sets between {0} and {1}? Y/N?".format(start_year, end_year))
    if proceed == "y" or proceed == "Y":
        set_list = database_info.get_sets_between_years(start_year, end_year)
        daily_data.get_all_daily_set_data(set_list)


if __name__ == "__main__":
    main_menu()