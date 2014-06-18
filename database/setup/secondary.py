__author__ = 'andrew.sielen'

# Secondary: {initiate the database, rely on primitives but can still be downloaded in bulk}
# * init_part_color_codes()
# @ Download from Bricklink and add to the database
# * init_sets()
#         @ Download sets from Bricklink
#         @ Download sets from Rebrickable
#     * init_re_inventories()
#         @ Download from Rebrickable Api and add to the database
# todo: need to implement this

import data.bricklink.bricklink_api as blapi


def init_part_color_codes():
    """
    Download the part color codes from bricklink and insert them into the database
    @return:
    """
    pass


def init_sets():
    """
    Download the list of sets from bricklink and get all their data
    @return:
    """
    blapi.update_sets()


def init_re_parts():
    """
    Download the list of sets from rebrickable and compare it to the current database, adding whatever is missing
    @return:
    """
    pass


def init_re_inventories():
    pass


if __name__ == "__main__":
    pass