from apis.bricklink_api import bricklink_set_data_scrape as BL

__author__ = 'andrew.sielen'

import logging
import arrow

import LBEF
from base_methods.basics import get_bl_inventory
from scrapers import brickset_set_data as BS


def get_basestats(set, type=0):
    """

    @param set: set num in standard format xxxx-x
    @return: dictionary of set information
    """

    if set is None:
        logging.warning("Trying to update a set but there is none to update")
        return None

    set_num, set_seq, set = LBEF.expand_set_num(set)

    scrubbed_dic = {}

    brickset_stats = BS.get_basestats(set_num, set_seq)
    bricklink_stats = BL.get_basestats(set_num, set_seq)

    if 'set_name' in brickset_stats:
        if brickset_stats['set_name'] == '': return None
        scrubbed_dic['set_name'] = brickset_stats['set_name']
    elif 'set_name' in bricklink_stats:
        if bricklink_stats['set_name'] == '': return None
        scrubbed_dic['set_name'] = bricklink_stats['set_name']
    else:
        return None

    if 'set_num' in brickset_stats:
        if brickset_stats['set_num'] == '': return None
        scrubbed_dic['item_num'], scrubbed_dic['item_seq'], scrubbed_dic['set_num'] = expand_set_num(
            brickset_stats['set_num'])
    elif 'set_num' in bricklink_stats:
        if bricklink_stats['set_num'] == '': return None
        scrubbed_dic['item_num'], scrubbed_dic['item_seq'], scrubbed_dic['set_num'] = expand_set_num(
            bricklink_stats['set_num'])
    else:
        return None

    if "theme" in brickset_stats:
        scrubbed_dic['theme'] = brickset_stats['theme']
    else:
        scrubbed_dic['theme'] = ""

    if "subtheme" in brickset_stats:
        scrubbed_dic['subtheme'] = brickset_stats['subtheme']
    else:
        scrubbed_dic['subtheme'] = ""

    if 'pieces' in brickset_stats:
        scrubbed_dic['piece_count'] = brickset_stats['pieces']
    elif 'pieces' in bricklink_stats:
        scrubbed_dic['piece_count'] = bricklink_stats['pieces']
    else:
        scrubbed_dic['piece_count'] = None

    if 'figures' in brickset_stats:
        scrubbed_dic['figures'] = brickset_stats['figures']
    elif 'figures' in bricklink_stats:
        scrubbed_dic['figures'] = bricklink_stats['figures']
    else:
        scrubbed_dic['figures'] = None

    if "weight" in bricklink_stats:
        scrubbed_dic['set_weight'] = bricklink_stats['weight']
    else:
        scrubbed_dic['set_weight'] = None

    if 'year_released' in brickset_stats:
        scrubbed_dic['year_released'] = brickset_stats['year_released']
    elif 'year_released' in bricklink_stats:
        scrubbed_dic['year_released'] = bricklink_stats['year_released']
    else:
        scrubbed_dic['year_released'] = None

    if 'available_us' in brickset_stats:
        scrubbed_dic['date_released_us'], scrubbed_dic['date_ended_us'] = brickset_stats['available_us']
    else:
        scrubbed_dic['date_released_us'], scrubbed_dic['date_ended_us'] = None, None

    if 'available_uk' in brickset_stats:
        scrubbed_dic['date_released_uk'], scrubbed_dic['date_ended_uk'] = brickset_stats['available_uk']
    else:
        scrubbed_dic['date_released_uk'], scrubbed_dic['date_ended_uk'] = None, None

    if 'original_price' in brickset_stats:
        if 'us' in brickset_stats['original_price']:
            scrubbed_dic['original_price_us'] = brickset_stats['original_price']['us']
        else:
            scrubbed_dic['original_price_us'] = None
        if 'uk' in brickset_stats['original_price']:
            scrubbed_dic['original_price_uk'] = brickset_stats['original_price']['uk']
        else:
            scrubbed_dic['original_price_uk'] = None
    else:
        scrubbed_dic['original_price_us'], scrubbed_dic['original_price_uk'] = None, None

    if 'age_range' in brickset_stats:
        scrubbed_dic['age_low'], scrubbed_dic['age_high'] = brickset_stats['age_range']
    else:
        scrubbed_dic['age_low'], scrubbed_dic['age_high'] = None, None

    if 'dimensions' in bricklink_stats:
        scrubbed_dic['box_size'] = str(bricklink_stats['dimensions']).strip('[]').strip('()')
    else:
        scrubbed_dic['box_size'] = None

    if 'volume' in bricklink_stats:
        scrubbed_dic['box_volume'] = bricklink_stats['volume']
    else:
        scrubbed_dic['box_volume'] = None

    if scrubbed_dic == {}:
        logging.warning("No data for set: {}".format(set))
        return None

    scrubbed_dic['last_update'] = arrow.now('US/Pacific').format('YYYY-MM-DD')

    if type == 1:  # Return a list instead of a dict
        return [scrubbed_dic['set_name'],
                scrubbed_dic['set_num'],
                scrubbed_dic['item_num'],
                scrubbed_dic['item_seq'],
                scrubbed_dic['theme'],
                scrubbed_dic['subtheme'],
                scrubbed_dic['piece_count'],
                scrubbed_dic['figures'],
                scrubbed_dic['set_weight'],
                scrubbed_dic['year_released'],
                scrubbed_dic['date_released_us'],
                scrubbed_dic['date_ended_us'],
                scrubbed_dic['date_released_uk'],
                scrubbed_dic['date_ended_uk'],
                scrubbed_dic['original_price_us'],
                scrubbed_dic['original_price_uk'],
                scrubbed_dic['age_low'],
                scrubbed_dic['age_high'],
                scrubbed_dic['box_size'],
                scrubbed_dic['box_volume'],
                scrubbed_dic['last_update']]

    return scrubbed_dic


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
            get_bl_inventory(set, bl_designs_in_database)

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
