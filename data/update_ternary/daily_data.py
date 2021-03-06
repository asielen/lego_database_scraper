# External
from multiprocessing import Pool as _pool
from time import sleep

# Internal
from data.brickset.brickset_api import brickset_set_data as BS
from data.bricklink import bricklink_data_scrape as BLDS
from database.update import add_daily_stats as ADS
from database import info
import system as syt
from data.data_classes import SetInfo
if __name__ == "__main__": syt.setup_logger()


def get_all_daily_set_data(set_list):
    """

    @param set_list: The list of sets to get data on (in this case, all of them)
    @return: success!
    """

    sets = info.read_bl_set_num_id()  # Gets a list of sets and set ids

    last_updated = info.get_last_updated_for_daily_stats() # List of when each set was last updated

    num_sets = len(set_list)  # Total number of sets to update

    set_daily_to_scrape = []
    set_daily_to_insert = []
    sets_missed = []
    pool = _pool(syt.RUNNINGPOOL)
    timer = syt.process_timer("Update {} Historic Prices".format(len(set_list)))
    syt.add_to_event("Update Ternary: Get Daily Data",len(set_list))

    for idx, set_num in enumerate(set_list):
        if set_num in sets:
            if last_updated[set_num]:  # IF TRUE = if the set was updated today
                continue
            set_daily_to_scrape.append((sets[set_num], set_num))
            # syt.add_to_event("Update Ternary: Get Daily Data: {}".format(set_num))
        else:
            # Todo Add set to database
            pass
        # Scrape Pieces

        if idx > 0 and idx % (syt.RUNNINGPOOL) == 0:
            try:
                temp_list = syt.pool_skimmer(pool.map(_get_daily_set_data, set_daily_to_scrape))

            except (AttributeError, TypeError):
                syt.log_error("Missed {} sets".format(len(set_daily_to_scrape)))
                sets_missed.extend(set_daily_to_scrape)
                temp_list = []

            set_daily_to_insert.extend(temp_list)

            syt.log_info(
                "@@@ Running Pool {} of {} sets ({}% complete)".format(idx, num_sets, round((idx / num_sets) * 100)))
            timer.log_time(len(set_daily_to_scrape), num_sets - idx)
            set_daily_to_scrape = []
            sleep(.5)

        # Insert Pieces

        if idx > 0 and len(set_daily_to_insert) >= 200:
            syt.log_info("@@@ Inserting {} sets".format(len(set_daily_to_insert)))
            _add_daily_set_data_to_database(set_daily_to_insert)
            syt.add_to_event("Update Ternary: Got Daily Data",len(set_daily_to_insert))
            set_daily_to_insert = []

    # Final Scrape and insert
    try:
        temp_list = syt.pool_skimmer(pool.map(_get_daily_set_data, set_daily_to_scrape))
    except AttributeError:
        syt.log_error("Missed {} sets".format(len(set_daily_to_scrape)))
        sets_missed.extend(set_daily_to_scrape)
        temp_list = []
    if temp_list: set_daily_to_insert.extend(temp_list)
    _add_daily_set_data_to_database(set_daily_to_insert)
    syt.add_to_event("Update Ternary: Got Daily Data", len(set_daily_to_insert))

    pool.close()
    pool.join()

    timer.log_time(num_sets)
    timer.end()

    if len(sets_missed) > 0:
        # Missed Sets
        syt.log_critical("MISSED {} SETS".format(len(sets_missed)))
        run_again = input("Run Again?")
        if run_again == "y":
            get_all_daily_set_data(sets_missed)


@syt.counter(name="Update Ternary: Get Daily Set Data")
def _get_daily_set_data(set_tags):
    if set_tags[1] is None or set_tags[0] is None:
        return {None: ((), ())}
    set_num, set_seq, set_n = SetInfo.expand_set_num(set_tags[1])
    price_dict = BLDS.get_all_prices(set_num, set_seq)
    daily_data = BS.get_daily_data(set_num, set_seq)
    syt.add_to_event("Update Ternary: Get Daily Set Data: {}".format(set_n))
    return {set_tags[0]: (price_dict, daily_data)}, syt.get_counts(1)  # Pass set_id with set data


def _add_daily_set_data_to_database(set_data):
    ADS.add_daily_set_data_to_database(set_data)

def price_capture_menu():
    # Todo, should this be in this file?
    # Todo: make sure this runs the right update function - update inventories between the time frame

    print("Please enter the start and end years you would like to update. "
          "If left blank, it will capture everything before/after the date")
    start_year = input("What year would you like to start with? ")
    end_year = input("What year would you like to end with? ")

    database_year_range = info.get_set_year_range()
    if start_year is "": start_year = database_year_range[0]
    if end_year is "": end_year = database_year_range[1]
    proceed = input(
        "Would you like to update get_prices for all sets between {0} and {1}? Y/N? ".format(start_year, end_year))
    if proceed == "y" or proceed == "Y":
        set_list = info.get_sets_between_years(start_year, end_year)
        get_all_daily_set_data(set_list)

def main():
    import pprint as pp

    set = SetInfo.input_set_num()
    pp.pprint(_get_daily_set_data(set))
    main()


if __name__ == "__main__":
    main()
