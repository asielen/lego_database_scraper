__author__ = 'andrew.sielen'

import sqlite3 as lite

import arrow

from database import database as db
from system.calculate_inflation import get_inflation_rate
from system import logger
from navigation import menu
from system import base_methods as base


# Done: 20140901 Make sure all these functions work still
#Todo: 20140904 Isn't some of this in database/info?

# # Basic Funtions
def get_set_id(set_num):
    """
    confirmed 20140904
    @param set_num: (TEXT) in this format xxxx-yy
    @return: (NUM) the id column num of the set in the database
    """
    set_id = None

    con = lite.connect(db)
    with con:
        c = con.cursor()
        c.execute('SELECT id FROM sets WHERE set_num=?', (set_num,))
        set_id_raw = c.fetchone()
        if set_id_raw is None:
            return None
        else:
            set_id = set_id_raw[0]
    return set_id


# These three functions return lists of sets that need to be updated
def get_all_set_years():
    """
    confirmed 20140904
    @return: a dictionary of all the sets in the database with the last date they were updated
    in the format {xxxx-y:[Date as text string Linux format],xxx-yy:DATE}
    """
    con = lite.connect(db)
    with con:
        c = con.cursor()
        c.execute("SELECT set_num, last_updated FROM sets;")
        last_updated = c.fetchall()

    if last_updated is None:
        return {}

    return {t[0]: t[1] for t in last_updated}  # convert from list of lists to a dictionary


def get_all_bl_update_years():
    """
    confirmed 20140904
    @return: a list of all the sets in the database that need to be updated with bricklink inventory
    """
    con = lite.connect(db)
    with con:
        c = con.cursor()
        c.execute("SELECT set_num, last_inv_updated_bl FROM sets;")
        last_updated = c.fetchall()

    if last_updated is None:
        return {}

    return {t[0]: t[1] for t in last_updated}  # convert from list of lists to a dictionary


def get_all_bs_update_years():
    """
    confirmed 20140904
    @return: a list of all the sets in the database that need to be updated with brickset inventory
    """
    con = lite.connect(db)
    with con:
        c = con.cursor()
        c.execute("SELECT set_num, last_inv_updated_bs FROM sets;")
        last_updated = c.fetchall()

    if last_updated is None:
        return {}

    return {t[0]: t[1] for t in last_updated}  # convert from list of lists to a dictionary


def check_last_updated_daily_stats(set_num):
    """
    confirmed 20140904 - Check again when updating sets
    @param set_num: in standard format xxxx-x
    @return: True if updated today, False otherwise
    """

    con = lite.connect(db)
    with con:
        c = con.cursor()

        c.execute("SELECT last_price_updated FROM sets WHERE set_num=?", (set_num,))
        last_updated_raw = c.fetchone()
        if last_updated_raw is None: return False
        last_updated = last_updated_raw[0]
        if arrow.now() == last_updated:  # If anything causes a problem, it is probably this line. Check date storage format
            return True

    return False


# # Basic information
def get_set_price(set_num, year=None):
    """
    confirmed 20140904
    @param set_num: set num in xxxx–x
    @param year: if this is not None, then get the price adjusted for system
    @return: the price
    """
    set_id = get_set_id(set_num)
    if set_id is None: return None

    con = lite.connect(db)

    with con:
        c = con.cursor()
        c.execute("SELECT original_price_us FROM sets WHERE id=?;", (set_id,))
        price_raw = c.fetchone()
        if price_raw is None: return None
        price = price_raw[0]
        if price is None:
            return price

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

    con = lite.connect(db)

    count = None

    if type == 'bricklink':
        with con:
            c = con.cursor()
            c.execute("SELECT SUM(bl_inventories.quantity) FROM bl_inventories "
                      " WHERE bl_inventories.set_id=?;", (set_id,))
            count = c.fetchone()[0]

    else:
        with con:
            c = con.cursor()
            c.execute("SELECT piece_count FROM sets WHERE id=?;", (set_id,))
            count = c.fetchone()[0]

    return count


