__author__ = 'andrew.sielen'

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





def quit():
    return 'kill'

def back():
    return 'back'

def options_menu(menu_options):

    options = list(menu_options.keys())
    options.sort()

    print()
    for entry in options:
        print(entry, menu_options[entry][0])

    selection = input("What would you like to do? ")

    if selection in menu_options:

        action = menu_options[selection][1]
        return action()
    else:
        print("Invalid Input. Please try again")
