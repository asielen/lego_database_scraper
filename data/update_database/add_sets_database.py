__author__ = 'andrew.sielen'

from multiprocessing import Pool as _pool

import data
import database as db
import database.info as info
import system.base_methods as LBEF
from system.logger import logger

SLOWPOOL = 5
FASTPOOL = 35
RUNNINGPOOL = FASTPOOL


def add_set_to_database(set_data):
    """
    Adds a set to the database
    @param set_data: either complete set data or a set id
    @return:
    """
    if set_data is None: return None
    if len(set_data) is 1:
        set_data = data.get_basestats(set_data)
        if set_data is None: return None

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


def add_sets_to_database(set_id_list, id_col=0, update=1):
    """

    @param set_id_list: list of set ids
    @param id_col: the column that set_ids are in
    @param update: 0 no updates, 1 basic updates, 2 all updates
        Basic is everything but prices and dates
    @return:
    """
    set_dict = info.read_bl_sets()

    logger.debug("Adding sets to the database")
    sets_to_scrape = []
    sets_to_insert = []
    pool = _pool(RUNNINGPOOL)
    timer = LBEF.process_timer()
    for idx, row in enumerate(set_id_list):
        if len(row) == 0:
            continue
        if row[id_col] in set_dict:
            if _check_set_completeness(set_dict[row[id_col]], level=update) is True:
                continue

        sets_to_scrape.append(row[id_col])

        if idx > 0 and idx % 150 == 0:
            logger.info("Running Pool {}".format(idx))
            sets_to_insert.extend(pool.map(_parse_get_basestats, sets_to_scrape))
            timer.log_time(len(sets_to_scrape))
            sets_to_scrape = []

        if idx > 0 and idx % 600 == 0:
            add_sets_data_to_database(sets_to_insert)
            sets_to_insert = []

    sets_to_insert.extend(pool.map(_parse_get_basestats, sets_to_scrape))
    timer.log_time(len(sets_to_scrape))

    pool.close()
    pool.join()

    add_sets_data_to_database(sets_to_insert)


def add_sets_data_to_database(sets_to_insert):
    """
    Add and update a list of sets to the database (need bl_id to be filled out)

    @return:
    """
    if sets_to_insert is None or len(sets_to_insert) == 0:
        return
    sets_to_insert = list(filter(None, sets_to_insert))
    logger.info("Adding {} sets to the database".format(len(sets_to_insert)))
    db.batch_update('INSERT OR IGNORE INTO sets(set_num) VALUES (?)', ((p[1],) for p in sets_to_insert))

    sets_to_insert_processed = [tuple(p[:] + [p[1]]) for p in sets_to_insert]
    db.batch_update('UPDATE sets SET '
                    'set_name=?, '
                    'set_num=?, '
                    'item_num=?, '
                    'item_seq=?, '
                    'theme=?, '
                    'subtheme=?, '
                    'piece_count=?, '
                    'figures=?, '
                    'set_weight=?, '
                    'year_released=?, '
                    'date_released_us=?, '
                    'date_ended_us=?, '
                    'date_released_uk=?, '
                    'date_ended_uk=?, '
                    'original_price_us=?, '
                    'original_price_uk=?, '
                    'age_low=?, '
                    'age_high=?, '
                    'box_size=?, '
                    'box_volume=?, '
                    'last_updated=?'
                    'WHERE set_num=?', sets_to_insert_processed)


def get_set_id(set_num, sets=None, add=False):
    """
    a more useable version of the one in database info that also allows for saving
    @param set_num:
    @param sets:
    @param add:
    @return:
    """
    set_id = None
    try:
        set_id = sets[set_num]
    except:
        set_id = info.get_set_id(set_num)
    if set_id is None and add:
        add_sets_to_database([set_num])
        set_id = info.get_set_id(set_num)
    return set_id


def _check_set_completeness(set_data, level=1):
    """

    @param set_data: data in database insert format
    @param level: -1 checks nothing, 0 checks date, 1 checks for basic stuff like name, theme, year released, pieces; 2 checks for everything
    @return: True if complete; False if not
    """
    if level == -1: return True
    if level >= 0:
        if LBEF.old_data(set_data[22]) is True:
            return False
    if level == 2:
        for n in set_data:
            if n is None:
                return False
    elif level == 1:
        for n in set_data[3:12]:
            if n is None:
                return False

    return True


def _parse_get_basestats(id):
    """
    Wrapper for the get_basestats method to make it work easier with multiprocess
    @param row:
    @return:
    """
    return data.get_basestats(id, 1)