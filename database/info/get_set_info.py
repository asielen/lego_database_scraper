__author__ = 'andrew.sielen'

import sqlite3 as lite

import arrow

from system.calculate_inflation import get_inflation_rate
import database as db
from system import base_methods as base
from system import logger



# # Basic Functions
def get_set_id(set_num=None):
    """
    @param set_num:
    @param add: if True, Add the set if it is missing in the database
    @return: the id column num of the set in the database, or a list of all set ids with set num if no set num is provided
    """
    if set_num is None:
        set_id_raw = db.run_sql('SELECT set_num, id FROM sets')
    else:
        set_id_raw = db.run_sql('SELECT id FROM sets WHERE set_num=?', (set_num.lower(),), one=True)
        if set_id_raw is not None:
            set_id_raw = set_id_raw[0]

    return set_id_raw


# These three functions return lists of sets that need to be updated
def get_all_set_years(set_num=None):
    """
    # Todo: 20140908 Test with new functionality of returning a single date or multiple dates
    confirmed 20140904

    @return: a dictionary of all the sets in the database with the last date they were updated
    in the format {xxxx-y:[Date as text string Linux format],xxx-yy:DATE}
    """
    last_updated = None
    if set_num is None:
        last_updated_raw = db.run_sql("SELECT set_num, last_updated FROM sets;")
        last_updated = base.list_to_dict(last_updated_raw)
    else:
        last_updated_raw = db.run_sql("SELECT last_updated FROM sets WHERE set_num=?;", (set_num,), one=True)
        if last_updated_raw is not None:
            last_updated = last_updated_raw[0]
    return last_updated


# Functions for figuring out what needs to be updated
def get_last_updated_for_daily_stats(set_num=None):
    """

    @param set_num: in standard format xxxx-x
    @return: True if updated today, False otherwise;
            or if no set_num was provided it returns a list of sets with True or False
    """
    today = arrow.now()
    update = None
    if set_num is None:
        last_updated_raw = db.run_sql("SELECT set_num, last_price_updated FROM sets")
        update = []
        for s in last_updated_raw:
            update.append((s[0], base.check_if_the_same_day(today, s[1])))
    else:
        last_updated_raw = db.run_sql("SELECT last_price_updated FROM sets WHERE set_num=?", (set_num,), one=True)

        if last_updated_raw is None:
            update = False
        last_updated = last_updated_raw[0]
        update = base.check_if_the_same_day(today, last_updated)

    return update


# Todo: 20140908 figure out how to test
def filter_list_on_dates(sets, year_sets, date_range=180):
    """
        Take a list of sets and a dictionary of sets and dates and returns a list of sets
        that are only within [date_range] of today
            Used to check if a set needs to be updated
            Need to get the first two lists though from somewhere else
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
            if base.check_in_date_rangeA(arrow.get(year_sets[s]), past, today):
                continue
        result.append(s)

    return result


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


# #####



# # Basic information
# TODO: Make sure this works with the new database structure
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


# TODO: Make sure this works with the new database structure
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
    set = base.input_set_num()
    print("Calculated: {}".format(get_piece_count(set, 'bricklink')))
    print("Reported: {}".format(get_piece_count(set, '')))
    print("Unique: {}".format(get_unique_piece_count(set, 'bricklink')))
    main()


if __name__ == "__main__":
    from navigation import menu

    def main_menu():

        logger.critical("get_set_info.py testing")
        options = {}

        options['1'] = "Get Set ID", menu_get_set_id
        options['2'] = "Get all set Years", menu_get_all_set_years
        options['2'] = "Get the date a set was last updated", menu_get_last_updated_for_daily_stats
        options['3'] = "Filter a list of sets by dates", menu_filter_list_on_dates
        options['4'] = "Get last BS update dates", menu_get_all_bs_update_years
        options['5'] = "Has a set been updated today?", menu_check_last_updated_daily_stats
        options['6'] = "Get a set's price adjusted for inflation", menu_get_set_price
        options['7'] = "Get a set's piece count", menu_get_piece_count
        options['9'] = "Quit", menu.quit

        while True:
            result = menu.options_menu(options)
            if result is 'kill':
                exit()

    def menu_get_set_id():
        set_num = base.input_set_num()
        print(get_set_id(set_num))
        base.print4(get_set_id())

    def menu_get_all_set_years():
        set_num = base.input_set_num()
        print(get_all_set_years(set_num))
        base.print4(get_all_set_years())

    def menu_get_last_updated_for_daily_stats():
        set_num = base.input_set_num()
        print(get_last_updated_for_daily_stats(set_num))
        base.print4(get_last_updated_for_daily_stats())

    def menu_filter_list_on_dates():
        # Todo: 20140908 figure out how to test
        print("Not sure how to test this")


    def menu_get_all_bs_update_years():
        csvfile = 2  # get_all_bs_update_years()
        base.print4(csvfile)


    def menu_check_last_updated_daily_stats():
        set_num = base.input_set_num()
        csvfile = get_last_updated_for_daily_stats(set_num)
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