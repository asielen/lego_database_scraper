__author__ = 'andrew.sielen'

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


def get_bl_update_years(set_num=None):
    """
    confirmed 20140904
    @return: a list of all the sets in the database that need to be updated with bricklink inventory
    """
    last_updated = None
    if set_num is None:
        last_updated = db.run_sql("SELECT set_num, last_inv_updated_bl FROM sets;")
        last_updated = base.list_to_dict(last_updated)

    else:
        last_updated = db.run_sql("SELECT set_num, last_inv_updated_bl FROM sets WHERE set_num=?;", (set_num,),
                                  one=True)
        if last_updated is not None:
            last_updated = last_updated[0]

    return last_updated


# def get_bs_update_years(set_num=None):
# """
# confirmed 20140904
# @return: a list of all the sets in the database that need to be updated with brickset inventory
#     """
#     last_updated = None
#     if set_num is None:
#         last_updated = db.run_sql("SELECT set_num, last_inv_updated_bs FROM sets;")
#         last_updated = base.list_to_dict(last_updated)
#
#     else:
#         last_updated = db.run_sql("SELECT set_num, last_inv_updated_bs FROM sets WHERE set_num=?;",(set_num,),one=True)
#         if last_updated is not None:
#             last_updated = last_updated[0]
#
#     return last_updated

def get_re_update_years(set_num=None):
    """
    confirmed 20140904
    @return: a list of all the sets in the database that need to be updated with rebrickable inventory
    """
    last_updated = None
    if set_num is None:
        last_updated = db.run_sql("SELECT set_num, last_inv_updated_re FROM sets;")
        last_updated = base.list_to_dict(last_updated)

    else:
        last_updated = db.run_sql("SELECT set_num, last_inv_updated_re FROM sets WHERE set_num=?;", (set_num,),
                                  one=True)
        if last_updated is not None:
            last_updated = last_updated[0]

    return last_updated


# #####



# # Basic information
def get_set_price(set_n=None, inf_year=None):
    """
    updated 20140908
    @param set_n: set num in xxxx–x
    @param inf_year: if this is not None, then get the original price
    @return: the price or list of prices if set_n is omitted
    """
    price = None
    if set_n is not None:
        set_id = get_set_id(set_n)
        if set_id is None: return None

        price_raw = db.run_sql("SELECT original_price_us FROM sets WHERE id=?;", (set_id,), one=True)
        if price_raw is None:
            return None
        price = price_raw[0]

        if inf_year is not None and price is not None:
            year_raw = db.run_sql("SELECT year_released FROM sets WHERE id=?;", (set_id,), one=True)
            if year_raw is None:
                return None
            year_released = year_raw[0]
            if inf_year >= year_released:
                return price
            price_inflated = (get_inflation_rate(year_released, inf_year) * price) + price
            return price_inflated, year_released, inf_year
        else:
            return price

    else:
        # if there is a an inflation year but no set specified. Get all sets from before this year and return their adjusted prices
        if inf_year is not None:
            prices_raw = db.run_sql(
                "SELECT set_num, original_price_us, year_released FROM sets WHERE set_num IS NOT NULL AND original_price_us IS NOT NULL AND year_released <= ?;",
                (inf_year,))
            prices = []
            for s in prices_raw:
                prices.append((s[0], (get_inflation_rate(s[2], inf_year) * s[1]) + s[1], s[2], inf_year))
            return prices
        else:
            # if there isn't a set specified or a inf_year specified, just return all set prices
            prices_raw = db.run_sql(
                "SELECT set_num, original_price_us FROM sets WHERE set_num IS NOT NULL AND original_price_us IS NOT NULL;")
            return prices_raw


