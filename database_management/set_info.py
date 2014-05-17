__author__ = 'andrew.sielen'

import sqlite3 as lite
from database_management.database_info import database
import LBEF
import arrow

##Basic Funtions
def get_set_id(set_num):
    """
    @param set_num:
    @return: the id column num of the set in the database
    """
    set_id = None
    print(database)
    con = lite.connect(database)
    with con:
        c = con.cursor()
        c.execute('SELECT id FROM sets WHERE set_num=?', (set_num,))
        set_id_raw = c.fetchone()
        if set_id_raw is None:
            return None
        else:
            set_id = set_id_raw[0]
    return set_id


def check_last_updated_basestats(set_num, range=15):
    """

    @param set_num: in standard format xxxx-x
    @param range: days before and after today to check
    @return: True if updated in the range, False otherwise
    """

    con = lite.connect(database)
    with con:
        c = con.cursor()

        c.execute("SELECT last_updated FROM sets WHERE set_num=?", (set_num,))
        last_updated_raw = c.fetchone()
        if last_updated_raw is None:
            return False
        last_updated = last_updated_raw[0]

        last_updated = arrow.get(last_updated)
        return LBEF.check_in_date_range(last_updated, last_updated.replace(days=-range),
                                        last_updated.replace(days=+range))

    return False


def check_last_updated_bl_inv(set_num, range=15):
    """

    @param set_num: in standard format xxxx-x
    @param range: days before and after today to check
    @return: True if updated in the range, False otherwise
    """

    con = lite.connect(database)
    with con:
        c = con.cursor()

        c.execute("SELECT last_inv_updated_bl FROM sets WHERE set_num=?", (set_num, ))
        last_updated_raw = c.fetchone()
        if last_updated_raw is None: return False
        last_updated = last_updated_raw[0]

        last_updated = arrow.get(last_updated)

        return LBEF.check_in_date_range(last_updated, last_updated.replace(days=-range),
                                        last_updated.replace(days=+range))

    return False


def check_last_updated_bs_inv(set_num, range=15):
    """

    @param set_num: in standard format xxxx-x
    @param range: days before and after today to check
    @return: True if updated in the range, False otherwise
    """

    con = lite.connect(database)
    with con:
        c = con.cursor()

        c.execute("SELECT last_inv_updated_bs FROM sets WHERE set_num=?", (set_num, ))
        last_updated_raw = c.fetchone()
        if last_updated_raw is None: return False
        last_updated = last_updated_raw[0]

        last_updated = arrow.get(last_updated)

        return LBEF.check_in_date_range(last_updated, last_updated.replace(days=-range),
                                        last_updated.replace(days=+range))

    return False


def check_last_updated_daily_stats(set_num):
    """

    @param set_num: in standard format xxxx-x
    @return: True if updated today, False otherwise
    """

    con = lite.connect(database)
    with con:
        c = con.cursor()

        c.execute("SELECT last_price_updated FROM sets WHERE set_num=?", (set_num,))
        last_updated_raw = c.fetchone()
        if last_updated_raw is None: return False
        last_updated = last_updated_raw[0]
        if arrow.now().format("YYYY-MM-DD") == last_updated:
            return True

    return False


##More Advanced Calculations
def get_piece_count(set_num, type=''):
    """
    Returns the piece count of a set by either gettting it straight from the piece count column or by
    calculating it based on inventory

    @param set_num: in standard format xxxx-x
    @param type: '' or bricklink or brickset
    @return: the number of pieces
    """
    #Get the set ID.
    set_id = get_set_id(set_num)

    con = lite.connect(database)

    count = None

    if type == '':
        with con:
            c = con.cursor()
            c.execute("SELECT piece_count FROM sets WHERE id=?;", (set_id,))
            count = c.fetchone()[0]

    elif type == 'bricklink':
        with con:
            c = con.cursor()
            c.execute("SELECT SUM(bl_inventories.quantity) FROM bl_inventories "
                      "JOIN piece_designs ON bl_inventories.piece_id = piece_designs.id"
                      " WHERE bl_inventories.set_id=?;", (set_id,))
            count = c.fetchone()[0]

    elif type == 'brickset':
        with con:
            c = con.cursor()
            c.execute('SELECT SUM(bs_inventories.quantity) FROM bs_inventories '
                      'JOIN unique_pieces ON bs_inventories.piece_id = unique_pieces.id '
                      'JOIN piece_designs ON unique_pieces.design_id = piece_designs.id '
                      'WHERE bs_inventories.set_id=?', (set_id,))
            count = c.fetchone()[0]

    return count


def get_unique_piece_count(set_num, type=''):
    """
    Returns the unique piece count of a set by calculating it based on inventory

    @param set_num: in standard format xxxx-x
    @param type: bricklink or brickset
    @return: the number of pieces
    """
    #Get the set ID.
    set_id = get_set_id(set_num)

    con = lite.connect(database)

    count = None

    if type == 'bricklink':
        with con:
            c = con.cursor()
            c.execute("SELECT COUNT(bl_inventories.quantity) FROM bl_inventories JOIN piece_designs"
                      " ON bl_inventories.piece_id = piece_designs.id"
                      " WHERE bl_inventories.set_id=?;", (set_id,))
            count = c.fetchone()[0]

    elif type == 'brickset':
        with con:
            c = con.cursor()
            c.execute('SELECT COUNT(bs_inventories.quantity) FROM bs_inventories '
                      'JOIN unique_pieces ON bs_inventories.piece_id = unique_pieces.id '
                      'JOIN piece_designs ON unique_pieces.design_id = piece_designs.id '
                      'WHERE bs_inventories.set_id=?', (set_id,))
            count = c.fetchone()[0]

    return count


def get_set_weight(set_num, type=''):
    """
    Returns the weight of a set by either gettting it straight from the set weight column or by
    calculating it based on inventory

    @param set_num: in standard format xxxx-x
    @param type: '' or bricklink or brickset
    @return: the weight in grams
    """
    #Get the set ID.
    set_id = get_set_id(set_num)

    con = lite.connect(database)

    weight = None

    if type == '':
        with con:
            c = con.cursor()
            c.execute("SELECT set_weight FROM sets WHERE id=?;", (set_id,))
            weight = c.fetchone()[0]

    elif type == 'bricklink':
        with con:
            c = con.cursor()
            c.execute(
                "SELECT SUM(bl_inventories.quantity * piece_designs.weight) FROM bl_inventories JOIN piece_designs"
                " ON bl_inventories.piece_id = piece_designs.id"
                " WHERE bl_inventories.set_id=?;", (set_id,))
            weight = c.fetchone()[0]

    elif type == 'brickset':
        with con:
            c = con.cursor()
            c.execute('SELECT SUM(bs_inventories.quantity * piece_designs.weight) FROM bs_inventories '
                      'JOIN unique_pieces ON bs_inventories.piece_id = unique_pieces.id '
                      'JOIN piece_designs ON unique_pieces.design_id = piece_designs.id '
                      'WHERE bs_inventories.set_id=?', (set_id,))
            weight = c.fetchone()[0]

    return weight



