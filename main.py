__author__ = 'andrew.sielen'

import logging
import arrow

import navigation.menu as menu

def get_week_for_log():
    """
    @return: a text string "YYYYMMDD-WKN.log
    """
    today = arrow.now()
    return today.format('YYYY')+"-WK"+str(today.isocalendar()[1])+".log"

def setup_logging():
    logging.basicConfig(filename=str(get_week_for_log()), level=logging.WARNING)
    logging.basicConfig(format='%(asctime)s : %(message)s')

def main():
    """
    Main launch menu
    @return:
    """

    setup_logging()
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


import sys

root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

main()