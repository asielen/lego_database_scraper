__author__ = 'andrew.sielen'

import os

from system import logger

if __name__ == "__main__": logger.setup()
from database.database import database
import navigation.menu as menu
import navigation.menu_daily_price_capture as DPC
import navigation.menu_update_all_basestats as UAB
import navigation.menu_update_set as US
import navigation.menu_get_set_info as GSI
import navigation.menu_system as SYS
import navigation.menu_update_all_inventories as INV


def run_get_sets():
    return UAB.main()


def run_get_prices():
    return DPC.main()


def run_update_set():
    return US.main()


def run_get_set_info():
    return GSI.main()


def run_system():
    return SYS.main()


def run_get_inv():
    return INV.main()


def validate_database():
    if os.path.isfile(database):
        logger.info("Database Found")

    else:
        logger.warning("No Database Found. Please locate it or create one in the system menu")


def main():
    """
    Main launch menu
    @return:
    """

    validate_database()

    logger.info("Running Main")
    options = {}

    options['1'] = "Run Daily Price Capture", run_get_prices
    options['2'] = "Run Total Basestats refresh", run_get_sets
    options['3'] = "Run Inventories Refresh", run_get_inv
    options['4'] = "Update set", run_update_set
    options['5'] = "Get Set Info", run_get_set_info
    options['6'] = "System", run_system
    options['9'] = "Quit", menu.quit

    while True:
        result = menu.options_menu(options)
        if result is 'kill':
            exit()


main()
