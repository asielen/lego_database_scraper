__author__ = 'andrew.sielen'

import arrow
import logging
from profilehooks import profile

from LBEF import expand_set_num
import LBEF

from database_management import set_info
from database_management import add_set
from database_management import add_inventories

from data_scrapers import brickset_set_data as BS
from data_scrapers import bricklink_set_data as BL
from data_scrapers import brickset_inventory as BSP
from data_scrapers import bricklink_inventory as BLP

@profile
def get_all_basestats(set_list, force=0):
    """

    @param set_list: a list of set_nums acquired either though sql or a set.txt file
    @return:
    """

    if set_list is not None:
        if force == 0:
            filtered_set_list = get_and_filter_sets_by_year(set_list)
            total = len(filtered_set_list)
        else:
            filtered_set_list = set_list
            total = len(set_list)

        bl_designs_in_database = get_and_filter_sets_blinv_by_year(set_list)
        bs_elements_in_database = get_and_filter_sets_bsinv_by_year(set_list)

        finished = len(set_list) - total
        logging.info("Starting at {}% of total list –– [ {} / {} ]".format(round((finished / len(set_list)) * 100, 2),
                                                                           finished, len(set_list)))
        # Update basestats
        for idx, set in enumerate(filtered_set_list):
            logging.info("[ {0}/{1} {2}% ] Getting info on {3}".format(idx, total, round((idx / total) * 100, 2), set))
            get_basestats(set)

        # Update bricklinnk inventories
        logging.info("Updating bricklink inventories for {} sets".format(len(bl_designs_in_database)))
        for idx, set in enumerate(bl_designs_in_database):
            logging.info("{0} Getting bl inventory on {1}".format(idx, set))
            get_bl_inventory(set, bl_designs_in_database)

        # Update brickset inventories
        logging.info("Updating brickset inventories for {} sets".format(len(bs_elements_in_database)))
        for idx, set in enumerate(bs_elements_in_database):
            logging.info("{0} Getting bs inventory on {1}".format(idx, set))
            get_bs_inventory(set, bs_elements_in_database)


def get_and_filter_sets_by_year(set_list):
    return set_info.filter_list_on_dates(set_list, set_info.get_all_set_years())

def get_and_filter_sets_blinv_by_year(set_list):
    return set_info.filter_list_on_dates(set_list, set_info.get_all_bl_update_years())

def get_and_filter_sets_bsinv_by_year(set_list):
    return set_info.filter_list_on_dates(set_list, set_info.get_all_bs_update_years())


@profile
def get_basestats(set):
    """

    @param set: set num in standard format xxxx-x
    @param force: if force is 1, it will update even if it doesn't need to be updated
    @return:
    """

    if set is None:
        logging.warning("Trying to update a set but there is no set to update")
        return None

    set_num, set_seq, set = expand_set_num(set)

    scrubbed_dic = {}

    logging.info("Getting base stats for: set {}".format(set))

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
        scrubbed_dic['item_num'], scrubbed_dic['item_seq'], scrubbed_dic['set_num'] = expand_set_num(brickset_stats['set_num'])
    elif 'set_num' in bricklink_stats:
        if bricklink_stats['set_num'] == '': return None
        scrubbed_dic['item_num'], scrubbed_dic['item_seq'], scrubbed_dic['set_num'] = expand_set_num(bricklink_stats['set_num'])
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

    add_set.add_set_to_database(scrubbed_dic)

def get_bl_inventory(set, bl_designs_in_database):
    """

    @param set: in standard format xxxx–x
    @param bl_designs_in_database: list of pieces
    @param force:
    @return:
    """
    set_num, set_seq, set = expand_set_num(set)

    logging.info("Updating bricklink inventory for set {}".format(set))
    bricklink_pieces = BLP.get_setpieces(set_num, set_seq)
    if bricklink_pieces is not None:
        add_inventories.add_bl_set_pieces_to_database(set, bricklink_pieces)


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
