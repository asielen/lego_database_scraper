__author__ = 'andrew.sielen'

# External
import os

# Internal
import system as syt
if __name__ == "__main__": syt.setup_logger()
from database import database as db
import navigation.menu_daily_price_capture as DPC
import navigation.menu_update_all_basestats as UAB
import navigation.menu_update_set as US
import navigation.menu_build_reports as GSI
import navigation.menu_system as SYS
import navigation.menu_update_all_inventories as INV

def run_get_sets():
    return UAB.main()


def run_get_prices():
    return DPC.price_capture_menu()


def run_update_set():
    return US.main()


def run_get_set_info():
    return GSI.report_menu()


def run_system():
    return SYS.main()


def run_get_inv():
    return INV.main()


def validate_database():
    if os.path.isfile(db):
        syt.log_info("Database Found")

    else:
        syt.log_warning("No Database Found. Please locate it or create one in the system menu")


def main_menu():
    """
    Main launch menu
    @return:
    """

    validate_database()

    syt.log_info("Running Main")

    options = (
        ("Run Daily Price Capture", run_get_prices),
        ("Run Total Basestats refresh", run_get_sets),
        ("Run Inventories Refresh", run_get_inv),
        ("Update set", run_update_set),
        ("Get Reports", run_get_set_info),
        ("System", run_system)
    )
    syt.Menu(name="- Lego Brick Evaluator -", choices=options, quit_tag=True).run()


if __name__ == "__main__":
    main_menu()
