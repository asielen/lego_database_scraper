from data.brickset.brickset_api import brickset_inventory as BSP
from z_junk import update_database as ud

__author__ = 'andrew.sielen'

import pprint as pp
import arrow
from system.base_methods.LBEF import expand_set_num


def get_basestats(set, force=0, verbose=0):
    if set is None: return None, None

    set_num, set_seq, set = expand_set_num(set)

    scrubbed_dic = {}
    if ud._chk_last_updated_today(set) == False and force == 0:
        if verbose == 1:
            print("Getting Base Stats: " + str(set))
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
            scrubbed_dic['set_num'] = brickset_stats['set_num']
            scrubbed_dic['item_num'], scrubbed_dic['item_seq'] = brickset_stats['set_num'].split("-")
        elif 'set_num' in bricklink_stats:
            if bricklink_stats['set_num'] == '': return None
            scrubbed_dic['set_num'] = bricklink_stats['set_num']
            scrubbed_dic['item_num'], scrubbed_dic['item_seq'] = bricklink_stats['set_num'].split("-")
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

        if scrubbed_dic == {}: return (None, None)
        scrubbed_dic['last_update'] = arrow.now('US/Pacific').format('YYYY-MM-DD')

        ud.add_set2database(scrubbed_dic, verbose)
    else:
        if verbose == 1:
            print("Base Stats in for today: " + str(set))
    return None


def get_pieces(set, force=0, verbose=0):
    set_num, set_seq, set = expand_set_num(set)
    if ud._chk_last_inv_updated_today(set) == False and force == 0:
        if verbose == 1:
            print("Getting Pieces: " + str(set))
        brickset_pieces = BSP.get_setpieces(set_num, set_seq)
        ud.add_BSsetPieces2Database(set, brickset_pieces, verbose)

        bricklink_pieces = BLP.get_setpieces(set_num, set_seq)
        ud.add_BLsetPieces2Database(set, bricklink_pieces, verbose)

    else:
        if verbose == 1:
            print("Pieces in for today: " + str(set))
    return None


def main():
    set = input("What is the set num? ")
    pp.pprint(get_basestats(set, verbose=1))
    pp.pprint(get_pieces(set, verbose=1))
    main()


if __name__ == "__main__":
    main()
