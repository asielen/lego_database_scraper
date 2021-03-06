# External
from multiprocessing import Pool as _pool

# Internal
import data
import database as db
import system as syt
from database import info as db_info
from data.bricklink.bricklink_api import bricklink_api as blapi
from data.data_classes.SetInfo_HPA_Class import SetInfo
if __name__ == "__main__": syt.setup_logger()


def add_set_to_database(set_num):
    """
    Single add
    @param set_num: xxxx-xx
    @return:
    """
    set_to_insert = _parse_get_basestats(set_num)
    add_set_data_to_database(set_to_insert)

@syt.counter("Update Secondary: Add Set to Database")
def add_set_data_to_database(set_data):
    """
    Single _set add to database
    @param set_data: list of 22 or 27 values to insert (27 with dates from class)
    @return:
    """

    # Strip out the counter part if there is one (counter is included in some  strings for pooling
    if len(set_data) == 2 and isinstance(set_data[1], syt.Counter):
        set_data = set_data[0]

    if set_data is None:
        return None

    syt.log_info("Inserting Set: {}".format(set_data[1]))

    # This is all for total update from a class
    dates = []
    if len(set_data) == 27:  #this is the total number of items in a class list
        set_data = set_data[1:]  #remove the id
        dates = list(set_data[-4:] + set_data[0])  # get the last four items of the list (dates)
        set_data = set_data[:22]  # remove the last four items from the list

    if len(set_data) != 22:
        syt.log_error("Set Data list is not valid")
        syt.log_error(set_data)

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

@syt.counter("Update Secondary: Add Sets to Database")
def add_sets_to_database(set_id_list, id_col=0, update=1):
    """
    # Todo:  Make a single add
    @param set_id_list: list of _set ids
    @param id_col: the column that set_ids are in
    @param update: 0 no updates, 1 basic updates, 2 all updates
        Basic is everything but get_prices and dates
    @return:
    """
    set_dict = db_info.read_bl_sets()

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
            pool_counts = None
            try:
                temp_list = syt.pool_skimmer(pool.map(_parse_get_basestats, sets_to_scrape))
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
    pool_counts = None
    try:
        temp_list = syt.pool_skimmer(pool.map(_parse_get_basestats, sets_to_scrape))
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

@syt.counter("Update Secondary: Add Sets Data to Database")
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
    syt.add_to_event("Update Secondary: Add Sets Data to Database – Sets",len(sets_to_insert_processed))


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
    return data.get_basestats(id), syt.get_counts(1)


# def main():
#     options = (
#         ("Update In Database", update_in_database),
#         ("Update from API", updates_sets_database_from_api)
#     )
#
#     syt.Menu("– Update Basestats –", choices=options).run()


# def update_in_database():
#     """
#
#     @return:
#     """
#     print("Please enter the start and end years you would like to update. "
#           "If left blank, it will capture everything before/after the date")
#     start_year = input("What year would you like to start with? ")
#     end_year = input("What year would you like to start with? ")
#
#     database_year_range = info.get_set_year_range()
#     if start_year is "": start_year = database_year_range[0]
#     if end_year is "": end_year = database_year_range[1]
#     proceed = input("Would you like to update all sets between {0} and {1}? Y/N?".format(start_year, end_year))
#     if proceed == "y" or proceed == "Y":
#         set_list = info.get_sets_between_years(start_year, end_year)
#
#         secondary.add_sets_to_database(set_list, update=1)


def updates_sets_database_from_api():
    """
    Update the database from an public_api call to bricklink and parses it and updates based on it
    ['Category ID', 'Category Name', 'Number', 'Name', 'Year Released', 'Weight (in Grams)', 'Dimensions']
    @return:
    """
    set_list = blapi.pull_set_catalog()
    if set_list is None: return None
    proceed = input("What Level of Update (-1 no check, 0 check 90 days, 1 check base data, 2 update all)? ")
    if proceed not in ('-1', '0', '1', '2'):
        proceed = 0
    else:
        proceed = int(proceed)
    add_sets_to_database(set_list, id_col=2, update=proceed)
