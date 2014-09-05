__author__ = 'andrew.sielen'

import pprint as pp

from data.brickset.brickset_api import brickset_set_data as BS
from database.update import add_daily_stats as ADS
from database import set_info_old
from system.base_methods.LBEF import *
from system.logger import logger


def get_all_daily_set_data(set_list):
    """

    @param set_list: The list of sets to get data on (in this case, all of them)
    @return: success
    """
    if set_list is not None:
        total = len(set_list)
        for idx, set_num in enumerate(set_list):
            logger.info(
                "[ {0}/{1} {2}% ] Getting info on {3}".format(idx, total, round((idx / total) * 100, 2), set_num))
            get_daily_set_data(set_num)


def get_daily_set_data(set_num):
    """

    @param set_num: a set num in format xxxx-yy (text)
    @return:
    """
    if set_num is None:
        return None

    if set_info_old.check_last_updated_daily_stats(set_num) == False:
        set_num, set_seq, set_num = expand_set_num(set_num)

        price_dict = BHP.get_all_prices(set_num, set_seq)  # Todo: 20140901 What did this do? Where is it now?
        daily_data = BS.get_daily_data(set_num, set_seq)

        ADS.add_daily_set_data_to_database(set_num, price_dict, daily_data)

        return set_num, price_dict, daily_data

    else:
        return None


def main():
    set = input("What is the set num? ")
    pp.pprint(get_daily_set_data(set))
    main()


if __name__ == "__main__":
    main()