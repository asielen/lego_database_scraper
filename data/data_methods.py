__author__ = 'andrew.sielen'

from system.logger import logger

from system.base_methods import LBEF
from data.bricklink import bricklink_data_scrape as blds
from data.bricklink.bricklink_api import bricklink_api as blapi
from data.brickset.brickset_api import brickset_set_data as BS
from data.rebrickable import rebrickable_api as reapi
from data.peeron.peeron_api import peeron_api as perapi


def get_colors():
    """
    combine data from peeron and rebrickable to create the colors table
    @return:  [bl_id, re_id, bo_id, ldraw_id, lego_id, bl_name, lego_name, hex]
    """
    logger.debug("Get all colors from rebrickable and peeron")

    rebrickable_colors = _filter_rebrickable_colors(
        reapi.pull_colors())  # bl_color: [rebrickable ID, Name, hex, [ldraw color], [bricklink color]]
    peeron_colors = _filter_peeron_colors(
        perapi.pull_colors())  # [bl_name, bl_id, ldraw_id, ldraw_hex, lego_id, lego_name]
    bricklink_colors = LBEF.list_to_dict(_filter_bl_colors(blapi.pull_colors()))

    processed_colors = []

    for color in peeron_colors:
        if color[1] is None: continue  # If there is no bl_id
        bl_id = str(color[1])
        bricklink_colors.pop(bl_id, None)
        re_color = [None]
        if str(color[1]) in rebrickable_colors:
            re_color = rebrickable_colors[str(bl_id)][0]
        # [bl_id, re_id, bo_id, ldraw_id, lego_id, bl_name, lego_name, hex]
        processed_colors.append([color[1], re_color[0], None, color[2], color[4], color[0], color[5], color[3]])

    # Add missing rebrickable colors
    missed_colors = rebrickable_colors['None']
    for color in missed_colors:  # If it couldn't match the color
        ldraw_id = color[3]
        peeron_id = None
        added = 0
        for p_color in processed_colors:
            if ldraw_id == p_color[3]:
                p_color[1] = color[0]
                added = 1
        if added == 0:  # if we couldn't find it and update it
            processed_colors.append([color[4], color[0], None, color[3], None, color[1], None, color[2].strip("#")])

    # Add missing bricklink colors
    for color in bricklink_colors:
        processed_colors.append([int(color), None, None, None, None, bricklink_colors[color], None, None])
    return processed_colors


def _filter_bl_colors(colors):
    """
    From:
    # [bl_id, color_name, rgb, type, parts, in sets, wanted, for sale, year from, year to]
    To
    # [bl_id, bl_name]
    @return:
    """
    processed_colors = []
    for c in colors:
        # Convert the text to ints
        processed_colors.append(c[:2])
    processed_colors = processed_colors[2:]
    return processed_colors


def _filter_peeron_colors(colors):
    """
    From:
    # [peeron_name, parts, bl_name, bl_id, ldraw_id, ldraw_hex, lego_id, lego_name, rgb, cmyk, pantone, notes]
    To
    # [bl_name, bl_id, ldraw_id, ldraw_hex, lego_id, lego_name]
    @return:
    """
    processed_colors = []
    for c in colors:
        # Convert the text to ints
        c[3] = LBEF.int_null(c[3])
        c[4] = LBEF.int_null(c[4])
        c[6] = LBEF.int_null(c[6])
        processed_colors.append(c[2:-4])
    return processed_colors


def _filter_rebrickable_colors(colors):
    """
    From
    # ['',rebrickable ID, Name, rgb hex, num parts, num sets, start year, start end, lego name, {ldraw color}, {bricklink color}, peeron color]
    To
    # [rebrickable ID, Name, hex, [ldraw color], [bricklink color]]
    @return:
    """
    processed_colors = {}
    colors = colors[1:]  # Remove the header
    colors_to_remove = []
    for c in colors:
        if c[1] == "ID":
            colors_to_remove.append(c)
            continue
        ldraw_ids = _process_clist(c[9])
        c[9] = ldraw_ids
        bl_ids = _process_clist(c[10])
        c[10] = bl_ids

        if len(bl_ids) > 1:
            for id in bl_ids:
                temp_c = c[:]
                temp_c[10] = [id]
                colors.append(temp_c)
            colors_to_remove.append(c)
        elif len(ldraw_ids) > 1:
            for id in ldraw_ids:
                temp_c = c[:]
                temp_c[9] = [id]
                colors.append(temp_c)
            colors_to_remove.append(c)
        else:
            continue
    for c in colors_to_remove:
        colors.remove(c)
    for c in colors:
        if str(c[10][0]) not in processed_colors:
            processed_colors[str(c[10][0])] = []
        processed_colors[str(c[10][0])].append([LBEF.int_null(c[1]), c[2], c[3], c[9][0], c[10][0]])

    return processed_colors


