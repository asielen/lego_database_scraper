# TODO: Add return specs for all api calls

# parameter info
# itemType =
# S : set
# P : parts
# M : minifig
# B : books
#
# downloadType =
# T : tabs
#   X : XML (seems to default to this)

#external
import logging

logger = logging.getLogger('LBEF')

#other module
from navigation import menu
from system import setup_logging as sys
from system.base_methods import LBEF


url = "http://www.bricklink.com/catalogDownload.asp"


def pull_set_catalog():
    """
    Access bricklink.com and download the csv of all the sets
    viewType=0&itemType=S&selYear=Y&selWeight=Y&selDim=Y&itemTypeInv=S&itemNo=&downloadType=T
    @return: ['Category ID', 'Category Name', 'Number', 'Name', 'Year Released', 'Weight (in Grams)', 'Dimensions']
    3 rows of heading
    """
    parameters = {'a': 'a',
                  'itemType': 'S',
                  'viewType': '0',
                  'selYear': 'Y',
                  'selWeight': 'Y',
                  'selDim': 'Y',
                  'itemTypeInv': 'S',
                  'downloadType': 'T'}
    return LBEF.read_csv_from_url(url, params=parameters)


def pull_part_catalog():
    """
    Access bricklink.com and download the csv of its part catalog
    # http://www.bricklink.com/catalogDownload.asp?viewType=0&itemType=P&selYear=Y&selWeight=Y&selDim=Y&itemTypeInv=S&itemNo=&downloadType=T
    @return: ['Category ID', 'Category Name', 'Number', 'Name', 'Weight (in Grams)']
    3 header rows
    """
    parameters = {'a': 'a',
                  'itemType': 'P',
                  'viewType': '0',
                  'itemTypeInv': 'S',
                  'selYear': 'Y',
                  'selWeight': 'Y',
                  'itemNo': None,
                  'downloadType': 'T'}
    return LBEF.read_csv_from_url(url, params=parameters)


def pull_minifig_catalog():
    """
    Access bricklink.com and download the csv of its minifig catalog
    # http://www.bricklink.com/catalogDownload.asp?viewType=0&itemType=M&selYear=Y&selWeight=Y&selDim=Y&itemTypeInv=S&itemNo=&downloadType=T
    @return: ['Category ID', 'Category Name', 'Number', 'Name', 'Weight (in Grams)']
    3 header rows
    """
    parameters = {'a': 'a',
                  'itemType': 'M',
                  'viewType': '0',
                  'itemTypeInv': 'S',
                  'selYear': 'Y',
                  'selWeight': 'Y',
                  'itemNo': None,
                  'downloadType': 'T'}
    return LBEF.read_csv_from_url(url, params=parameters)


def pull_book_catalog():
    """
    Access bricklink.com and download the csv of its book catalog
    # http://www.bricklink.com/catalogDownload.asp?viewType=0&itemType=B&itemTypeInv=S&itemNo=&downloadType=T
    @param set_num:
    @return:
    """
    parameters = {'a': 'a',
                  'itemType': 'B',
                  'viewType': '0',
                  'itemTypeInv': 'S',
                  'selYear': 'Y',
                  'selWeight': 'Y',
                  'itemNo': None,
                  'downloadType': 'T'}
    return LBEF.read_csv_from_url(url, params=parameters)


def pull_gear_catalog():
    """
    Access bricklink.com and download the csv of its book catalog
    @param set_num:
    @return:
    """
    parameters = {'itemType': 'G',
                  'viewType': '0',
                  'itemTypeInv': 'S',
                  'selYear': 'Y',
                  'selWeight': 'Y',
                  'selDim': 'Y',
                  'itemNo': None,
                  'downloadType': 'T'}
    return LBEF.read_csv_from_url(url, params=parameters)


def pull_catalogs_catalog():
    """
    Access bricklink.com and download the csv of its book catalog
    @param set_num:
    @return:
    """
    parameters = {'itemType': 'C',
                  'viewType': '0',
                  'itemTypeInv': 'S',
                  'selYear': 'Y',
                  'selWeight': 'Y',
                  'selDim': 'Y',
                  'itemNo': None,
                  'downloadType': 'T'}
    return LBEF.read_csv_from_url(url, params=parameters)


def pull_instructions_catalog():
    """
    Access bricklink.com and download the csv of its book catalog
    @param set_num:
    @return:
    """
    parameters = {'itemType': 'I',
                  'viewType': '0',
                  'itemTypeInv': 'S',
                  'selYear': 'Y',
                  'selWeight': 'Y',
                  'selDim': 'Y',
                  'itemNo': None,
                  'downloadType': 'T'}
    return LBEF.read_csv_from_url(url, params=parameters)


def pull_boxes_catalog():
    """
    Access bricklink.com and download the csv of its book catalog
    @param set_num:
    @return:
    """
    parameters = {'itemType': 'O',
                  'viewType': '0',
                  'itemTypeInv': 'S',
                  'selYear': 'Y',
                  'selWeight': 'Y',
                  'selDim': 'Y',
                  'itemNo': None,
                  'downloadType': 'T'}
    return LBEF.read_csv_from_url(url, params=parameters)


