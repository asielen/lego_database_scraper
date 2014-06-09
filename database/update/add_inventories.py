from data.update_database.add_parts_database import add_part_to_database

__author__ = 'andrew.sielen'

import sqlite3 as lite
import logging

import arrow

from database.info.database_info import database
from database.set_info_old import get_set_id
from database.piece_info_old import get_element_id
from database.piece_info_old import get_design_id
from database.update.add_pieces import add_element_to_database
import data.bricklink.bricklink_api as blapi


def add_bs_set_pieces_to_database(set_num, brickset_pieces):
    """

    @param set_num: standard format xxxx-x
    @param brickset_pieces: list of pieces [[x, q],[x, q]]
    @return: None
    """

    con = lite.connect(database)

    set_id = get_set_id(set_num)

    if set_id is not None:
        add_bs_inventory_to_database(set_id, brickset_pieces)


def add_bs_inventory_to_database(set_id, set_dict):
    """

    @param set_id: the row id from the sets table
    @param set_dict: the dictionary of the inventory of a set [element, qty]
    @return:
    """

    if set_dict is None or set_id is None:
        logging.warning("Can't add BS inventory to database: set_id = {}".format(set_id))
        return None

    con = lite.connect(database)

    # Remove the previous inventory from the database
    with con:
        c = con.cursor()
        c.execute('DELETE FROM bs_inventories WHERE set_id=?', (set_id, ))

    current_element = ""

    for e_set in set_dict:
        current_element = e_set[0]

        # Check to see if the piece is in the database
        piece_id = get_element_id(current_element)

        # If the piece isn't already in the database, add it
        if piece_id is None:
            logging.info("Adding BS element to database: element = " + current_element)

            piece_dic = BSPI.get_pieceinfo(current_element)

            if piece_dic is None:
                logging.warning("BS piece failed to scrape: element = " + current_element)
                return None

            design_id = get_design_id(piece_dic['design_num'])

            if design_id is None:
                logging.info("Adding BS design to database: design = " + piece_dic['design_num'])
                design_id = add_part_to_database(piece_dic)
                if design_id is None:
                    logging.warning("BS design id cannot be found: design = " + piece_dic['design_num'])
                    return None

            piece_id = add_element_to_database(design_id, piece_dic)

        with con:  # Add the element to the inventory table
            c = con.cursor()
            c.execute('INSERT INTO bs_inventories(set_id, piece_id, quantity) VALUES (?,?,?)',
                      (set_id, piece_id, e_set[1]))

    with con:  # Update the last date
        c = con.cursor()
        c.execute('UPDATE sets SET last_inv_updated_bs=? WHERE id=?',
                  (arrow.now('US/Pacific').format('YYYY-MM-DD'), set_id))


def add_bl_set_pieces_to_database(set_num, bricklink_pieces):
    """

    @param set_num: standard format xxxx-x
    @param bricklink_pieces: list of pieces [[x, q],[x, q]]
    @return:
    """

    con = lite.connect(database)

    set_id = get_set_id(set_num)

    if set_id is not None:
        add_bl_inventory_to_database(set_id, bricklink_pieces)


def add_bl_inventory_to_database(set_id, set_dict):
    """

    @param set_id: the row id from the sets table
    @param set_dict: the dictionary of the inventory of a set [element, qty]
    @return:
    """

    if set_dict is None or set_id is None:
        logging.warning("Can't add blapi inventory to database: set_id = {}".format(set_id))
        return None

    con = lite.connect(database)

    # Remove the previous inventory from the database
    with con:
        c = con.cursor()
        c.execute('DELETE FROM bl_inventories WHERE set_id=?', (set_id,))

    current_design = ""

    for e_set in set_dict:
        current_design = e_set
        current_quantity = set_dict[e_set]

        # Check to see if the design is in the database
        design_id = get_design_id(current_design)

        # If it isn't in the database yet, add it
        if design_id is None:
            logging.info("Adding blapi element to database: design = " + current_design)

            design_id = blapi.add_part_to_database(current_design)

        with con:
            c = con.cursor()
            c.execute('INSERT INTO bl_inventories(set_id, piece_id, quantity) VALUES (?,?,?)',
                      (set_id, design_id, current_quantity))

    with con:  # Update the last date
        c = con.cursor()
        c.execute('UPDATE sets SET last_inv_updated_bl=? WHERE id=?',
                  (arrow.now('US/Pacific').format('YYYY-MM-DD'), set_id))