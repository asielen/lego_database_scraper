__author__ = 'Andrew'

import csv
import sqlite3 as lite
import LBEF
from database_management.database_info import database
import logging
from profilehooks import profile

BYOND_EVAL_FILE = 'Eval_Data.csv'

@profile
def open_csv_file():
    set_id_dict = get_all_set_ids()

    total = 0
    with open(BYOND_EVAL_FILE, 'r') as csvfile:
        historic_prices_generator = csv.reader(csvfile)
        for i, l in enumerate(historic_prices_generator): pass
        total = i
    with open(BYOND_EVAL_FILE, 'r') as csvfile:
        historic_prices_generator = csv.reader(csvfile)
        for idx, r in enumerate(historic_prices_generator):
            add_to_database(r, set_id_dict)
            print("[ {0}/{1} {2}% ] complete".format(idx, total, round((idx / total) * 100, 2)))

def add_to_database(row, set_id_dict):
    set_id = None
    try:
        set_id = set_id_dict[row[0]]
    except:
        try:
            set_id = set_id_dict[LBEF.expand_set_num(row[0])]
        except:
            return None

    date = parse_date(row[5])

    scrubbed_prices, scrubbed_raiting = scrub_row(row[6:28])
    add_daily_prices_to_database(set_id, date, scrubbed_prices)
    add_daily_ratings_to_database(set_id, date, scrubbed_raiting)
    return 0


def scrub_row(row):
    price_dict = {'current_new': dict(avg=None, max=None, min=None, qty_avg=None, tot=None, qty=None, price_avg=None),
                  'current_used': dict(avg=None, max=None, min=None, qty_avg=None, tot=None, qty=None, price_avg=None),
                  'historic_new': dict(avg=None, max=None, min=None, qty_avg=None, tot=None, qty=None, price_avg=None),
                  'historic_used': dict(avg=None, max=None, min=None, qty_avg=None, tot=None, qty=None, price_avg=None)}

    raiting_dict = {'bs_want': None, 'bs_own': None}


    raiting_dict['bs_own'] = LBEF.int_null(row[0])
    raiting_dict['bs_want'] = LBEF.int_null(row[1])

    price_dict['current_new']['min'] = LBEF.float_null(row[10])
    price_dict['current_new']['max'] = LBEF.float_null(row[11])
    price_dict['current_new']['avg'] = LBEF.float_null(row[12])
    price_dict['current_new']['qty_avg'] = LBEF.float_null(row[13])
    price_dict['current_new']['piece_avg'] = LBEF.float_null(row[3])

    price_dict['current_used']['min'] = LBEF.float_null(row[18])
    price_dict['current_used']['max'] = LBEF.float_null(row[19])
    price_dict['current_used']['avg'] = LBEF.float_null(row[20])
    price_dict['current_used']['qty_avg'] = LBEF.float_null(row[21])
    price_dict['current_used']['piece_avg'] = LBEF.float_null(row[5])

    price_dict['historic_new']['min'] = LBEF.float_null(row[6])
    price_dict['historic_new']['max'] = LBEF.float_null(row[7])
    price_dict['historic_new']['avg'] = LBEF.float_null(row[8])
    price_dict['historic_new']['qty_avg'] = LBEF.float_null(row[9])
    price_dict['historic_new']['piece_avg'] = LBEF.float_null(row[2])

    price_dict['historic_used']['min'] = LBEF.float_null(row[14])
    price_dict['historic_used']['max'] = LBEF.float_null(row[15])
    price_dict['historic_used']['avg'] = LBEF.float_null(row[16])
    price_dict['historic_used']['qty_avg'] = LBEF.float_null(row[17])
    price_dict['historic_used']['piece_avg'] = LBEF.float_null(row[4])

    return price_dict, raiting_dict

def add_daily_prices_to_database(set_id, record_date, prices):

    con = lite.connect(database)
    with con:
        c = con.cursor()

        for price in prices:
            c.execute('INSERT OR IGNORE INTO historic_prices(set_id, record_date, price_type, avg, max, min, qty_avg, piece_avg)'
                      ' VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                        (set_id,
                        record_date,
                        price,
                        prices[price]['avg'],
                        prices[price]['max'],
                        prices[price]['min'],
                        prices[price]['qty_avg'],
                        prices[price]['piece_avg']))

def add_daily_ratings_to_database(set_id, record_date, ratings):

    con = lite.connect(database)
    with con:
        c = con.cursor()
        c.execute('INSERT OR IGNORE INTO bs_ratings(set_id, want, own, record_date)'
                      ' VALUES (?, ?, ?, ?)',
                      (set_id,
                      ratings['bs_want'],
                      ratings['bs_own'],
                      record_date))

def parse_date(s):
    return s[:4] + "-" + s[4:6] + "-" + s[6:]


def get_all_set_ids():
    con = lite.connect(database)
    print(database)
    with con:
        c = con.cursor()

        c.execute("SELECT set_num, id FROM sets")
        set_id_list = LBEF.list_to_dict(c.fetchall())

    return set_id_list


def main():
    set = input("Press Enter")
    open_csv_file()


if __name__ == "__main__":
    main()