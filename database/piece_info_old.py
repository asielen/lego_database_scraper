__author__ = 'andrew.sielen'

import sqlite3 as lite

from database import database as db
from system import logger
from system import base_methods as base

# Todo: 20140901 Make sure all these functions work still

def get_bs_piece_id(part_num):
    """

    @param part_num: the number used by brickset for pieces
    @return: the primary key for a piece in the database
    """
    # Todo: 20140906L remove all instances of bS inventories
    con = lite.connect(db)

    element_id = None

    with con:
        c = con.cursor()
        c.execute('SELECT id FROM parts WHERE brickset_id=?', (part_num,))
        element_id_raw = c.fetchone()
        if element_id_raw is None:
            return None
        element_id = element_id_raw[0]

    return element_id


def get_bl_piece_id(design_num):
    """

    @param design_num: the number used by bricklink for pieces
    @return:the primary key for a piece in the database
    """
    design_id = None

    con = lite.connect(db)

    element_id = None

    with con:
        c = con.cursor()
        c.execute('SELECT id FROM parts WHERE bricklink_id=?', (design_num,))
        design_id_raw = c.fetchone()
        if design_id_raw is None:
            return None
        design_id = design_id_raw[0]

    return design_id


def get_sets_per_design():
    """

    @return: a list of all the designs with the number of sets they are in
    based off bricklink inventories
    """
    designs = []

    con = lite.connect(db)
    with con:
        c = con.cursor()
        c.execute("SELECT parts.bricklink_id, COUNT(bl_inventories.set_id) AS number_of_sets FROM parts "
                  "JOIN bl_inventories ON parts.id = bl_inventories.piece_id "
                  "GROUP BY parts.bricklink_id;")
        designs = c.fetchall()

    return designs


def get_years_available(design_num):
    """

    @param design_num: the design id used by bricklink
    @return: the first and last year a design was used in a set calculated by bl inventories
    """
    years = []

    con = lite.connect(db)
    with con:
        c = con.cursor()
        c.execute(
            "SELECT MIN(sets.year_released) AS first_year, MAX(sets.year_released) AS last_year FROM parts "
            "JOIN bl_inventories ON parts.id = bl_inventories.piece_id "
            "JOIN sets ON bl_inventories.set_id = sets.id "
            "WHERE parts.bricklink_id=?;", (design_num,))
        years = c.fetchall()

    return years


def get_avg_price_per_design(design_num):
    """
        if a piece is 10 cents in one set and 20 in another this returns 15
        This is also weighted for the number in a set, so if one set has 1000 at .10 and another has 100 at .5
        it will be close to .10
    @param design_num: the design id used by bricklink
    @return: taking the price per piece of a set, this calculates the average price per piece of a piece
    """
    avg_price = []

    design_id = get_bl_piece_id(design_num)  # this saves us from having to do an extra join

    con = lite.connect(db)
    with con:
        c = con.cursor()
        c.execute("SELECT SUM((sets.original_price_us / sets.piece_count) * "
                  "bl_inventories.quantity) / SUM(bl_inventories.quantity) "
                  "AS average_weighted_price FROM sets JOIN bl_inventories ON bl_inventories.set_id = sets.id "
                  "WHERE bl_inventories.piece_id=? AND sets.original_price_us IS NOT NULL;", (design_id, ))
        avg_price = c.fetchall()

    return avg_price


if __name__ == "__main__":
    from navigation import menu

    def main_menu():
        """
        Main launch menu
        @return:
        """

        logger.critical("set_info.py testing")
        options = {}

        options['1'] = "Get BS Part ID", menu_get_element_id
        options['2'] = "Get BL Part ID", menu_get_bl_piece_id
        options['3'] = "Get #sets / design", menu_get_sets_per_design
        options['4'] = "Get years available", menu_get_years_available
        options['5'] = "AVG price by design", menu_get_avg_price_per_design
        options['9'] = "Quit", menu.quit

        while True:
            result = menu.options_menu(options)
            if result is 'kill':
                exit()

    def menu_get_element_id():
        set_num = base.input_part_num()
        csvfile = get_bs_piece_id(set_num)
        print(csvfile)

    def menu_get_bl_piece_id():
        set_num = base.input_part_num()
        csvfile = get_bl_piece_id(set_num)
        print(csvfile)

    def menu_get_sets_per_design():
        csvfile = get_sets_per_design()
        base.print4(csvfile)


    def menu_get_years_available():
        set_num = base.input_part_num()
        csvfile = get_years_available(set_num)
        print(csvfile)


    def menu_get_avg_price_per_design():
        set_num = base.input_part_num()
        csvfile = get_avg_price_per_design(set_num)
        print(csvfile)


    if __name__ == "__main__":
        main_menu()
