#External
import sqlite3 as lite

#interla
import arrow
import database as db
import system as syt


# Todo: Make this all work with the new database structure

# ### General Database information
def get_sets_between_years(start_year, end_year=None):
    """

    @param start_year:
    @param end_year:
    @return: returns all the _set ids between start_year and end_year
    """

    if start_year is None: return None

    # Can be used to get all sets from a single year
    if end_year is None:
        end_year = start_year

    con = lite.connect(db.database)

    with con:
        c = con.cursor()
        c.execute("SELECT set_num FROM sets WHERE year_released BETWEEN ? AND ?;", (start_year, end_year))
        sets_raw = c.fetchall()
        sets = syt.flatten_list(sets_raw)

    return sets


def get_set_year_range():
    """
    @return: A tuple with the first and last years in the database
    """

    min_year = None
    max_year = None
    con = lite.connect(db.database)

    with con:
        c = con.cursor()
        c.execute("SELECT MIN(year_released) FROM sets;")
        min_year = c.fetchone()[0]

        c.execute("SELECT MAX(year_released) FROM sets;")
        max_year = c.fetchone()[0]

    return min_year, max_year


def get_sets_by_year():
    """

    @return: A dictionary with the number of sets per year
    """
    years = []

    con = lite.connect(db.database)
    with con:
        c = con.cursor()
        c.execute("SELECT year_released, COUNT(set_num) AS NumberOfSets FROM sets GROUP BY year_released;")
        years = c.fetchall()

    return years


def get_sets_by_theme():
    """

    @return: A dictionary with the number of sets per theme
    """
    themes = []

    con = lite.connect(db.database)
    with con:
        c = con.cursor()
        c.execute("SELECT theme, COUNT(set_num) AS NumberOfSets FROM sets GROUP BY theme;")
        themes = c.fetchall()

    return themes


def get_number_of_sets():
    """

    @return: The number of sets in the database
    """
    set_num = 0

    con = lite.connect(db.database)
    with con:
        c = con.cursor()
        c.execute("SELECT COUNT(set_num) FROM sets")
        set_num = c.fetchone()[0]

    return set_num


def get_bl_category_id(category_num):
    """
    @param category_num: the category num used by bricklink
    @return: the primary key for a category in the database
    """

    element_id = None
    con = lite.connect(db.database)
    with con:
        c = con.cursor()
        c.execute('SELECT id FROM bl_categories WHERE bl_category_id=?', (category_num,))
        element_id_raw = c.fetchone()
        if element_id_raw is None:
            return None
        element_id = element_id_raw[0]

    return element_id


def read_bl_categories():
    """

    @return: a list in this format [category_id, id]
    """
    return syt.list_to_dict(db.run_sql('SELECT bl_category_id, id FROM bl_categories'))


def read_bl_colors():
    """

    @return: a list in this format {color_id, id}
    """
    return syt.list_to_dict(db.run_sql('SELECT bl_color_id, id FROM colors'))


def read_re_colors():
    """

    @return: a list in this format {color_id, id}
    """
    return syt.list_to_dict(db.run_sql('SELECT re_color_id, id FROM colors'))


def read_bl_colors_name():
    """

    @return: a list in this format {color_name, id}
    """
    return syt.list_to_dict(db.run_sql('SELECT bl_color_name, id FROM colors'))


def read_bl_price_types():
    """

    @return: a dict in this format {price_id: id}
    """
    return syt.list_to_dict(db.run_sql('SELECT price_type, id FROM price_types'))


def read_bl_sets():
    """

    @return: a dict in this format {set_num: [_set]}
    """
    bl_set_list = db.run_sql('SELECT * FROM sets')
    return {b[1]: b[:] for b in bl_set_list}  # 1 is the position of the bricklink column


def read_bl_set_id_num():
    """

    @return: a list in this format {id: set_num}
    """
    bl_set_list = db.run_sql('SELECT * FROM sets')
    return {b[0]: b[1] for b in bl_set_list}  # 1 is the position of the bricklink column


