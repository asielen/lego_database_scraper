__author__ = 'andrew.sielen'

import sqlite3 as lite
import pprint as pp
import arrow


def add_daily2database(set_num, prices, ratings):

    con = lite.connect('lego_sets.sqlite')

    set_id = None

    with con:
        c = con.cursor()
        set_id = ud.get_set_id(set_num, c)

    if set_id is None:
        get_set.get_basestats(set_num)
        with con:
            c = con.cursor()
            set_id = ud.get_set_id(set_num, c)
        if set_id is None: raise AssertionError


    add_dailyPrices2database(set_id, prices)

    add_dailyRatings2database(set_id, ratings)


def add_dailyPrices2database(set_id, prices):


    current_date = arrow.now('US/Pacific').format('YYYY-MM-DD')
    con = lite.connect('lego_sets.sqlite')

    with con:
        c = con.cursor()

        for price in prices:
            c.execute('INSERT OR IGNORE INTO historic_prices(set_id, record_date, price_type, avg, lots, max, min, qty, qty_avg, piece_avg)'
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

def add_dailyRatings2database(set_id, ratings):
    #need to add this next 2014 05 13
    con = lite.connect('lego_sets.sqlite')
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
        check_setAvailability(set_id, ratings)

def check_setAvailability(set_id, ratings):

    set_dates = {'date_released_us': None, 'date_ended_us': None, 'date_released_uk': None, 'date_ended_uk': None}

    if 'available_us' in ratings:
        set_dates['date_released_us'], set_dates['date_ended_us'] = ratings['available_us']

    if 'available_uk' in ratings:
        set_dates['date_released_uk'], set_dates['date_ended_uk'] = ratings['available_uk']

    con = lite.connect('lego_sets.sqlite')
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
    pp.pprint(get_daily(SET))
    main()

if __name__ == "__main__":
    main()