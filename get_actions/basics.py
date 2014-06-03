__author__ = 'andrew.sielen'

import logging

import arrow

from LBEF import expand_set_num
from database_management import set_info_old
from database_management import add_inventories
from database_management.add_set import add_set_to_database_from_dict
from scrapers import brickset_set_data as BS
from scrapers import bricklink_set_data as BL
from scrapers import brickset_inventory as BSP
from scrapers import brickset_piece_info as BPI
from apis import bricklink_api_update_database as Blapi


def add_set_to_database(set_num):
    """
    Takes a set num, pulls all the base stats for it and then adds it to the database
    @param set_num: in the format xxxx-xx
    @return:
    """
    add_set_to_database_from_dict(get_basestats(set_num))


def add_piece_to_database(bl_id="", bo_id=""):
    """

    @param bl_id:
    @return:
    """
    if bl_id == "" and bo_id == "":
        return None
    if bl_id != "":
        add_design_to_database(BPI.get_blPieceInfo(bl_id))


def add_bl_inventory_to_database():
    pass


def add_bs_inventory_to_database():
    pass


def add_bo_inventory_to_database():
    pass


# TODO: Rewrite this to use multiprocess
def get_all_basestats(set_list, force=0):
    """

    @param set_list: a list of set_nums acquired either though sql or a text file
    @return:
    """

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
    return set_info_old.filter_list_on_dates(set_list, set_info_old.get_all_set_years())


def _get_and_filter_sets_blinv_by_year(set_list):
    return set_info_old.filter_list_on_dates(set_list, set_info_old.get_all_bl_update_years())


def _get_and_filter_sets_bsinv_by_year(set_list):
    return set_info_old.filter_list_on_dates(set_list, set_info_old.get_all_bs_update_years())


def get_basestats(set, type=0):
    """

    @param set: set num in standard format xxxx-x
    @return: dictionary of set information
    """

    if set is None:
        logging.warning("Trying to update a set but there is none to update")
        return None

    set_num, set_seq, set = expand_set_num(set)

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


def get_bl_inventory(set, bl_designs_in_database):
    """

    @param set: in standard format xxxx–x
    @param bl_designs_in_database: list of pieces
    @param force:
    @return:
    """
    set_num, set_seq, set = expand_set_num(set)

    logging.info("Updating bricklink inventory for set {}".format(set))
    Blapi.add_set_inventory(set)


def get_bs_inventory(set, bs_elements_in_database):
    """

    @param set:
    @param bs_elements_in_database:
    @param force:
    @return:
    """
    set_num, set_seq, set = expand_set_num(set)

    logging.info("Updating brickset inventory for set {}".format(set))
    brickset_pieces = BSP.get_setpieces(set_num, set_seq)
    if brickset_pieces is not None:
        add_inventories.add_bs_set_pieces_to_database(set, brickset_pieces)


def main():
    set = input("What is the set num? ")
    print(get_basestats(set))
    print(get_pieces(set))
    main()


if __name__ == "__main__":
    main()