# #More Advanced Calculations
# TODO: Make sure this works with the new database structure
def get_piece_count(set_n=None, type=''):
    """


    Returns the piece count of a set by either getting it straight from the piece count column or by
    calculating it based on inventory

    @param set_n: in standard format xxxx-x
    @param type: '' or bricklink or brickset
    @return: the number of pieces
    """
    # Get the set ID.

    if set_n is not None:
        set_id = get_set_id(set_n)
        if set_id is None: return None

        if type == 'bricklink':
            count = db.run_sql("SELECT SUM(bl_inventories.quantity) FROM bl_inventories "
                               " WHERE bl_inventories.set_id=?;", (set_id,), one=True)
            count = count[0]

        else:
            count = db.run_sql("SELECT piece_count FROM sets WHERE id=?;", (set_id,), one=True)
            count = count[0]

    else:
        if type == 'bricklink':
            count = db.run_sql("SELECT set_num, pieces FROM sets AS S JOIN (SELECT set_id, SUM(quantity) AS pieces "
                               "FROM bl_inventories GROUP BY set_id) AS P ON S.id = P.set_id;")
        else:
            count = db.run_sql("SELECT set_num, piece_count FROM sets;")

    return count


# TODO: Make this work with rebrickable inventories
def get_unique_piece_count(set_num=None, type=''):
    """
    Returns the unique piece count of a set by calculating it based on inventory

    @param set_num: in standard format xxxx-x
    @param type: bricklink or brickset
    @return: the number of pieces
    """

    if set_num is not None:
        set_id = get_set_id(set_num)
        count = db.run_sql("SELECT COUNT(bl_inventories.quantity) FROM bl_inventories JOIN parts"
                           " ON bl_inventories.piece_id = parts.id"
                           " WHERE bl_inventories.set_id=?;", (set_id,), one=True)
        count = count[0]
    else:
        count = db.run_sql("SELECT set_num, unique_pieces FROM sets AS S JOIN (SELECT bl_inventories.set_id, "
                           "COUNT(bl_inventories.quantity) AS unique_pieces FROM bl_inventories "
                           "JOIN parts ON bl_inventories.piece_id = parts.id GROUP BY bl_inventories.set_id) "
                           "AS U ON S.id = U.set_id")

    return count


# TODO: Make sure piece weight is being imported correctly
def get_set_weight(set_num=None, type=''):
    """
    Returns the weight of a set by either getting it straight from the set weight column or by
    calculating it based on inventory

    @param set_num: in standard format xxxx-x
    @param type: '' or bricklink
    @return: the weight in grams
    """
    weight = None
    if set_num is not None:
        set_id = get_set_id(set_num)

        if type == 'bricklink':
            weight = db.run_sql("SELECT SUM(bl_inventories.quantity * parts.weight) FROM bl_inventories JOIN parts"
                                " ON bl_inventories.piece_id = parts.id"
                                " WHERE bl_inventories.set_id=?;", (set_id,), one=True)
            weight = weight[0]

        else:
            weight = db.run_sql("SELECT set_weight FROM sets WHERE id=?;", (set_id,), one=True)
            weight = weight[0]

    else:
        weight = db.run_sql("SELECT set_num, cset_weight, set_weight FROM sets AS S "
                            "JOIN (SELECT bl_inventories.set_id, SUM(bl_inventories.quantity * parts.weight) "
                            "AS cset_weight FROM bl_inventories JOIN parts ON bl_inventories.piece_id = parts.id "
                            "GROUP BY bl_inventories.set_id) AS W ON S.id = W.set_id;")

    return weight