def read_bl_set_num_id():
    """

    @return: a list in this format {set_num: id}
    """
    bl_set_list = db.run_sql('SELECT * FROM sets')
    return {b[1]: b[0] for b in bl_set_list}  # 1 is the position of the bricklink column


def read_inv_update_date(date='last_updated'):
    """

    @param date: last_updated,
    @return: a list in the format {set_num: last_updated} for the date _type in list:
        # last_updated pos = 22
        # last_inv_updated_bo = 23
        # last_inv_updated_bl = 24
        # last_inv_updated_re = 25
        # last_price_updated = 26
    """
    date_list = db.run_sql('SELECT * FROM sets')
    date_pos = 22
    if date == 'last_inv_updated_bo':
        date_pos = 23
    elif date == 'last_inv_updated_bl':
        date_pos = 24
    elif date == 'last_inv_updated_re':
        date_pos = 25
    elif date == 'last_price_updated':
        date_pos = 26
    return {b[1]: b[date_pos] for b in date_list}


def read_bl_invs():
    """

    @return: a list of the sets who's inventory is in the system
    """
    bl_set_list = db.run_sql('SELECT * FROM bl_inventories')
    bl_set_list = set(b[1] for b in bl_set_list)
    return bl_set_list


def read_re_invs():
    """

    @return: a list of the sets who's inventory is in the system
    """
    re_set_list = db.run_sql(
        'SELECT DISTINCT sets.set_num FROM re_inventories JOIN sets ON re_inventories.set_id = sets.id')
    re_set_list = set(b[0] for b in re_set_list)
    return re_set_list


def read_bl_parts():
    """

    @return: a dict in this format {part_num: id, }
    """
    return syt.list_to_dict(db.run_sql('SELECT bricklink_id, id FROM parts'))


def read_re_parts():
    """

    @return: a dict in this format {part_num: id, }
    """
    return syt.list_to_dict(db.run_sql('SELECT rebrickable_id, id FROM parts'))


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
            update.append((s[0], syt.check_if_the_same_day(today, s[1])))
        update = syt.list_to_dict(update)
    else:
        last_updated_raw = db.run_sql("SELECT last_price_updated FROM sets WHERE set_num=?", (set_num,), one=True)

        if last_updated_raw is None:
            update = False
        # last_updated = last_updated_raw[0]
        update = syt.check_if_the_same_day(today, last_updated_raw)

    return update


#
# def filter_list_on_dates(sets, year_sets, date_range=180):
#     """
#         Take a list of sets and a dictionary of sets and dates and returns a list of sets
#         that are only within [get_date_range] of today
    # Used to check if a _set needs to be updated
#             Need to get the first two lists though from somewhere else
#     @param sets: list of _set nums [xxx–xx,yyy–y,zzz–z]
    #     @param year_sets: dict of a list of sets with last updated dates {xxx–x:2014-05-12}
#     @param date_range: the number of days on either side of the date
#     @return: a list of sets that need to be updated
#     """
#     result = []
#
#     today = arrow.now()
#     past = today.replace(days=-date_range)
#
#     for s in sets:
#         if s in year_sets:
#             if syt.check_in_date_rangeA(arrow.get(year_sets[s]), past, today):
#                 continue
#         result.append(s)
#
#     return result

#
# def get_bl_update_years(set_num=None):
#     """
#     confirmed 20140904
#     @return: a list of all the sets in the database that need to be updated with bricklink inventory
#     """
#     last_updated = None
#     if set_num is None:
#         last_updated = db.run_sql("SELECT set_num, last_inv_updated_bl FROM sets;")
#         last_updated = syt.list_to_dict(last_updated)
#
#     else:
#         last_updated = db.run_sql("SELECT set_num, last_inv_updated_bl FROM sets WHERE set_num=?;", (set_num,),
#                                   one=True)
#         # if last_updated is not None:
#         # last_updated = last_updated[0]
#
#     return last_updated


