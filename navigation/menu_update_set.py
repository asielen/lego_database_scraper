__author__ = 'andrew.sielen'

# Update a single set using the set num
# todo
#
#
#

import navigation.menu

def main():
    options = {}
    options['1'] = "Update Basestats", update_baseStats
    options['2'] = "Update Prices", update_prices
    options['3'] = "Manual Update", manual_Update
    options['9'] = "Back", navigation.menu.back

    while True:
        result = navigation.menu.options_menu(options)
        if result is 'back':
            break
    print("Run Update Set")

def update_baseStats():
    print("Update Base Stats")

def update_prices():
    print("Update Prices")

def manual_Update():
    print("Manual Update")
