__author__ = 'andrew.sielen'

# Update a single set using the set num
# todo
#
#
#

import navigation.menu
from data import update_secondary as secondary
from system import base


def main():
    options = {}
    options['1'] = "Update Basestats", update_baseStats  # Todo: Check to see if this works
    options['2'] = "Update Prices", update_prices  # Todo
    options['3'] = "Manual Update", manual_Update  # Todo
    options['9'] = "Back", navigation.menu.back

    while True:
        result = navigation.menu.options_menu(options)
        if result is 'back':
            break
    print("Run Update Set")


def update_baseStats():
    print("Update Base Stats")
    set_id = base.input_set_num()
    secondary.add_set_to_database(set_id)


def update_prices():
    print("Update Prices")


def manual_Update():
    print("Manual Update")


if __name__ == "__main__":
    main()