from data.brickset.brickset_api import brickset_set_data as BS

__author__ = 'andrew.sielen'

import logging

import arrow

from system.base_methods import LBEF
import data.bricklink.bricklink_data_scrape as blapi


def get_piece_info(bl_id=None, bo_id=None, re_id=None, lego_id=None, type=1):
    """
    Returns a list or a dict ready to be added to the database
    @param bl_id:
    @param bo_id:
    @param re_id:
    @param type:
    @return:
    """

    piece_info = {'lego_id': lego_id, 'bricklink_id': bl_id, 'brickowl_id': bo_id, 'rebrickable_id': re_id,
                  'design_name': None,
                  'weight': None, "bl_category": None, "bl_type": None}
    bl_piece_info = None
    if bl_id is not None:
        bl_piece_info = blapi.get_bl_piece_info(bl_id)
    elif re_id is not None:
        bl_piece_info = blapi.get_bl_piece_info(re_id)

    if bl_piece_info is not None:
        piece_info['bricklink_id'] = bl_piece_info['design_num']
        piece_info['design_name'] = bl_piece_info['design_name']
        piece_info['weight'] = bl_piece_info['weight']
        piece_info['bl_category'] = bl_piece_info['piece_category']
        piece_info['bl_type'] = bl_piece_info['piece_type']

    if type == 1:
        return [piece_info['lego_id'],
                piece_info['bricklink_id'],
                piece_info['brickowl_id'],
                piece_info['rebrickable_id'],
                piece_info['design_name'],
                piece_info['weight'],
                piece_info['bl_type'],
                piece_info["bl_category"]]
    return piece_info


def get_basestats(set, type=1):
    """
    Gets base set info from a combination of bricklink and brickset data
    @param set: set num in standard format xxxx-x
    @param type: 0 = dict, 1 = list
    @return: dictionary of set information
    """

    if set is None:
        logging.warning("Trying to update a set but there is none to update")
        return None

    set_num, set_seq, set = LBEF.expand_set_num(set)

    scrubbed_dic = {}

    brickset_stats = BS.get_basestats(set_num, set_seq)
    bricklink_stats = blapi.get_basestats(set_num, set_seq)

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
        scrubbed_dic['item_num'], scrubbed_dic['item_seq'], scrubbed_dic['set_num'] = LBEF.expand_set_num(
            brickset_stats['set_num'])
    elif 'set_num' in bricklink_stats:
        if bricklink_stats['set_num'] == '': return None
        scrubbed_dic['item_num'], scrubbed_dic['item_seq'], scrubbed_dic['set_num'] = LBEF.expand_set_num(
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


if __name__ == "__main__":
    def main():
        SET = input("What is the set number?: ")
        print(get_basestats(SET))
        main()


    if __name__ == "__main__":
        main()