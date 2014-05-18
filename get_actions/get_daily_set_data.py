__author__ = 'andrew.sielen'

import pprint as pp
from data_scrapers import bricklink_historic_prices as BHP
from data_scrapers import brickset_set_data as BS
from database_management import add_daily_stats as ADS
from database_management import set_info
from LBEF import *
import logging

def get_all_daily_set_data(set_list):
    """

    @param set_list
    @return:
    """
    if set_list is not None:
        total = len(set_list)
        for idx, set in enumerate(set_list):
            logging.info("[ {0}/{1} {2}% ] Getting info on {3}".format(idx, total, round((idx/total)*100, 2), set))
            get_daily_set_data(set)


def get_daily_set_data(set_num):
    """

    @param set_num:
    @return:
    """
    if set_num is None:
        return None

    if set_info.check_last_updated_daily_stats(set_num) == False:
        set_num, set_seq, set_num = expand_set_num(set_num)

        price_dict = BHP.get_all_prices(set_num, set_seq)
        daily_data = BS.get_daily_data(set_num, set_seq)

        ADS.add_daily_set_data_to_database(set_num, price_dict, daily_data)

        return set_num, price_dict, daily_data


def main():
    set = input("What is the set num? ")
    pp.pprint(get_daily_set_data(set))
    main()


if __name__ == "__main__":
    main()