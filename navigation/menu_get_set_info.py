__author__ = 'andrew.sielen'

import navigation.menu

def main():
    options = {}
    options['1'] = "Quick Info", quick_info
    options['2'] = "Make set report", make_setReport
    options['3'] = "Make price report", make_priceReport
    options['9'] = "Back", navigation.menu.back

    while True:
        result = navigation.menu.options_menu(options)
        if result is 'back':
            break
    print("Run Get Info")



def quick_info():
    print("Quick Info")

def make_setReport():
    print("Make Set Report")

def make_priceReport():
    print("Make Price Report")