# System
import system as syt

if __name__ == "__main__": syt.setup_logger()

# Main Menu
from navigation.M1_quick_data_menu import quick_data_menu
from navigation.M2_reports_menu import make_report_menu
from navigation.M3_update_database_menu import database_update_menu
from navigation.M4_system_menu import system_menu

# Price capture
from data.update_ternary import daily_data


def main_menu():
    def daily_update():
        daily_data.price_capture_menu()

    def quick_data():
        quick_data_menu()

    def make_reports():
        make_report_menu()

    def update_database():
        database_update_menu()  # Mostly done

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





if __name__ == "__main__":
    main_menu()