def _process_clist(clist):
    """
    Take a list like '{12, 3, 4}'
    and return [12,3,4]
    @param clist:
    @return:
    """
    if isinstance(clist, list): return clist
    clist = clist.strip("{}")
    clist = clist.split(',')
    clist = [LBEF.int_null(c) for c in clist]
    return clist


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
                  'weight': None, "bl_category": 0, "bl_type": None}
    bl_piece_info = None
    design_alts = None
    if bl_id is not None:
        bl_piece_info = blds.get_bl_piece_info(bl_id)

    # Try to find the bl_id for this set by searching alternate ids and element ids. This can be very slow
    elif re_id is not None:
        logger.debug("Searching for bl_id for re_id {}".format(re_id))
        re_piece_info = reapi.pull_piece_info(re_id)  # [re_id, bl_id, name, alt_ids, element_ids]
        if re_piece_info is None:
            logger.warning("{} doesn't even exist on rebrickable".format(re_id))
            return piece_info, design_alts
        elif re_piece_info[1] is not None:
            bl_piece_info = blds.get_bl_piece_info(re_piece_info[1], default=None)

        else:
            bl_piece_info = blds.get_bl_piece_info(re_piece_info[0], default=None)

            if bl_piece_info is None and re_piece_info[3] is not None:
                for alt in re_piece_info[3]:
                    bl_piece_info = blds.get_bl_piece_info(alt, default=None)

                    if bl_piece_info is not None: break
            if bl_piece_info is None and re_piece_info[4] is not None:
                for elm in re_piece_info[4]:
                    bl_piece_info = blds.get_bl_piece_info(elm, default=None)

                    if bl_piece_info is not None: break
            # if bl_piece_info is None:
            # bl_piece_info = blds.get_bl_piece_info(re_piece_info[2], default=None) # Worst case, lookup the name


            if bl_piece_info is not None:
                logger.debug("Found bl_id {}".format(bl_piece_info['design_num']))
            else:
                logger.debug("Couldn't Find bl_id adding as filler")
                LBEF.note("Missing Piece Info: re_id={}".format(re_id))

    if bl_piece_info is not None:
        piece_info['bricklink_id'] = bl_piece_info['design_num']
        piece_info['design_name'] = bl_piece_info['design_name']
        piece_info['weight'] = bl_piece_info['weight']
        piece_info['bl_category'] = bl_piece_info['piece_category']
        piece_info['bl_type'] = bl_piece_info['piece_type']

    if type == 1:
        return [piece_info['bricklink_id'],
                piece_info['brickowl_id'],
                piece_info['rebrickable_id'],
                piece_info['lego_id'],
                piece_info['design_name'],
                piece_info['weight'],
                piece_info['bl_type'],
                piece_info["bl_category"]]
    return piece_info


def get_basestats(o_set, type=1):
    """
    Gets base o_set info from a combination of bricklink and brickset data
    @param o_set: o_set num in standard format xxxx-x
    @param type: 0 = dict, 1 = list
    @return: dictionary of o_set information
    """

    if o_set is None:
        logger.warning("Trying to update a set but there is none to update")
        return None

    set_num, set_seq, o_set = LBEF.expand_set_num(o_set)
    if set_num is None:  # If it is an invalid setnum then return Num, this happens for rebrickable alternate sets that have multiple dashes in the setnum
        return None

    scrubbed_dic = {}

    brickset_stats = BS.get_basestats(set_num, set_seq)
    bricklink_stats = blds.get_basestats(set_num, set_seq)
    rebrickable_stats = list(reapi.pull_set_info(o_set))

    if 'set_name' in brickset_stats:
        # if brickset_stats['set_name'] == '':
        # return None
        scrubbed_dic['set_name'] = brickset_stats['set_name']
    elif 'set_name' in bricklink_stats:
        # if bricklink_stats['set_name'] == '':
        # return None
        scrubbed_dic['set_name'] = bricklink_stats['set_name']
    elif len(rebrickable_stats) > 1:
        scrubbed_dic['set_name'] = rebrickable_stats[3]
    else:
        scrubbed_dic['set_name'] = None

    if 'set_num' in brickset_stats:
        # if brickset_stats['set_num'] == '':
        # return None
        scrubbed_dic['item_num'], scrubbed_dic['item_seq'], scrubbed_dic['set_num'] = LBEF.expand_set_num(
            brickset_stats['set_num'])
    elif 'set_num' in bricklink_stats:
        # if bricklink_stats['set_num'] == '':
        # return None
        scrubbed_dic['item_num'], scrubbed_dic['item_seq'], scrubbed_dic['set_num'] = LBEF.expand_set_num(
            bricklink_stats['set_num'])
    else:
        scrubbed_dic['item_num'], scrubbed_dic['item_seq'], scrubbed_dic['set_num'] = LBEF.expand_set_num(
            o_set)

    if "theme" in brickset_stats:
        scrubbed_dic['theme'] = brickset_stats['theme']
    elif len(rebrickable_stats) > 1:
        scrubbed_dic['theme'] = rebrickable_stats[4]
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
    elif len(rebrickable_stats) > 1:
        scrubbed_dic['year_released'] = rebrickable_stats[5]
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
        logger.warning("No data for o_set: {}".format(o_set))
        return None

    scrubbed_dic['last_update'] = LBEF.get_timestamp()

    scrubbed_dic['bo_set_num'] = None  # Todo, have this actually set the bo_set_num

    if type == 1:  # Return a list instead of a dict
        return [scrubbed_dic['set_num'],
                scrubbed_dic['bo_set_num'],
                scrubbed_dic['item_num'],
                scrubbed_dic['item_seq'],
                scrubbed_dic['set_name'],
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
    part = input("part num? ")
    print(get_piece_info(bl_id=part))
