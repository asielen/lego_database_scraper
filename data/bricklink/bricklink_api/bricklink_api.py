# Internal

import system as syt
from data.data_classes import SetInfo

if __name__ == "__main__": syt.setup_logger()

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
# X : XML (seems to default to this)

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
    return syt.read_csv_from_url(url, params=parameters)


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
    return syt.read_csv_from_url(url, params=parameters)


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
    return syt.read_csv_from_url(url, params=parameters)


def pull_book_catalog():
    """
    Access bricklink.com and download the csv of its book catalog
    # http://www.bricklink.com/catalogDownload.asp?viewType=0&itemType=B&itemTypeInv=S&itemNo=&downloadType=T
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
    return syt.read_csv_from_url(url, params=parameters)


def pull_gear_catalog():
    """
    Access bricklink.com and download the csv of its book catalog
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
    return syt.read_csv_from_url(url, params=parameters)


def pull_catalogs_catalog():
    """
    Access bricklink.com and download the csv of its book catalog
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
    return syt.read_csv_from_url(url, params=parameters)


def pull_instructions_catalog():
    """
    Access bricklink.com and download the csv of its book catalog
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
    return syt.read_csv_from_url(url, params=parameters)


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
    return syt.read_csv_from_url(url, params=parameters)


def pull_item_types():
    """
    Access bricklink.com and download the csv of its book catalog
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
    return syt.read_csv_from_url(url, params=parameters)


def pull_categories():
    """
    Access bricklink.com and download the csv of its book catalog
    # http://www.bricklink.com/catalogDownload.asp?itemType=S&viewType=2&itemTypeInv=S&itemNo=&downloadType=T
    @return: [Category ID, Category Name]
    """
    url = "http://www.bricklink.com/catalogDownload.asp"
    parameters = {'itemType': 'S',
                  'viewType': '2',
                  'itemTypeInv': 'S',
                  'itemNo': None,
                  'downloadType': 'T'}
    return syt.read_csv_from_url(url, params=parameters)


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
    return syt.read_csv_from_url(url, params=parameters)


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
    return syt.read_csv_from_url(url, params=parameters)


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
    return syt.read_csv_from_url(url, params=parameters)


if __name__ == "__main__":
    def main_menu():
        """
        Main launch menu
        @return:
        """

        options = (
            ("Pull Set Inventory", menu_pull_set_inventory),
            ("Pull Set Catalog", menu_pull_set_catalog),
            ("Pull Part Catalog", menu_pull_part_catalog),
            ("Pull Minifig Catalog", menu_pull_minifig_catalog),
            ("SYS Pull Item Types", menu_pull_item_types),
            ("SYS Pull Categories", menu_pull_categories),
            ("SYS Pull Colors", menu_pull_colors),
            ("SYS Pull Part Codes", menu_pull_part_color_codes)
        )

        syt.Menu(name="– Bricklink API Testing –", choices=options, quit_tag="Exit").run()

    def menu_pull_set_catalog():
        csvfile = pull_set_catalog()
        syt.print4(csvfile)


    def menu_pull_part_catalog():
        csvfile = pull_part_catalog()
        syt.print4(csvfile)


    def menu_pull_minifig_catalog():
        csvfile = pull_part_catalog()
        syt.print4(csvfile)


    def menu_pull_item_types():
        csvfile = pull_item_types()
        syt.print4(csvfile)


    def menu_pull_categories():
        csvfile = pull_categories()
        syt.print4(csvfile)


    def menu_pull_colors():
        csvfile = pull_colors()
        syt.print4(csvfile)


    def menu_pull_part_color_codes():
        csvfile = pull_part_color_codes()
        syt.print4(csvfile)


    def menu_pull_set_inventory():
        set_num = SetInfo.input_set_num()
        csvfile = pull_set_inventory(set_num)
        syt.print4(csvfile)


    if __name__ == "__main__":
        main_menu()
