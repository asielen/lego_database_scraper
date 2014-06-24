from system.base_methods import LBEF

__author__ = 'andrew.sielen'

import sqlite3 as lite

import arrow

from system.calculate_inflation import get_inflation_rate
import database as db


def get_set_id(set_num, sets=None, add=False):
    """
    @param set_num:
    @param add: if True, Add the set if it is missing in the database
    @return: the id column num of the set in the database
    """
    con = lite.connect(db.database)
    with con:
        c = con.cursor()
        c.execute('SELECT id FROM sets WHERE set_num=?', (set_num,))
        set_id_raw = c.fetchone()
    if set_id_raw is None:
        return None
    else:
        return set_id_raw[0]


def filter_list_on_dates(sets, year_sets, date_range=180):
    """

    @param sets: list of set nums [xxx–xx,yyy–y,zzz–z]
    @param year_sets: dict of a list of sets with last updated dates {xxx–x:2014-05-12}
    @param date_range: the number of days on either side of the date
    @return: a list of sets that need to be updated
    """
    result = []

    today = arrow.now()
    past = today.replace(days=-date_range)

    for s in sets:
        if s in year_sets:
            if LBEF.check_in_date_rangeA(arrow.get(year_sets[s]), past, today):
                continue
        result.append(s)

    return result


def check_last_updated_daily_stats(set_num):
    """

    @param set_num: in standard format xxxx-x
    @return: True if updated today, False otherwise
    """

    con = lite.connect(db.database)
    with con:
        c = con.cursor()

        c.execute("SELECT last_price_updated FROM sets WHERE set_num=?", (set_num,))
        last_updated_raw = c.fetchone()
        if last_updated_raw is None: return False
        last_updated = last_updated_raw[0]
        if arrow.now().format("YYYY-MM-DD") == last_updated:
            return True

    return False


# # Basic information
# TODO: Make sure this works with the new database structure
def get_set_price(set_num, year=None):
    """

    @param set_num: set num in xxxx–x
    @param year: if this is not None, then get the price adjusted for system
    @return: the price
    """
    set_id = get_set_id(set_num)
    if set_id is None: return None

    con = lite.connect(db.database)
    year = int(arrow.now().format("YYYY")) - 2
    with con:
        c = con.cursor()
        c.execute("SELECT original_price_us FROM sets WHERE id=?;", (set_id,))
        price_raw = c.fetchone()
        if price_raw is None: return None
        price = price_raw[0]

    if year is not None:
        with con:
            c = con.cursor()
            c.execute("SELECT year_released FROM sets WHERE id=?;", (set_id,))
            year_raw = c.fetchone()
            if year_raw is None: return None
            year_released = year_raw[0]

        price_inflated = (get_inflation_rate(year_released, year) * price) + price
        return price_inflated, year_released, year
    else:
        return price


# #More Advanced Calculations
# TODO: Make sure this works with the new database structure
def get_piece_count(set_num, type=''):
    """
    Returns the piece count of a set by either getting it straight from the piece count column or by
    calculating it based on inventory

    @param set_num: in standard format xxxx-x
    @param type: '' or bricklink or brickset
    @return: the number of pieces
    """
    # Get the set ID.
    set_id = get_set_id(set_num)
    if set_id is None: return None

    con = lite.connect(db.database)

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
                      "JOIN parts ON bl_inventories.piece_id = parts.id"
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


# TODO: Make sure this works with the new database structure
def get_unique_piece_count(set_num, type=''):
    """
    Returns the unique piece count of a set by calculating it based on inventory

    @param set_num: in standard format xxxx-x
    @param type: bricklink or brickset
    @return: the number of pieces
    """
    # Get the set ID.
    set_id = get_set_id(set_num)

    con = lite.connect(db.database)

    count = None

    if type == 'bricklink':
        with con:
            c = con.cursor()
            c.execute("SELECT COUNT(bl_inventories.quantity) FROM bl_inventories JOIN parts"
                      " ON bl_inventories.piece_id = parts.id"
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


# TODO: Make sure this works with the new database structure
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

    con = lite.connect(db.database)

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


def main():
    set = LBEF.input_set_num()
    print("Calculated: {}".format(get_piece_count(set, 'bricklink')))
    print("Reported: {}".format(get_piece_count(set, '')))
    print("Unique: {}".format(get_unique_piece_count(set, 'bricklink')))
    main()


if __name__ == "__main__":
    main()


