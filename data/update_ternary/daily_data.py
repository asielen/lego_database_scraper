__author__ = 'andrew.sielen'

from multiprocessing import Pool as _pool
from time import sleep

from data.brickset.brickset_api import brickset_set_data as BS
from data.bricklink import bricklink_data_scrape as BLDS
from database.update import add_daily_stats as ADS
from database import info
from system import base
from system.logger import logger


def get_all_daily_set_data(set_list):
    """

    @param set_list: The list of sets to get data on (in this case, all of them)
    @return: success!
    """

    sets = info.read_bl_set_num_id()  # Gets a list of sets and set ids

    last_updated = info.get_last_updated_for_daily_stats()  # List of when each set was last updated

    num_sets = len(set_list)  # Total number of sets to update

    set_daily_to_scrape = []
    set_daily_to_insert = []
    sets_missed = []
    pool = _pool(base.RUNNINGPOOL)
    timer = base.process_timer("Update Historic Prices")

    for idx, set_num in enumerate(set_list):
        if set_num in sets:
            if last_updated[set_num]:  # IF TRUE = if the set was updated today
                continue
            set_daily_to_scrape.append((sets[set_num], set_num))
        else:
            # Todo Add set to database
            pass
        # Scrape Pieces

        if idx > 0 and idx % (base.RUNNINGPOOL) == 0:
            try:
                temp_list = pool.map(_get_daily_set_data, set_daily_to_scrape)
            except AttributeError:
                logger.error("Missed {} sets".format(len(set_daily_to_scrape)))
                sets_missed.extend(set_daily_to_scrape)
                temp_list = []

            set_daily_to_insert.extend(temp_list)
            logger.info(
                "@@@ Running Pool {} of {} sets ({}% complete)".format(idx, num_sets, round((idx / num_sets) * 100)))
            timer.log_time(len(set_daily_to_scrape), num_sets - idx)
            set_daily_to_scrape = []
            sleep(.5)

        # Insert Pieces

        if idx > 0 and len(set_daily_to_insert) >= 200:
            logger.info("@@@ Inserting {} pieces".format(len(set_daily_to_insert)))
            _add_daily_set_data_to_database(set_daily_to_insert)
            set_daily_to_insert = []

    # Final Scrape and insert
    try:
        temp_list = pool.map(_get_daily_set_data, set_daily_to_scrape)
    except AttributeError:
        logger.error("Missed {} sets".format(len(set_daily_to_scrape)))
        sets_missed.extend(set_daily_to_scrape)
        temp_list = []
    set_daily_to_insert.extend(temp_list)
    _add_daily_set_data_to_database(set_daily_to_insert)

    pool.close()
    pool.join()

    timer.log_time(num_sets)
    timer.end()

    if len(sets_missed) > 0:
        # Missed Sets
        logger.critical("MISSED {} SETS".format(len(sets_missed)))
        run_again = input("Run Again?")
        if run_again == "y":
            get_all_daily_set_data(sets_missed)


def _get_daily_set_data(set_tags):
    if set_tags[1] is None or set_tags[0] is None:
        return {None: ((), ())}
    set_num, set_seq, set_n = base.expand_set_num(set_tags[1])
    price_dict = BLDS.get_all_prices(set_num, set_seq)
    daily_data = BS.get_daily_data(set_num, set_seq)

    return {set_tags[0]: (price_dict, daily_data)}  # Pass set_id with set data


def _add_daily_set_data_to_database(set_data):
    ADS.add_daily_set_data_to_database(set_data)


def get_daily_set_data(set_num):
    """

    @param set_num: a set num in format xxxx-yy (text)
    @return:
    """
    if set_num is None:
        return None

    if info.get_last_updated_for_daily_stats(set_num) == False:
        set_num, set_seq, set_num = base.expand_set_num(set_num)

        price_dict = BLDS.get_all_prices(set_num, set_seq)
        daily_data = BS.get_daily_data(set_num, set_seq)

        ADS.add_daily_set_data_to_database(set_num, price_dict, daily_data)

        return set_num, price_dict, daily_data

    else:
        return None


def main():
    import pprint as pp

    set = base.input_set_num("What is the set num? ")
    pp.pprint(_get_daily_set_data(set))
    main()


if __name__ == "__main__":
    main()