__author__ = 'andrew.sielen'

import sqlite3 as lite

from database.set_info_old import database
from database.piece_info_old import get_design_id
from database.piece_info_old import get_element_id


def add_design_to_database(piece_dic):
    """
    Adds a design to the database
    @param piece_dic: a dictionary containing the piece information (from bricklink)
    @return:
    """

    con = lite.connect(database)

    with con:
        c = con.cursor()

        c.execute('INSERT OR IGNORE INTO piece_designs(design_num) VALUES (?)', (piece_dic['design_num'], ))
        c.execute('UPDATE piece_designs SET design_name=?, weight=?, design_alts=?, piece_type=? WHERE design_num=?;',
                  (piece_dic['design_name'], piece_dic['weight'], piece_dic['design_alts'], piece_dic['piece_type'],
                   piece_dic['design_num']))

    design_id = get_design_id(piece_dic['design_num'])

    if piece_dic['design_alts'] is not '' and piece_dic['design_alts'] is not None and design_id is not None:
        parse_design_alts(design_id, piece_dic['design_alts'])

    return design_id


def add_element_to_database(design_id, element_dic):
    """

    @param element_dic: a dictionary containing the element information (from brickset)
    @param design_id: the row of the design in the design table
    @return:
    """

    con = lite.connect(database)

    with con:
        c = con.cursor()
        c.execute('INSERT OR IGNORE INTO unique_pieces(part_num) VALUES (?)', (element_dic['part_num'], ))
        c.execute('UPDATE unique_pieces SET design_id=?, color_name=? WHERE part_num=?;',
                  (design_id, element_dic['color_name'], element_dic['part_num']))

    return get_element_id(element_dic['part_num'])


def parse_design_alts(design_id, design_alts):
    """
    Parse a design alts list and add it to the element database
    @param design_alts:
    @return:
    """
    design_list = [a.strip() for a in design_alts.split(',')]
    for design in design_list:
        add_element_to_database(design_id, {'color_name': 'ALT_ID', 'part_num': design})
