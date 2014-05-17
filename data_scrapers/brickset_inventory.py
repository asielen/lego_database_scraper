__author__ = 'andrew.sielen'

from LBEF import *
import pprint
from data_scrapers import brickset_piece_info as BPI


# http://brickset.com/inventories/21010-1 <-Set piece lookip

#Get pieces stats
def get_setpieces(set_num_primary, set_num_secondary=1):
    """
        Return a dictionary of pieces from Brickset.com
        ((part_num,qty),(part_num,qty),(part_num,qty))
    """
    url = "http://brickset.com/inventories/{0}-{1}".format(set_num_primary, set_num_secondary)
    # print(url)
    soup = soupify(url)

    pieces = {}
    pieces = _parse_pieces(soup)

    return pieces


def get_setpieces_details(set_num_primary, set_num_secondary=1):
    pieces = get_setpieces(set_num_primary, set_num_secondary)

    pieces_details = {}
    for p in pieces:
        print(p[0])
        pieces_details[p[0]] = BPI.get_pieceinfo(p[0])

    return pieces_details


def _parse_pieces(soup):
    if soup is None:
        return None
    parent_tags0 = soup.find("section", {"class": "main"})
    if parent_tags0 is None:
        return None
    parent_table0 = parent_tags0.find("table", {"class": "neattable"})
    if parent_table0 is None:
        return None

    pieces_array = parse_html_table(parent_table0)

    pieces_array2 = []

    for i in range(0, len(pieces_array)):
        pieces_array2.append([pieces_array[i][0], int(pieces_array[i][2])])

    return pieces_array2


def main():
    set = input("What is the set num? ")
    pprint.pprint(get_setpieces(set))
    main()


if __name__ == "__main__":
    main()