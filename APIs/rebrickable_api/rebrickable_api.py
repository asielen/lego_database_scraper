__author__ = 'Andrew'

import logging

import navigation.menu as menu
from apis import api_methods as api
import system_setup as sys
import LBEF


KEY = 'LmtbQqIRtP'
url = 'http://rebrickable.com/api'

# These methods rely on the monthly data-dump, they are faster but less accurate
def pull_all_colors():
    """
    USE pull_colors instead. It has more detail
    This is from a datadump on http://rebrickable.com/downloads
    It pulls all colors in rebrickable terms
    @return:
    """
    # url = "http://rebrickable.com/files/colors.csv.gz"
    # return api.read_gzip_csv_from_url(url)
    return pull_colors()


def pull_all_pieces():
    """
    This is from a datadump on http://rebrickable.com/downloads
    It pulls all piece types in the database
    @return:
    """
    url = "http://rebrickable.com/files/pieces.csv.gz"
    return api.read_gzip_csv_from_url(url)


def pull_all_set_parts():
    """
    This is from a datadump on http://rebrickable.com/downloads
    It pulls all the inventories in the database, need to pull all pieces first
    @return:
    """
    url = "http://rebrickable.com/files/set_pieces.csv.gz"
    return api.read_gzip_csv_from_url(url)


def pull_set_info(set_num):
    """
    key - API Key
    set - The Set num to look up (e.g. 8043-1)
    format - How to display output data. Valid values: xml, json, csv, tsv
    @param set_num:
    @return:
    """
    parameters = {'key': KEY, 'set_id': set_num, 'format': 'csv'}
    return api.read_csv_from_url(url + '/get_set', params=parameters)


def pull_set_inventory(set_num):
    """
    key - API Key
    set - The Set ID to look up (e.g. 8258-1)
    format - How to display output data. Valid values: xml, json, csv, tsv
    @param set_num:
    @return:
    """
    parameters = {'key': KEY, 'set': set_num, 'format': 'csv'}
    return api.read_csv_from_url(url + '/get_set_parts', params=parameters)


def pull_piece_info(part_id):
    """
    key - API Key
    part_id - The Part ID to look up (e.g. 3001)
    inc_rels - Optional flag (1 or 0) to include Part Relationships in return data (may be a lot of data for some parts)
    inc_ext - Optional flag (1 or 0) to include external Part IDs (may be a lot of data for some parts due to LEGO element ids)
    format - How to display output data. Valid values: xml, json
    @param piece:
    @return: in json format for some stupid reason (a dictionary)
    """
    parameters = {'key': KEY, 'part_id': part_id, 'inc_ext': '1', 'format': 'json'}
    return api.read_json_from_url(url + '/get_part', params=parameters)


def pull_colors():
    """
    This doesn't use the API because it instead pulls ALL colors from this table: http://rebrickable.com/colors
        The api only returns the _main id
    @return: ['',rebrickable ID, Name, rgb hex, num parts, num sets, start year, start end, lego name, ldraw color, bricklink color, peeron color]
    note rebrickable ID is essentially the same as the ldraw id
    """
    url = 'http://rebrickable.com/colors'
    soup = LBEF.soupify(url)
    table = soup.find('table', {'class': 'table'})
    return LBEF.parse_html_table(table)


def main_menu():
    """
    Main launch menu
    @return:
    """
    sys.setup_logging()
    logging.info("RUNNING: Rebrickable API testing")
    options = {}

    options['1'] = "Pull Set Info", menu_pull_set_info
    options['2'] = "Pull Set Inventory", menu_pull_set_inventory
    options['3'] = "Pull Piece Info", menu_pull_piece_info
    options['4'] = "Pull all Pieces", menu_pull_all_pieces
    options['5'] = "Pull all set Parts", menu_pull_all_set_parts
    options['6'] = "SYS Pull Colors", menu_pull_colors
    options['9'] = "Quit", menu.quit

    while True:
        result = menu.options_menu(options)
        if result is 'kill':
            exit()


def menu_pull_all_pieces():
    csvfile = pull_all_pieces()
    api.print4(csvfile)


def menu_pull_all_set_parts():
    csvfile = pull_all_set_parts()
    api.print4(csvfile)


def menu_pull_set_info():
    set_num = input("What set num? ")
    csvfile = pull_set_info(set_num)
    api.print4(csvfile)


def menu_pull_set_inventory():
    set_num = input("What set num? ")
    csvfile = pull_set_inventory(set_num)
    # api.print4(csvfile)
    for c in csvfile:
        print(c)


def menu_pull_piece_info():
    piece_num = input("What piece num? ")
    csvfile = pull_piece_info(piece_num)
    print(csvfile)  # a dictionary that will need to be parsed


def menu_pull_colors():
    csvfile = pull_colors()
    api.print4(csvfile)


if __name__ == "__main__":
    main_menu()