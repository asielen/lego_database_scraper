__author__ = 'andrew.sielen'
# TODO: Is this needed?

import pprint as pp

from LBEF import *



# http://www.bricklink.com/catalogItemInv.asp?S=1068-1&v=0&bt=2 <-Set piece lookip

# TODO: This is no longer needed, replaced by bricklink_api.pull_set_inventory
# Get pieces stats
def get_setpieces(set_num_primary, set_num_secondary=1, verbose=0):
    """

        Return a dictionary of pieces from Bricklink.com
        {design_num: qty,design_num: qty,design_num: qty}
    """
    url = "http://www.bricklink.com/catalogItemInv.asp?S={0}-{1}&v=0&bt=1".format(set_num_primary, set_num_secondary)
    if verbose == 1: print(url)
    soup = soupify(url)

    pieces = {}
    pieces = _parse_pieces(soup)

    return pieces


def _parse_pieces(soup):
    parent_tags0 = soup.find("table", {"cellpadding": "3"})
    if parent_tags0 is None:
        return None

    pieces = {}
    table_array = parse_html_table(parent_tags0)[2:]
    for r in table_array:
        if len(r) == 1:
            if r[0] == 'Counterparts:' or r[0] == 'Books:' or r[0] == 'Gear:':
                break
        if len(r) == 5:
            current_piece = r[2].split(" ")[0]
            if current_piece in pieces:
                pieces[current_piece] += int(r[1])
            else:
                pieces[current_piece] = int(r[1].split(" ")[0])
    return pieces


def main():
    set = input("What is the set num? ")
    piece_list = get_setpieces(set)
    pp.pprint(piece_list)

    main()


if __name__ == "__main__":
    main()