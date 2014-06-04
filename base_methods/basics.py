__author__ = 'andrew.sielen'

# Automated: {run over all sets to update info}
# * add_bl_inventory(set_num)
#         @ Api call
#
# Basic: {once the database is initlaized, these are used to update one at a time}
#     * add_set(set_num)
#         @ Scrape data from Bricklink & Brickset
#     * add_part(part_num)
#         @ Scrape data from Bricklink & Brickset

import logging

import LBEF
from base_methods.basics_support import get_basestats
from database_management.add_set import add_set_to_database_from_dict
import apis.bricklink_api as blapi


def add_set_to_database(set_num):
    """
    Takes a set num, pulls all the base stats for it and then adds it to the database
    @param set_num: in the format xxxx-xx
    @return:
    """
    add_set_to_database_from_dict(get_basestats(set_num))


def add_piece_to_database(bl_id="", bo_id=""):
    """

    @param bl_id:
    @return:
    """
    if bl_id == "" and bo_id == "":
        return None
    if bl_id != "":
        blapi.add_part_to_database(bl_id)


def get_bl_inventory(set, bl_designs_in_database):
    """

    @param set: in standard format xxxx–x
    @param bl_designs_in_database: list of pieces
    @param force:
    @return:
    """
    set_num, set_seq, set = LBEF.expand_set_num(set)

    logging.info("Updating bricklink inventory for set {}".format(set))
    blapi.add_set_database(set)


def get_bs_inventory(set, bs_elements_in_database):
    """

    @param set:
    @param bs_elements_in_database:
    @param force:
    @return:
    """
    set_num, set_seq, set = expand_set_num(set)

    logging.info("Updating brickset inventory for set {}".format(set))
    brickset_pieces = BSP.get_setpieces(set_num, set_seq)
    if brickset_pieces is not None:
        add_inventories.add_bs_set_pieces_to_database(set, brickset_pieces)