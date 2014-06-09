from data.brickset.brickset_api import brickset_set_data as BS
from z_junk import update_database_with_daily_info as udi

__author__ = 'andrew.sielen'

import pprint as pp
from system.base_methods.LBEF import *


def get_daily(set):
    if set is None: return None

    set_num, set_seq, set = expand_set_num(set)

    price_dict = BHP.get_all_prices(set_num, set_seq)
    daily_data = BS.get_daily_data(set_num, set_seq)

    udi.add_daily2database(set, price_dict, daily_data)

    return set, price_dict, daily_data


def main():
    set = input("What is the set num? ")
    pp.pprint(get_daily(set))
    main()


if __name__ == "__main__":
    main()