def get_unique_piece_count(set_num, type=''):
    """
    Returns the unique piece count of a set by calculating it based on inventory

    @param set_num: in standard format xxxx-x
    @param type: bricklink or brickset
    @return: the number of pieces
    """
    # Get the set ID.
    set_id = get_set_id(set_num)

    con = lite.connect(db)

    count = None

    if type == 'bricklink':
        with con:
            c = con.cursor()
            c.execute("SELECT COUNT(bl_inventories.quantity) FROM bl_inventories JOIN parts"
                      " ON bl_inventories.piece_id = parts.id"
                      " WHERE bl_inventories.set_id=?;", (set_id,))
            count = c.fetchone()[0]

    return count


def get_set_weight(set_num, type=''):
    """
    Returns the weight of a set by either getting it straight from the set weight column or by
    calculating it based on inventory

    @param set_num: in standard format xxxx-x
    @param type: '' or bricklink or brickset
    @return: the weight in grams
    """
    # Get the set ID.
    set_id = get_set_id(set_num)

    con = lite.connect(db)

    weight = None

    if type == 'bricklink':
        with con:
            c = con.cursor()
            c.execute(
                "SELECT SUM(bl_inventories.quantity * parts.weight) FROM bl_inventories JOIN parts"
                " ON bl_inventories.piece_id = parts.id"
                " WHERE bl_inventories.set_id=?;", (set_id,))
            weight = c.fetchone()[0]

    else:
        with con:
            c = con.cursor()
            c.execute("SELECT set_weight FROM sets WHERE id=?;", (set_id,))
            weight = c.fetchone()[0]

    return weight


def main():
    set = input("What is the set number?: ")
    print(get_set_price(set))
    main()

# Done: 20140901 Make this menu work for this file
if __name__ == "__main__":
    def main_menu():
        """
        Main launch menu
        @return:
        """

        logger.critical("set_info.py testing")
        options = {}

        options['1'] = "Get Set ID - Returns the set id row num", menu_get_set_id
        options[
            '2'] = "Get all set years - Returns a dictionary of all the sets with their last update", menu_get_all_set_years
        options['3'] = "Get last BL update dates", menu_get_all_bl_update_years
        options['4'] = "Get last BS update dates", menu_get_all_bs_update_years
        options['5'] = "Has a set been updated today?", menu_check_last_updated_daily_stats
        options['6'] = "Get a set's price adjusted for inflation", menu_get_set_price
        options['7'] = "Get a set's piece count", menu_get_piece_count
        options['8'] = "Get a set's unique piece count", menu_get_unique_piece_count
        options['9'] = "Get a set's weight", menu_get_set_weight
        options['0'] = "Quit", menu.quit

        while True:
            result = menu.options_menu(options)
            if result is 'kill':
                exit()

    def menu_get_set_id():
        set_num = base.input_set_num()
        csvfile = get_set_id(set_num)
        print(csvfile)

    def menu_get_all_set_years():
        csvfile = get_all_set_years()
        base.print4(csvfile)

    def menu_get_all_bl_update_years():
        csvfile = get_all_bl_update_years()
        base.print4(csvfile)


    def menu_get_all_bs_update_years():
        csvfile = get_all_bs_update_years()
        base.print4(csvfile)


    def menu_check_last_updated_daily_stats():
        set_num = base.input_set_num()
        csvfile = check_last_updated_daily_stats(set_num)
        print(csvfile)


    def menu_get_set_price():
        set_num = base.input_set_num()
        csvfile = get_set_price(set_num)
        base.print4(csvfile)
        base.print4(get_set_price(set_num, 2013))


    def menu_get_piece_count():
        set_num = base.input_set_num()
        base.print4(get_piece_count(set_num))
        base.print4(get_piece_count(set_num, 'bricklink'))
        base.print4(get_piece_count(set_num, 'brickset'))


    def menu_get_unique_piece_count():
        set_num = base.input_set_num()
        base.print4(get_unique_piece_count(set_num))
        base.print4(get_unique_piece_count(set_num, 'bricklink'))
        base.print4(get_unique_piece_count(set_num, 'brickset'))

    def menu_get_set_weight():
        set_num = base.input_set_num()
        base.print4(get_set_weight(set_num))
        base.print4(get_set_weight(set_num, 'bricklink'))
        base.print4(get_set_weight(set_num, 'brickset'))


    if __name__ == "__main__":
        main_menu()


