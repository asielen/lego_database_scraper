# File Probably no longer needed todo

# Not used by anything

import system as syt

# http://brickset.com/inventories/21010-1 <-Set piece lookup

# Get pieces stats
def get_setpieces(set_num_primary, set_num_secondary=1):
    """
        Return a dictionary of pieces from Brickset.com
        ((part_num,qty),(part_num,qty),(part_num,qty))
        Part num is not the design id
    """
    # url = "http://brickset.com/inventories/{0}-{1}".format(set_num_primary, set_num_secondary)
    url = "http://brickset.com/exportscripts/inventory/{0}-{1}".format(set_num_primary, set_num_secondary) #Download as csv instead of scraping the page
    csv = syt.read_csv_from_url(url)

    pieces = _parse_pieces(csv)

    return pieces


# def get_setpieces_details(set_num_primary, set_num_secondary=1):
#     pieces = get_setpieces(set_num_primary, set_num_secondary)
#
#     pieces_details = {}
#     for p in pieces:
#         pieces_details[p[0]] = BPI.get_pieceinfo(p[0])
#
#     return pieces_details


def _parse_pieces(csv):
    validate = False
    pieces_array = []
    for row in csv:
        if len(row) < 1: continue
        row_l = row[0].split(',')
        if validate is False:
            if row_l[0] == "SetNumber":
                validate = True
                continue
            else: break
        pieces_array.append([row_l[1], int(row_l[2])])

    return pieces_array


if __name__ == "__main__":
    import pprint

    def main():
        set = input("What is the set num? ")
        pprint.pprint(get_setpieces(set))
        main()


    if __name__ == "__main__":
        main()