# Todo: Need to test this file

# External
from multiprocessing import Pool as _pool

# Internal
import data
import database as db
import database.info as info
import system as syt
from data.data_classes.SetInfo_HPA_Class import SetInfo
if __name__ == "__main__": syt.setup_logger()


# def add_set_to_database(set_data):
# """
#     Adds a set to the database
#     @param set_data: either complete set data or a set id
#     @return:
#     """
#     if set_data is None: return None
#     if len(set_data) is 1:
#         set_data = data.get_basestats(set_data)
#         if set_data is None: return None
#
#     return db.run_sql(
#         'INSERT OR IGNORE INTO sets('
#         'set_num, '
#         'bo_set_num, '
#         'item_num, '
#         'item_seq, '
#         'set_name, '
#         'theme, '
#         'subtheme, '
# 'get_piece_count, '
#         'get_figures, '
#         'set_weight, '
#         'year_released, '
#         'date_released_us, '
#         'date_ended_us, '
#         'date_released_uk, '
#         'date_ended_uk, '
#         'original_price_us, '
#         'original_price_uk, '
#         'age_low, '
#         'age_high, '
#         'box_size, '
#         'box_volume, '
#         'last_updated'
#         ') VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', insert_list=tuple(set_data))


def add_set_to_database(set_num):
    """
    Single add
    @param set_num: xxxx-xx
    @return:
    """
    set_to_insert = _parse_get_basestats(set_num)
    add_set_data_to_database(set_to_insert)


def add_set_data_to_database(set_data):
    """
    Single set add to database
    @param set_data: list of 22 or 27 values to insert (27 with dates from class)
    @return:
    """
    if set_data is None:
        return None

    # sys.info("Inserting Set: {}".format(set_data[1]))

    # This is all for total update from a class
    dates = []
    if len(set_data) == 27:  #this is the total number of items in a class list
        set_data = set_data[1:]  #remove the id
        dates = list(set_data[-4:] + set_data[0])  # get the last four items of the list (dates)
        set_data = set_data[:22]  # remove the last four items from the list

    if len(set_data) != 22:
        syt.log_error("Set Data list is not valid")

    db.run_sql('INSERT OR IGNORE INTO sets(set_num) VALUES (?)', (set_data[0],))

    set_data_processed = tuple(
        set_data[1:] + [set_data[1]])  #Take set_num and move it to the back so i can use it to compare
    db.run_sql('UPDATE sets SET '
               'bo_set_num=?,'
               'item_num=?, '
               'item_seq=?,'
               'set_name=?, '
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
               'WHERE set_num=?', set_data_processed)

    if len(dates) == 4:
        db.run_sql('UPDATE sets SET '
                   'last_inv_updated_bo=?, '
                   'last_inv_updated_bl=?, '
                   'last_inv_updated_re=?, '
                   'last_price_updated=?'
                   'WHERE set_num=?', set_data_processed)


# def add_or_update_set_from_class(set_data_list):
# """
#     Single set add to database from a complete data list (all 26 items)
#     @param sets_to_insert:
#     @return:
#     """
#     if set_data_list is None:
#         return None
#     assert len(set_data_list)==26
#
#
#     db.run_sql('INSERT OR IGNORE INTO sets(set_num) VALUES (?)', (set_data_list[0],))
#
#     set_data_processed = tuple(set_data_list[1:] + [set_data_list[0]])
#     db.run_sql('UPDATE sets SET '
#                'bo_set_num=?,'
#                'item_num=?, '
#                'item_seq=?,'
#                'set_name=?, '
#                'theme=?, '
#                'subtheme=?, '
#                'get_piece_count=?, '
# 'get_figures=?, '
#                'set_weight=?, '
#                'year_released=?, '
#                'date_released_us=?, '
#                'date_ended_us=?, '
#                'date_released_uk=?, '
#                'date_ended_uk=?, '
#                'original_price_us=?, '
#                'original_price_uk=?, '
#                'age_low=?, '
#                'age_high=?, '
#                'box_size=?, '
#                'box_volume=?, '
#                'last_updated=?,'
#                'last_inv_updated_bo=?,'
#                'last_inv_updated_bl=?,'
#                'last_inv_updated_re=?,'
#                'last_price_updated=? '
#                'WHERE set_num=?', set_data_processed)


