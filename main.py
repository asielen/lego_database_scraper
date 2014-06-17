from system import setup_logging as sys

__author__ = 'andrew.sielen'

import logging

import navigation.menu as menu
import navigation.menu_daily_price_capture as DPC
import navigation.menu_update_all_basestats as UAB
import navigation.menu_update_set as US
import navigation.menu_get_set_info as GSI
import navigation.menu_system as SYS


def run_get_sets():
    return UAB.main()


def run_get_prices():
    return DPC.main()


def run_updat_set():
    return US.main()


def run_get_set_info():
    return GSI.main()


def run_system():
    return SYS.main()


def main():
    """
    Main launch menu
    @return:
    """

    sys.setup_logging()
    logging.info("Running Main")
    options = {}

    options['1'] = "Run Daily Price Capture", run_get_prices
    options['2'] = "Run Total Basestats refresh", run_get_sets
    options['3'] = "Update set", run_updat_set
    options['4'] = "Get Set Info", run_get_set_info
    options['5'] = "System", run_system
    options['9'] = "Quit", menu.quit

    while True:
        result = menu.options_menu(options)
        if result is 'kill':
            exit()


main()
