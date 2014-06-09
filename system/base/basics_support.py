from system.base_methods import LBEF

__author__ = 'andrew.sielen'

# external
import logging
import arrow


# other module
from public_api.basics import add_bl_inventory_to_database


def get_all_basestats(set_list, force=0):
    """

    @param set_list: a list of set_nums acquired either though sql or a text file
    @return:
    """
    # TODO: Rewrite this to use multiprocess
    if set_list is not None:
        if force == 0:
            filtered_set_list = _get_and_filter_sets_by_year(set_list)
            total = len(filtered_set_list)
        else:
            filtered_set_list = set_list
            total = len(set_list)

        bl_designs_in_database = _get_and_filter_sets_blinv_by_year(set_list)
        bs_elements_in_database = _get_and_filter_sets_bsinv_by_year(set_list)

        finished = len(set_list) - total
        logging.info("Starting at {}% of total list –– [ {} / {} ]".format(round((finished / len(set_list)) * 100, 2),
                                                                           finished, len(set_list)))
        # Update basestats
        for idx, set in enumerate(filtered_set_list):
            logging.info("[ {0}/{1} {2}% ] Getting info on {3}".format(idx, total, round((idx / total) * 100, 2), set))
            basics.add_set_to_database(set)

        # Update bricklink inventories
        logging.info("Updating bricklink inventories for {} sets".format(len(bl_designs_in_database)))
        for idx, set in enumerate(bl_designs_in_database):
            logging.info("{0} Getting bl inventory on {1}".format(idx, set))
            add_bl_inventory_to_database(set, bl_designs_in_database)

        # Update brickset inventories
        logging.info("Updating brickset inventories for {} sets".format(len(bs_elements_in_database)))
        for idx, set in enumerate(bs_elements_in_database):
            logging.info("{0} Getting bs inventory on {1}".format(idx, set))
            get_bs_inventory(set, bs_elements_in_database)


def _get_and_filter_sets_by_year(set_list):
    return filter_list_on_dates(set_list, get_all_set_years())


def _get_and_filter_sets_blinv_by_year(set_list):
    return filter_list_on_dates(set_list, get_all_bl_update_years())


def _get_and_filter_sets_bsinv_by_year(set_list):
    return filter_list_on_dates(set_list, get_all_bs_update_years())


def filter_list_on_dates(sets, year_sets, date_range=180):
    """

    @param sets: list of setnums [xxx–xx,yyy–y,zzz–z]
    @param year_set: dict of a list of sets with last updated dates {xxx–x:2014-05-12}
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


# These three functions return lists of sets that need to be updated
def get_all_set_years():
    """

    @return: a dictionary of all the sets in the database with the last date they were updated
    """
    con = lite.connect(database)
    with con:
        c = con.cursor()
        c.execute("SELECT set_num, last_updated FROM sets;")
        last_updated = c.fetchall()

    if last_updated is None:
        return {}

    return {t[0]: t[1] for t in last_updated}  # convert from list of lists to a dictionary


def get_all_bl_update_years():
    """

    @return: a list of all the sets in the database that need to be updated with bricklink inventory
    """
    con = lite.connect(database)
    with con:
        c = con.cursor()
        c.execute("SELECT set_num, last_inv_updated_bl FROM sets;")
        last_updated = c.fetchall()

    if last_updated is None:
        return {}

    return {t[0]: t[1] for t in last_updated}  # convert from list of lists to a dictionary


def get_all_bs_update_years():
    """

    @return: a list of all the sets in the database that need to be updated with brickset inventory
    """
    con = lite.connect(database)
    with con:
        c = con.cursor()
        c.execute("SELECT set_num, last_inv_updated_bs FROM sets;")
        last_updated = c.fetchall()

    if last_updated is None:
        return {}

    return {t[0]: t[1] for t in last_updated}  # convert from list of lists to a dictionary