# def get_bs_update_years(set_num=None):
# """
# confirmed 20140904
# @return: a list of all the sets in the database that need to be updated with brickset inventory
# """
# last_updated = None
# if set_num is None:
#         last_updated = db.run_sql("SELECT set_num, last_inv_updated_bs FROM sets;")
#         last_updated = syt.list_to_dict(last_updated)
#
#     else:
#         last_updated = db.run_sql("SELECT set_num, last_inv_updated_bs FROM sets WHERE set_num=?;",(set_num,),one=True)
#         if last_updated is not None:
#             last_updated = last_updated[0]
#
#     return last_updated
#
# def get_re_update_years(set_num=None):
#     """
#     confirmed 20140904
#     @return: a list of all the sets in the database that need to be updated with rebrickable inventory
#     """
#     last_updated = None
#     if set_num is None:
#         last_updated = db.run_sql("SELECT set_num, last_inv_updated_re FROM sets;")
#         last_updated = syt.list_to_dict(last_updated)
#
#     else:
#         last_updated = db.run_sql("SELECT set_num, last_inv_updated_re FROM sets WHERE set_num=?;", (set_num,),
#                                   one=True)
#         # if last_updated is not None:
#         #     last_updated = last_updated[0]
#
#     return last_updated
#

# # # Basic information
# def get_set_price(set_num=None, _inf_year=None):
    # """
    #     updated 20140908
#     @param set_num: _set num in xxxx–x
    # @param _inf_year: if this is not None, then get the original price
    #     @return: the price or list of get_prices if set_num is omitted
#     """
#     price = None
#
#     # Single Set Lookup
#     if set_num is not None:
#
#         set_id = get_set_id(set_num)
#         if set_id is None: return None
#
#         price = db.run_sql("SELECT original_price_us FROM sets WHERE id=?;", (set_id,), one=True)
#         if price is None:
#             return None
#
#         if _inf_year is not None and price is not None:
    #             year_released = db.run_sql("SELECT year_released FROM sets WHERE id=?;", (set_id,), one=True)
#             if year_released is None:
#                 return None
#             if _inf_year >= year_released:
    #                 return price
#             price_inflated = (syt.get_inflation_rate(year_released, _inf_year) * price) + price
    # return price_inflated, year_released, _inf_year
    #         else:
    #             return price
#
#     # All Set lookup
#     else:
#         # if there is a an inflation year but no _set specified. Get all sets from before this year and return their adjusted get_prices
    # if _inf_year is not None:
    #             prices_raw = db.run_sql(
#                 "SELECT set_num, original_price_us, year_released FROM sets WHERE set_num IS NOT NULL AND original_price_us IS NOT NULL AND year_released <= ?;",
#                 (_inf_year,))
#             prices = []
    #             for s in prices_raw:
#                 prices.append((s[0], (syt.get_inflation_rate(s[2], _inf_year) * s[1]) + s[1], s[2], _inf_year))
    # return prices
    #         else:
#             # if there isn't a _set specified or a _inf_year specified, just return all _set get_prices
    # prices_raw = db.run_sql(
    #                 "SELECT set_num, original_price_us FROM sets WHERE set_num IS NOT NULL AND original_price_us IS NOT NULL;")
#             return prices_raw
#

# #More Advanced Calculations


# #Historic Info
# def get_historic_prices(set_num=None, set_id=None):
#     """
#     Get historic get_prices
#     @param set_num: in format xxxx-xx
#     @return: This format: id, set_num, record_date, price_type, lots, qty, min, max, avg, qty_avg, price_avg
#     """
#     if set_num is None and set_id is None: return None
#     if set_id is None:
#         set_id = get_set_id(set_num)
#     prices = db.run_sql("SELECT historic_prices.id, sets.set_num, historic_prices.record_date, price_types.price_type, "
#                         "historic_prices.lots, historic_prices.qty, historic_prices.min, historic_prices.max,"
#                         "historic_prices.avg, historic_prices.qty_avg, historic_prices.piece_avg "
#                         "FROM historic_prices "
#                         "JOIN sets ON (sets.id=historic_prices.set_id) "
#                         "JOIN price_types ON (price_types.id=historic_prices.price_type) "
#                         "WHERE historic_prices.set_id=?", (set_id,))
#     return prices

