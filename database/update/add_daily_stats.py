__author__ = 'andrew.sielen'

import sqlite3 as lite

from system.logger import logger
from database import info
import database.database as db
import public_api
import system.base_methods as LBEF
from z_junk import get_daily


def add_daily_set_data_to_database(set_num, prices, ratings):
    """

    @param set_num: in standard format xxxx-x
    @param prices: list of all prices for the day
    @param ratings: current ratings (and date available)
    @return:
    """

    set_id = info.get_set_id(set_num)

    if set_id is None:  # TODO: This isn't needed with new set_id lookup
        public_api.get_basestats(set_num)
        set_id = info.get_set_id(set_num)
        if set_id is None:
            logger.warning("Cannot get daily data because set [{}] is not loading".format(set_num))
            return None

    add_daily_prices_to_database(set_id, prices)

    add_daily_ratings_to_database(set_id, ratings)

    con = lite.connect(db)
    with con:  # Update the last date
        c = con.cursor()
        c.execute('UPDATE sets SET last_price_updated=? WHERE id=?',
                  (LBEF.timestamp(), set_id))


def add_daily_prices_to_database(set_id, prices):
    current_date = LBEF.timestamp()

    con = lite.connect(db)
    with con:
        c = con.cursor()

        for price in prices:
            c.execute(
                'INSERT OR IGNORE INTO historic_prices(set_id, record_date, price_type, avg, lots, max, min, qty, qty_avg, piece_avg)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (set_id,
                 current_date,
                 price,
                 prices[price]['avg'],
                 prices[price]['lots'],
                 prices[price]['max'],
                 prices[price]['min'],
                 prices[price]['qty'],
                 prices[price]['qty_avg'],
                 prices[price]['piece_avg']))


def add_daily_ratings_to_database(set_id, ratings):
    """

    @param set_id: in standard format xxxx-x
    @param ratings:
    @return:
    """

    con = lite.connect(db)
    with con:
        c = con.cursor()
        c.execute('INSERT OR IGNORE INTO bs_ratings(set_id, want, own, rating, record_date)'
                  ' VALUES (?, ?, ?, ?, ?)',
                  (set_id,
                   ratings['bs_want'],
                   ratings['bs_own'],
                   ratings['bs_score'],
                   LBEF.timestamp()))

    if 'available_us' in ratings or 'available_uk' in ratings:
        check_set_availability_dates(set_id, ratings)


def check_set_availability_dates(set_id, ratings):
    set_dates = {'date_released_us': None, 'date_ended_us': None, 'date_released_uk': None, 'date_ended_uk': None}

    if 'available_us' in ratings:
        set_dates['date_released_us'], set_dates['date_ended_us'] = ratings['available_us']

    if 'available_uk' in ratings:
        set_dates['date_released_uk'], set_dates['date_ended_uk'] = ratings['available_uk']

    con = lite.connect(db)
    with con:
        c = con.cursor()
        c.execute('UPDATE sets SET '
                  'date_released_us=?,'
                  'date_ended_us=?,'
                  'date_released_uk=?,'
                  'date_ended_uk=? '
                  'WHERE id=?;',
                  (set_dates['date_released_us'],
                   set_dates['date_ended_us'],
                   set_dates['date_released_uk'],
                   set_dates['date_ended_uk'],
                   set_id))


def main():
    SET = input("What is the set number?: ")
    print(get_daily(SET))
    main()


if __name__ == "__main__":
    main()