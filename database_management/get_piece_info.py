__author__ = 'andrew.sielen'

import sqlite3 as lite

from database_management.database import database


def get_bl_piece_id(part_num):
    """
    @param part_num: the number used by bricklink for pieces
    @return: the primary key for a piece in the database
    """
    con = lite.connect(database)

    element_id = None

    with con:
        c = con.cursor()
        c.execute('SELECT id FROM parts WHERE bricklink_id=?', (part_num,))
        element_id_raw = c.fetchone()
        if element_id_raw is None:
            return None
        element_id = element_id_raw[0]

    return element_id


#
# def get_element_id(part_num):
# """
#     @param part_num: the number used by brickset for pieces
#     @return: the primary key for a piece in the database
#     """
#     con = lite.connect(database)
#
#     element_id = None
#
#     with con:
#         c = con.cursor()
#         c.execute('SELECT id FROM unique_pieces WHERE part_num=?', (part_num,))
#         element_id_raw = c.fetchone()
#         if element_id_raw is None:
#             return None
#         element_id = element_id_raw[0]
#
#     return element_id
#
# def get_design_id(design_num):
#     """
#
#     @param design_num: the number used by bricklink for pieces
#     @return:the primary key for a piece in the database
#     """
#     design_id = None
#
#     con = lite.connect(database)
#
#     element_id = None
#
#     with con:
#         c = con.cursor()
#         c.execute('SELECT id FROM piece_designs WHERE design_num=?', (design_num,))
#         design_id_raw = c.fetchone()
#         if design_id_raw is None:
#             return None
#         design_id = design_id_raw[0]
#
#     return design_id

#TODO: Make sure this works with the new database structure
def get_sets_per_design():
    """

    @return: a list of all the designs with the number of sets they are in
    based off bricklink inventories
    """
    designs = []

    con = lite.connect(database)
    with con:
        c = con.cursor()
        c.execute("SELECT piece_designs.design_num, COUNT(bl_inventories.set_id) AS number_of_sets FROM piece_designs "
                  "JOIN bl_inventories ON piece_designs.id = bl_inventories.piece_id "
                  "GROUP BY piece_designs.design_num;")
        designs = c.fetchall()

    return designs


#TODO: Make sure this works with the new database structure
def get_years_available(design_num):
    """

    @param design_num: the design id used by bricklink
    @return: the first and last year a design was used in a set calculated by bl inventories
    """
    years = []

    con = lite.connect(database)
    with con:
        c = con.cursor()
        c.execute(
            "SELECT MIN(sets.year_released) AS first_year, MAX(sets.year_released) AS last_year FROM piece_designs "
            "JOIN bl_inventories ON piece_designs.id = bl_inventories.piece_id "
            "JOIN sets ON bl_inventories.set_id = sets.id "
            "WHERE piece_designs.design_num=?;", (design_num,))
        years = c.fetchall()

    return years


#TODO: Make sure this works with the new database structure
def get_avg_price_per_design(design_num):
    """
        if a piece is 10 cents in one set and 20 in another this returns 15
        This is also weighted for the number in a set, so if one set has 1000 at .10 and another has 100 at .5
        it will be close to .10
    @param design_num: the design id used by bricklink
    @return: taking the price per piece of a set, this calculates the average price per piece of a piece
    """
    avg_price = []

    design_id = get_design_id(design_num)  #this saves us from having to do an extra join

    con = lite.connect(database)
    with con:
        c = con.cursor()
        c.execute("SELECT SUM((sets.original_price_us / sets.piece_count) * "
                  "bl_inventories.quantity) / SUM(bl_inventories.quantity) "
                  "AS average_weighted_price FROM sets JOIN bl_inventories ON bl_inventories.set_id = sets.id "
                  "WHERE bl_inventories.piece_id=? AND sets.original_price_us IS NOT NULL;", (design_id, ))
        avg_price = c.fetchall()

    return avg_price