#
# def get_historic_data(set_num=None, set_id=None):
#     """
#     Get historic bs data
#     @param set_num: in format xxxx-xx
#     @return:
#     """
#     if set_num is None and set_id is None: return None
#     if set_id is None:
#         set_id = get_set_id(set_num)
#     ratings = db.run_sql(
#         "SELECT bs_ratings.id, sets.set_num, bs_ratings.record_date, want, own, _rating FROM bs_ratings "
    #         "JOIN sets ON (sets.id=bs_ratings.set_id) WHERE bs_ratings.set_id=?", (set_id,))
#     return ratings

#
# def get_set_dump(set_num):
#     """
#     Get a string + list of all _set variables
#     @param set_num:
    # @return:
    #     """
    #     if set_num is None: return None
#
#     set_info = db.run_sql("SELECT * FROM sets WHERE set_num=?", (set_num,))
#     set_info = set_info[0]

#     set_id = set_info[0]
#     set_name = set_info[5]
#     set_theme = set_info[6]
#     set_sub_theme = set_info[7]
#     set_piece_count = set_info[8]
#     set_figures = set_info[9]
#     set_weight = set_info[10]
#     set_year_released = set_info[11]
#     set_date_released_us = syt.get_date(set_info[12])
#     set_date_ended_us = syt.get_date(set_info[13])
#     set_date_released_uk = syt.get_date(set_info[14])
#     set_date_ended_uk = syt.get_date(set_info[15])
#     set_original_price_us = set_info[16]
#     set_original_price_uk = set_info[17]
#     set_age_low = set_info[18]
#     set_age_high = set_info[19]
#     set_box_size = set_info[20]
#     set_box_volume = set_info[21]
#     set_last_updated = syt.get_date(set_info[22])
#     set_last_inv_updated_bl = syt.get_date(set_info[24])
#     set_last_inv_updated_re = syt.get_date(set_info[25])
#     set_last_price_updated = syt.get_date(set_info[26])
#
#     set_calc_price = get_set_price(set_num, 2014)
#     set_calc_pieces = get_piece_count(set_num, 'bricklink')
#     set_calc_unique_pieces = get_unique_piece_count(set_num)
#     set_calc_weight = get_set_weight(set_num, 'bricklink')
#
#     print("{0}-###################-{0}".format(set_id))
#     print("Set: {} | {}".format(set_num, set_name))
#     print("Theme: {} - {}".format(set_theme, set_sub_theme))
#     print("Ages: {} to {}".format(set_age_low, set_age_high))
#     print("Released US: {} - From {} to {}".format(set_year_released, set_date_released_us, set_date_ended_us))
#     print("Released UK: {} - From {} to {}".format(set_year_released, set_date_released_uk, set_date_ended_uk))
#     print("Pieces/Figures: {} / {} - Calc: [{}] / Uni: [{}]".format(set_piece_count, set_figures, set_calc_pieces,
#                                                                     set_calc_unique_pieces))
#     print("Weight: {} - Calc: [{}]".format(set_weight, set_calc_weight))
#     print("Price: {} USD / {} GBP - Adj: [{}] USD".format(set_original_price_us, set_original_price_uk, set_calc_price))
#     if set_piece_count is not None and set_calc_price is not None and set_piece_count > 0:
#         print("PPP: Original {} - Adjusted: {}".format(set_original_price_us / set_piece_count,
#                                                        set_calc_price / set_piece_count))
#     if set_weight is not None and set_calc_price is not None and set_weight > 0:
#         print("PPG: Original {} - Adjusted: {}".format(set_original_price_us / set_weight, set_calc_price / set_weight))
#     print("Box Size: {} - Box Volume {}".format(set_box_size, set_box_volume))
#     print("Last Updated: {}".format(set_last_updated))
#     print("Inventory Last Updated: BL {} / RE {}".format(set_last_inv_updated_bl, set_last_inv_updated_re))
#     print("Daily Pricing Last Updated: {}".format(set_last_price_updated))
#     print("{0}-###################-{0}".format(set_id))

