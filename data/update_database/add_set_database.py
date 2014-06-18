__author__ = 'andrew.sielen'

import logging

logger = logging.getLogger('LBEF')
from multiprocessing import Pool as _pool

import data
import database as db
import database.info as info


def add_set_to_database(set_data):
    """
    Adds a set to the database
    @param set_data: in the format below
    @return:
    """
    if set_data is None: return None
    # con = lite.connect(db.database)
    # with con:
    # c = con.cursor()
    #     c.execute('INSERT OR IGNORE INTO sets('
    #                 'set_name, '
    #                 'set_num, '
    #                 'item_num, '
    #                 'item_seq, '
    #                 'theme, '
    #                 'subtheme, '
    #                 'piece_count, '
    #                 'figures, '
    #                 'set_weight, '
    #                 'year_released, '
    #                 'date_released_us, '
    #                 'date_ended_us, '
    #                 'date_released_uk, '
    #                 'date_ended_uk, '
    #                 'original_price_us, '
    #                 'original_price_uk, '
    #                 'age_low, '
    #                 'age_high, '
    #                 'box_size, '
    #                 'box_volume, '
    #                 'last_updated'
    #                 ') VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', tuple(set_data))

    return db.run_sql(
        'INSERT OR IGNORE INTO sets('
        'set_name, '
        'set_num, '
        'item_num, '
        'item_seq, '
        'theme, '
        'subtheme, '
        'piece_count, '
        'figures, '
        'set_weight, '
        'year_released, '
        'date_released_us, '
        'date_ended_us, '
        'date_released_uk, '
        'date_ended_uk, '
        'original_price_us, '
        'original_price_uk, '
        'age_low, '
        'age_high, '
        'box_size, '
        'box_volume, '
        'last_updated'
        ') VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', insert_list=tuple(set_data))


def add_sets_to_database(set_id_list):
    """

    @param set_id_list: list of set ids
    @return:
    """
    set_dict = info.read_bl_sets()

    logger.debug("Adding {} sets to the database".format(len(set_id_list)))
    sets_to_scrape = []
    sets_to_insert = []
    pool = _pool(50)
    for idx, row in enumerate(set_id_list):
        if len(row) == 0: continue
        if row[2] in set_dict:
            continue
        else:
            sets_to_scrape.append(row)
        if idx > 0 and idx % 150 == 0:
            sets_to_insert.extend(pool.map(_parse_get_basestats, sets_to_scrape))
            print("Completed {}".format(idx))
            print(len(sets_to_insert))
            sets_to_scrape = []
    sets_to_insert.extend(pool.map(_parse_get_basestats, sets_to_scrape))
    print("Completed {}".format(idx))
    print(len(sets_to_insert))

    pool.close()
    pool.join()  # TODO: Test with database insert
    db.batch_update('INSERT OR IGNORE INTO sets('
                    'set_name, '
                    'set_num, '
                    'item_num, '
                    'item_seq, '
                    'theme, '
                    'subtheme, '
                    'piece_count, '
                    'figures, '
                    'set_weight, '
                    'year_released, '
                    'date_released_us, '
                    'date_ended_us, '
                    'date_released_uk, '
                    'date_ended_uk, '
                    'original_price_us, '
                    'original_price_uk, '
                    'age_low, '
                    'age_high, '
                    'box_size, '
                    'box_volume, '
                    'last_updated'
                    ') VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', sets_to_insert,
                    header_len=0)


def _parse_get_basestats(row):
    """
    Wrapper for the get_basestats method to make it work easier with multiprocess
    @param row:
    @return:
    """
    return data.get_basestats(row[2], 1)