def pull_item_types():
    """
    Access bricklink.com and download the csv of its book catalog
    @param set_num:
    @return: [Item Type ID, Item Type name]
    """
    parameters = {'itemType': 'O',
                  'viewType': '1',
                  'itemTypeInv': 'S',
                  'selYear': 'Y',
                  'selWeight': 'Y',
                  'selDim': 'Y',
                  'itemNo': None,
                  'downloadType': 'T'}
    return LBEF.read_csv_from_url(url, params=parameters)


def pull_categories():
    """
    Access bricklink.com and download the csv of its book catalog
    # http://www.bricklink.com/catalogDownload.asp?itemType=S&viewType=2&itemTypeInv=S&itemNo=&downloadType=T
    @param set_num:
    @return: [Category ID, Category Name]
    """
    url = "http://www.bricklink.com/catalogDownload.asp"
    parameters = {'itemType': 'S',
                  'viewType': '2',
                  'itemTypeInv': 'S',
                  'itemNo': None,
                  'downloadType': 'T'}
    return LBEF.read_csv_from_url(url, params=parameters)


def pull_colors():
    """
    itemType=O&selYear=Y&selWeight=Y&selDim=Y&viewType=3&itemTypeInv=S&itemNo=&downloadType=T
    @return: [Color ID, Color Name, RGB, Type, Parts, In Sets, Wanted, For Sale, Year From, Year To]
    """
    url = "http://www.bricklink.com/catalogDownload.asp"
    parameters = {'itemType': 'O',
                  'viewType': '3',
                  'itemTypeInv': 'S',
                  'itemNo': None,
                  'downloadType': 'T'}
    return LBEF.read_csv_from_url(url, params=parameters)


def pull_part_color_codes():
    """
    itemType=O&selYear=Y&selWeight=Y&selDim=Y&viewType=5&itemTypeInv=S&itemNo=&downloadType=T
    @return: [Item no (from part list), Color, Code]
    """
    url = "http://www.bricklink.com/catalogDownload.asp"
    parameters = {'itemType': 'O',
                  'viewType': '5',
                  'itemTypeInv': 'S',
                  'itemNo': None,
                  'downloadType': 'T'}
    return LBEF.read_csv_from_url(url, params=parameters)


def pull_set_inventory(set_num):
    """
    Access bricklink.com and download the csv of its inventory into a csv file
    http://www.bricklink.com/catalogDownload.asp?a=a&itemType=S&viewType=4&itemTypeInv=S&itemNo=10197-1&downloadType=T
    @return:
    """
    url = "http://www.bricklink.com/catalogDownload.asp"
    parameters = {'a': 'a',
                  'itemType': 'S',
                  'viewType': '4',
                  'itemTypeInv': 'S',
                  'itemNo': set_num,
                  'downloadType': 'T'}
    return LBEF.read_csv_from_url(url, params=parameters)


if __name__ == "__main__":
    def main_menu():
        """
        Main launch menu
        @return:
        """
        sys.setup_logging()
        logger.critical("Bricklink API testing")
        options = {}

        options['1'] = "Pull Set Inventory", menu_pull_set_inventory
        options['2'] = "Pull Set Catalog", menu_pull_set_catalog
        options['3'] = "Pull Part Catalog", menu_pull_part_catalog
        options['4'] = "Pull Minifig Catalog", menu_pull_minifig_catalog
        options['5'] = "SYS Pull Item Types", menu_pull_item_types
        options['6'] = "SYS Pull Categories", menu_pull_categories
        options['7'] = "SYS Pull Colors", menu_pull_colors
        options['8'] = "SYS Pull Part Codes", menu_pull_part_color_codes
        options['9'] = "Quit", menu.quit

        while True:
            result = menu.options_menu(options)
            if result is 'kill':
                exit()


    def menu_pull_set_catalog():
        csvfile = pull_set_catalog()
        LBEF.print4(csvfile)


    def menu_pull_part_catalog():
        csvfile = pull_part_catalog()
        LBEF.print4(csvfile)


    def menu_pull_minifig_catalog():
        csvfile = pull_part_catalog()
        LBEF.print4(csvfile)


    def menu_pull_item_types():
        csvfile = pull_item_types()
        LBEF.print4(csvfile)


    def menu_pull_categories():
        csvfile = pull_categories()
        LBEF.print4(csvfile)


    def menu_pull_colors():
        csvfile = pull_colors()
        LBEF.print4(csvfile)


    def menu_pull_part_color_codes():
        csvfile = pull_part_color_codes()
        LBEF.print4(csvfile)


    def menu_pull_set_inventory():
        set_num = LBEF.input_set_num()
        csvfile = pull_set_inventory(set_num)
        LBEF.print4(csvfile)


    if __name__ == "__main__":
        print("Running as Test")
        main_menu()
