__author__ = 'andrew.sielen'
# todo

import navigation.menu
import database.info as info
from system import base


def main():
    options = {}
    options['1'] = "Quick Info", quick_info  # Working 2014-10-5
    options['2'] = "Make single set report", make_setReport  # Todo: See DM report for example
    options['3'] = "Make price report", make_priceReport  # Todo: See DM report for example
    options['9'] = "Back", navigation.menu.back

    while True:
        result = navigation.menu.options_menu(options)
        if result is 'back':
            break
    print("Run Get Info")


def quick_info():
    set_num = base.input_set_num()
    info.get_set_dump(set_num)


def make_setReport():
    print("Make Set Report")


def make_priceReport():
    print("Make Price Report")


if __name__ == "__main__":
    main()
