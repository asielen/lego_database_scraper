__author__ = 'andrew.sielen'

import logging

import navigation.menu as menu
import system_setup as sys


def main():
    """
    Main launch menu
    @return:
    """

    sys.setup_logging()
    logging.critical("Test Warning")
    options = {}

    options['1'] = "Run Daily Price Capture", menu.run_get_prices
    options['2'] = "Run Total Basestats refresh", menu.run_get_sets
    options['3'] = "Update set", menu.run_updat_set
    options['4'] = "Get Set Info", menu.run_get_set_info
    options['5'] = "System", menu.run_system
    options['9'] = "Quit", menu.quit

    while True:
        result = menu.options_menu(options)
        if result is 'kill':
            exit()


main()