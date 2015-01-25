__author__ = 'andrew.sielen'
# Basic menu system

def quit():
    return 'kill'


def back():
    return 'back'


def options_menu(menu_options):
    options = list(menu_options.keys())
    options.sort()

    print()
    for entry in options:
        print(entry + ":", menu_options[entry][0])

    selection = input("What would you like to do? ")

    if selection in menu_options:

        action = menu_options[selection][1]
        return action()
    else:
        print("Invalid Input. Please try again")