def get_set_dump(set_num):
    """
    Get a string + list of all set variables
    @param set_num:
    @return:
    """
    if set_num is None: return None

    set_info = db.run_sql("SELECT * FROM sets WHERE set_num=?", (set_num,), one=True)
    # set_info = set_info[0]
    # Todo, turn this into a class
    set_id = set_info[0]
    set_name = set_info[5]
    set_theme = set_info[6]
    set_sub_theme = set_info[7]
    set_piece_count = set_info[8]
    set_figures = set_info[9]
    set_weight = set_info[10]
    set_year_released = set_info[11]
    set_date_released_us = set_info[12]
    set_date_ended_us = set_info[13]
    set_date_released_uk = set_info[14]
    set_date_ended_uk = set_info[15]
    set_original_price_us = set_info[16]
    set_original_price_uk = set_info[17]
    set_age_low = set_info[18]
    set_age_high = set_info[19]
    set_box_size = set_info[20]
    set_box_volume = set_info[21]
    set_last_updated = set_info[22]
    set_last_inv_updated_bl = set_info[24]
    set_last_inv_updated_re = set_info[25]
    set_last_price_updated = set_info[26]

    set_calc_price = get_set_price(set_num, 2014)
    set_calc_pieces = get_piece_count(set_num, 'bricklink')
    set_calc_unique_pieces = get_unique_piece_count(set_num)
    set_calc_weight = get_set_weight(set_num, 'bricklink')

    print("{0}-###################-{0}".format(set_id))
    print("Set: {} | {}".format(set_num, set_name))
    print("Theme: {} - {}".format(set_theme, set_sub_theme))
    print("Ages: {} to {}".format(set_age_low, set_age_high))
    print("Released US: {} - From {} to {}".format(set_year_released, set_date_released_us, set_date_ended_us))
    print("Released UK: {} - From {} to {}".format(set_year_released, set_date_released_uk, set_date_ended_uk))
    print("Pieces/Figures: {} / {} - Calc: [{}] / Uni: [{}]".format(set_piece_count, set_figures, set_calc_pieces,
                                                                    set_calc_unique_pieces))
    print("Weight: {} - Calc: [{}]".format(set_weight, set_calc_weight))
    print("Price: {} USD / {} GBP - Adj: [{}] USD".format(set_original_price_us, set_original_price_uk, set_calc_price))
    if set_piece_count is not None and set_calc_price is not None and set_piece_count > 0:
        print("PPP: Original {} - Adjusted: {}".format(set_original_price_us / set_piece_count,
                                                       set_calc_price / set_piece_count))
    if set_weight is not None and set_calc_price is not None and set_weight > 0:
        print("PPG: Original {} - Adjusted: {}".format(set_original_price_us / set_weight, set_calc_price / set_weight))
    print("Box Size: {} - Box Volume {}".format(set_box_size, set_box_volume))
    print("Last Updated: {}".format(set_last_updated))
    print("Inventory Last Updated: BL {} / RE {}".format(set_last_inv_updated_bl, set_last_inv_updated_re))
    print("Daily Pricing Last Updated: {}".format(set_last_price_updated))
    print("{0}-###################-{0}".format(set_id))


if __name__ == "__main__":
    from navigation import menu

    def main_menu():

        logger.critical("get_set_info.py testing")
        options = {}

        options['0'] = "Get Set ID", menu_get_set_id
        options['1'] = "Get all set Years", menu_get_all_set_years
        options['2'] = "Get the date a set was last updated", menu_get_last_updated_for_daily_stats
        options['3'] = "Filter a list of sets by dates", menu_filter_list_on_dates
        options['4'] = "Get last BL update list", menu_get_bl_update_years
        options['5'] = "Has a set been updated today?", menu_get_re_update_years
        options['6'] = "Get a set's price adjusted for inflation", menu_get_set_price
        options['7'] = "Get a set's piece count", menu_get_piece_count
        options['8'] = "Get a set's unique piece count", menu_get_unique_piece_count
        options['9'] = "Get a set's weight", menu_get_set_weight
        options['A'] = "Get a quick overview of a set", menu_get_set_dump
        options['Q'] = "Quit", menu.quit

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


    def menu_get_bl_update_years():
        set_num = base.input_set_num()
        print(get_bl_update_years(set_num))
        base.print4(get_bl_update_years())


    def menu_get_re_update_years():
        set_num = base.input_set_num()
        print(get_re_update_years(set_num))
        base.print4(get_re_update_years())


    def menu_get_set_price():
        set_num = base.input_set_num()
        print(get_set_price(set_num))
        base.print4(get_set_price(set_num, 2013))
        base.print4(get_set_price())
        base.print4(get_set_price(None, 2010))

    def menu_get_piece_count():
        set_num = base.input_set_num()
        print(get_piece_count(set_num))
        base.print4(get_piece_count(set_num, 'bricklink'))
        base.print4(get_piece_count())
        base.print4(get_piece_count(None, 'bricklink'))


    def menu_get_unique_piece_count():
        set_num = base.input_set_num()
        base.print4(get_unique_piece_count(set_num))
        base.print4(get_unique_piece_count())

    def menu_get_set_weight():
        set_num = base.input_set_num()
        base.print4(get_set_weight(set_num))
        base.print4(get_set_weight(set_num, 'bricklink'))
        base.print4(get_set_weight())

    def menu_get_set_dump():
        set_num = base.input_set_num()
        get_set_dump(set_num)


    if __name__ == "__main__":
        main_menu()