def add_sets_to_database(set_id_list, id_col=0, update=1):
    """
    # Todo:  Make a single add
    @param set_id_list: list of set ids
    @param id_col: the column that set_ids are in
    @param update: 0 no updates, 1 basic updates, 2 all updates
        Basic is everything but get_prices and dates
    @return:
    """
    set_dict = info.read_bl_sets()

    syt.log_info("$$$ Adding sets to the database")
    sets_to_scrape = []
    sets_to_insert = []
    sets_missed = []
    set_id_list = list(set_id_list)
    set_list_len = len(set_id_list)
    pool = _pool(syt.RUNNINGPOOL)

    timer = syt.process_timer("Add Sets to Database {}".format(update))
    for idx, row in enumerate(set_id_list):
        if len(row) == 0:
            continue
        if row[id_col] in set_dict:  # If the row is already in the database
            if _check_set_completeness(set_dict[row[id_col]], level=update) is True:
                continue

        sets_to_scrape.append(row[id_col])

        if idx > 0 and idx % (syt.RUNNINGPOOL * 2) == 0:
            syt.log_info("@@@ Running Pool {}".format(idx))
            temp_list = []
            try:
                temp_list = pool.map(_parse_get_basestats, sets_to_scrape)
                sets_to_insert.extend(temp_list)
            except:
                #Skip the add and make a note
                syt.log_error("Missed {} sets".format(len(sets_to_scrape)))
                sets_missed.extend(sets_to_scrape)
            timer.log_time(len(sets_to_scrape), set_list_len - idx)
            sets_to_scrape = []

        if idx > 0 and len(sets_to_insert) >= 600:
            add_sets_data_to_database(sets_to_insert)
            sets_to_insert = []

    temp_list = []
    try:
        temp_list = pool.map(_parse_get_basestats, sets_to_scrape)
        sets_to_insert.extend(temp_list)
    except:
        #Skip the add and make a note
        syt.log_error("Missed {} sets".format(len(sets_to_scrape)))
        sets_missed.extend(sets_to_scrape)
    timer.log_time(len(sets_to_scrape), 0)
    timer.end()

    pool.close()
    pool.join()

    add_sets_data_to_database(sets_to_insert)
    syt.log_info("%%% Sets added to database")

    if len(sets_missed) > 0:
        # Missed Sets
        syt.log_critical("MISSED {} SETS".format(len(sets_missed)))
        run_again = input("Run Again?")
        if run_again == "y":
            add_sets_to_database(sets_missed, id_col, update)


def add_sets_data_to_database(sets_to_insert):
    """
    Add and update a list of sets to the database (need bl_id to be filled out)

    @return:
    """
    # import pprint
    # print("inserting sets")
    # pprint.pprint([tuple(p[1:] + [p[0]]) for p in sets_to_insert])
    if sets_to_insert is None or len(sets_to_insert) == 0:
        return
    sets_to_insert = list(filter(None, sets_to_insert))
    syt.log_info("Adding {} sets to the database".format(len(sets_to_insert)))

    db.batch_update('INSERT OR IGNORE INTO sets(set_num) VALUES (?)',
                    ((p[0],) for p in sets_to_insert))  # 0 is the position of the set_num

    sets_to_insert_processed = [tuple(p[1:] + [p[0]]) for p in sets_to_insert]  #take the setnum and move it to the end
    db.batch_update('UPDATE sets SET '
                    'bo_set_num=?,'
                    'item_num=?, '
                    'item_seq=?,'
                    'set_name=?, '
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
    set_num = set_num.lower()
    try:
        set_id = sets[set_num]
    except:
        set_id = SetInfo.get_set_id(set_num)
    if set_id is None and add:
        add_set_to_database(set_num)
        set_id = SetInfo.get_set_id(set_num)
        if set_id is not None:
            sets[set_num] = set_id
    return set_id


def _check_set_completeness(set_data, level=1):
    """

    @param set_data: data in database insert format
    @param level: -1 checks nothing, 0 checks date, 1 checks for basic stuff like name, theme, year released, pieces; 2 checks for everything
    @return: True if complete; False if not
    """
    if level == -1: return True
    if level >= 0:
        if syt.old_data(set_data[22]) is True:
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
    @param id:
    @return:
    """
    return data.get_basestats(id)