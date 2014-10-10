__author__ = 'andrew.sielen'

from multiprocessing import Pool as _pool
from time import sleep

from data.brickset.brickset_api import brickset_set_data as BS
from data.bricklink import bricklink_data_scrape as BLDS
from database.update import add_daily_stats as ADS
from database import info
from system import base_methods as LBEF
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
    pool = _pool(LBEF.RUNNINGPOOL)
    timer = LBEF.process_timer("Update Historic Prices")

    for idx, set_num in enumerate(set_list):
        if set_num in sets:
            if last_updated[set_num]:  # IF TRUE = if the set was updated today
                continue
            set_daily_to_scrape.append((sets[set_num], set_num))
        else:
            # Todo Add set to database
            pass
        # Scrape Pieces

        if idx > 0 and idx % (LBEF.RUNNINGPOOL) == 0:
            temp_list = pool.map(_get_daily_set_data, set_daily_to_scrape)
            set_daily_to_insert.extend(temp_list)
            logger.info(
                "Running Pool {} of {} sets ({}% complete)".format(idx, num_sets, round((idx / num_sets) * 100)))
            timer.log_time(len(set_daily_to_scrape), num_sets - idx)
            set_daily_to_scrape = []
            sleep(.5)

        # Insert Pieces

        if idx > 0 and len(set_daily_to_insert) >= 200:
            logger.info("Inserting {} pieces".format(len(set_daily_to_insert)))
            _add_daily_set_data_to_database(set_daily_to_insert)
            set_daily_to_insert = []

    # Final Scrape and insert
    temp_list = pool.map(_get_daily_set_data, set_daily_to_scrape)
    set_daily_to_insert.extend(temp_list)
    _add_daily_set_data_to_database(set_daily_to_insert)

    pool.close()
    pool.join()

    timer.log_time(num_sets)
    timer.end()


def _get_daily_set_data(set_tags):
    if set_tags[1] is None or set_tags[0] is None:
        return {None: ((), ())}
    set_num, set_seq, set_n = LBEF.expand_set_num(set_tags[1])
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
        set_num, set_seq, set_num = LBEF.expand_set_num(set_num)

        price_dict = BLDS.get_all_prices(set_num, set_seq)
        daily_data = BS.get_daily_data(set_num, set_seq)

        ADS.add_daily_set_data_to_database(set_num, price_dict, daily_data)

        return set_num, price_dict, daily_data

    else:
        return None


def main():
    import pprint as pp

    set = LBEF.input_set_num("What is the set num? ")
    pp.pprint(_get_daily_set_data(set))
    main()


if __name__ == "__main__":
    main()