__author__ = 'andrew.sielen'

import sqlite3 as lite
import logging

import arrow

from database import set_info_old

from database.info.database_info import database
import api
from z_junk import get_daily


def add_daily_set_data_to_database(set_num, prices, ratings):
    """

    @param set_num: in standard format xxxx-x
    @param prices: list of all prices for the day
    @param ratings: current ratings (and date available)
    @return:
    """

    set_id = set_info_old.get_set_id(set_num)

    if set_id is None:  # TODO: This isn't needed with new set_id lookup
        api.get_basestats(set_num)
        set_id = set_info_old.get_set_id(set_num)
        if set_id is None:
            logging.warning("Cannot get daily data because set [{}] is not loading".format(set_num))
            return None

    add_daily_prices_to_database(set_id, prices)

    add_daily_ratings_to_database(set_id, ratings)

    con = lite.connect(database)
    with con:  # Update the last date
        c = con.cursor()
        c.execute('UPDATE sets SET last_price_updated=? WHERE id=?',
                  (arrow.now('US/Pacific').format('YYYY-MM-DD'), set_id))


def add_daily_prices_to_database(set_id, prices):
    current_date = arrow.now('US/Pacific').format('YYYY-MM-DD')

    con = lite.connect(database)
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

    con = lite.connect(database)
    with con:
        c = con.cursor()
        c.execute('INSERT OR IGNORE INTO bs_ratings(set_id, want, own, rating, record_date)'
                  ' VALUES (?, ?, ?, ?, ?)',
                  (set_id,
                   ratings['bs_want'],
                   ratings['bs_own'],
                   ratings['bs_score'],
                   arrow.now('US/Pacific').format('YYYY-MM-DD')))

    if 'available_us' in ratings or 'available_uk' in ratings:
        check_set_availability_dates(set_id, ratings)


def check_set_availability_dates(set_id, ratings):
    set_dates = {'date_released_us': None, 'date_ended_us': None, 'date_released_uk': None, 'date_ended_uk': None}

    if 'available_us' in ratings:
        set_dates['date_released_us'], set_dates['date_ended_us'] = ratings['available_us']

    if 'available_uk' in ratings:
        set_dates['date_released_uk'], set_dates['date_ended_uk'] = ratings['available_uk']

    con = lite.connect(database)
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