#
# if __name__ == "__main__":
#     from navigation import menu
#
#     def main_menu():
#
#         syt.log_critical("get_set_info.py testing")
#         options = (
#             ("Get Set ID", menu_get_set_id),
#             ("Get all _set Years", menu_get_all_set_years),
#             ("Get the date a _set was last updated", menu_get_last_updated_for_daily_stats),
    #             ("Filter a list of sets by dates", menu_filter_list_on_dates),
#             ("Get last BL update list", menu_get_bl_update_years),
#             ("Has a _set been updated today?", menu_get_re_update_years),
    # ("Get a _set's price adjusted for inflation", menu_get_set_price),
    #             ("Get a _set's piece count", menu_get_piece_count),
    #             ("Get a _set's unique piece count", menu_get_unique_piece_count),
    #             ("Get a _set's weight", menu_get_set_weight),
    #             ("Get Historic Prices", menu_get_historic_prices),
    #             ("Get Historic BS Data", menu_get_historic_data),
#             ("Get a quick overview of a _set", menu_get_set_dump)
#         )
    #         syt.Menu(name="– get_set_info.py testing –", choices=options)
#
#     def menu_get_set_id():
#         set_num = si.input_set_num()
#         print(get_set_id(set_num))
#         print(get_set_info(set_num))
#         syt.print4(get_set_id())
#
#     def menu_get_all_set_years():
#         set_num = si.input_set_num()
#         print(get_all_set_years(set_num))
#         syt.print4(get_all_set_years())
#
#     def menu_get_last_updated_for_daily_stats():
#         set_num = si.input_set_num()
#         if set_num == '-1': set_num = None
#         print(get_last_updated_for_daily_stats(set_num))
#         syt.print4(get_last_updated_for_daily_stats())
#
#     def menu_filter_list_on_dates():
#         # Todo: 20140908 figure out how to test
#         print("Not sure how to test this")
#
#
#     def menu_get_bl_update_years():
#         set_num = si.input_set_num()
#         print(get_bl_update_years(set_num))
#         syt.print4(get_bl_update_years())
#
#
#     def menu_get_re_update_years():
#         set_num = si.input_set_num()
#         print(get_re_update_years(set_num))
#         syt.print4(get_re_update_years())
#
#
#     def menu_get_set_price():
#         set_num = si.input_set_num()
#         print(get_set_price(set_num))
#         print(get_set_price(set_num, 2013))
#         syt.print4(get_set_price())
#         syt.print4(get_set_price(None, 2010))
#
#     def menu_get_piece_count():
#         set_num = si.input_set_num()
#         print(get_piece_count(set_num))
#         syt.print4(get_piece_count(set_num, 'bricklink'))
#         syt.print4(get_piece_count())
#         syt.print4(get_piece_count(None, 'bricklink'))
#
#
#     def menu_get_unique_piece_count():
#         set_num = si.input_set_num()
#         syt.print4(get_unique_piece_count(set_num))
#         syt.print4(get_unique_piece_count())
#
#     def menu_get_set_weight():
#         set_num = si.input_set_num()
#         syt.print4(get_set_weight(set_num))
#         syt.print4(get_set_weight(set_num, 'bricklink'))
#         syt.print4(get_set_weight())
#
#     def menu_get_historic_prices():
#         set_num = si.input_set_num()
#         prices = get_historic_prices(set_num)
#         syt.print4(prices)
#
#     def menu_get_historic_data():
#         set_num = si.input_set_num()
#         data = get_historic_data(set_num)
#         syt.print4(data)
#
#     def menu_get_set_dump():
#         set_num = si.input_set_num()
#         get_set_dump(set_num)
#
#
#     if __name__ == "__main__":
#         main_menu()