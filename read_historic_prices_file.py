__author__ = 'Andrew'

import csv
import sqlite3 as lite
import logging

import arrow
from profilehooks import profile

import LBEF
from database.info.database_info import database


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
        price_rows_to_process = []
        raiting_rows_to_process = []
        current_price_row = []
        current_raiting_row = ()
        for idx, r in enumerate(historic_prices_generator):

            current_price_row, current_raiting_row = get_rows(r, set_id_dict)
            if current_price_row is None or current_raiting_row is None: continue

            price_rows_to_process.extend(current_price_row)
            raiting_rows_to_process.append(current_raiting_row)

            current_price_row = []
            current_raiting_row = ()
            if idx % 100 == 0:
                print("Inserting Rows")
                print("[ {0}/{1} {2}% ] complete".format(idx, total, round((idx / total) * 100, 2)))
                add_daily_prices_to_database(price_rows_to_process)
                add_daily_ratings_to_database(raiting_rows_to_process)
                price_rows_to_process = []
                raiting_rows_to_process = []

        print("Inserting Final Rows")

        add_daily_prices_to_database(price_rows_to_process)
        add_daily_ratings_to_database(raiting_rows_to_process)


def get_rows(row, set_id_dict):
    set_id = None
    try:
        set_id = set_id_dict[row[0]]
    except:
        try:
            set_id = set_id_dict[LBEF.expand_set_num(row[0])]
        except:
            if len(row) > 0:
                logging.warning("Can't find set: {}".format(row[0]))
            return None, None

    date = parse_date(row[5])

    scrubbed_prices, scrubbed_raiting = scrub_row(set_id, date, row[6:28])
    return scrubbed_prices, scrubbed_raiting


def scrub_row(set_id, date, row):
    price_types = {'current_new': 1, 'current_used': 2, 'historic_new': 3, 'historic_used': 4}
    price_list = [(set_id, date, price_types['current_new'], LBEF.float_null(row[12]), LBEF.float_null(row[11]),
                   LBEF.float_null(row[10]), LBEF.float_null(row[13]), LBEF.float_null(row[3])),
                  (set_id, date, price_types['current_used'], LBEF.float_null(row[20]), LBEF.float_null(row[19]),
                   LBEF.float_null(row[18]), LBEF.float_null(row[21]), LBEF.float_null(row[5])),
                  (set_id, date, price_types['historic_new'], LBEF.float_null(row[8]), LBEF.float_null(row[7]),
                   LBEF.float_null(row[6]), LBEF.float_null(row[9]), LBEF.float_null(row[2])),
                  (set_id, date, price_types['historic_used'], LBEF.float_null(row[16]), LBEF.float_null(row[15]),
                   LBEF.float_null(row[14]), LBEF.float_null(row[17]), LBEF.float_null(row[4]))]

    raiting_list = (set_id, LBEF.int_null(row[1]), LBEF.int_null(row[0]), date)

    return price_list, raiting_list

    # price_dict = {'current_new': dict(set_id=None, date=None, avg=None, max=None, min=None, qty_avg=None, tot=None, qty=None, price_avg=None),
    # 'current_used': dict(set_id=None, date=None, avg=None, max=None, min=None, qty_avg=None, tot=None, qty=None, price_avg=None),
    #               'historic_new': dict(set_id=None, date=None, avg=None, max=None, min=None, qty_avg=None, tot=None, qty=None, price_avg=None),
    #               'historic_used': dict(set_id=None, date=None, avg=None, max=None, min=None, qty_avg=None, tot=None, qty=None, price_avg=None)}
    #
    # raiting_dict = {'set_id': None, 'date': None, 'bs_want': None, 'bs_own': None}
    #
    #
    # raiting_dict['bs_own'] = LBEF.int_null(row[0])
    # raiting_dict['bs_want'] = LBEF.int_null(row[1])
    #
    # price_dict['current_new']['min'] = LBEF.float_null(row[10])
    # price_dict['current_new']['max'] = LBEF.float_null(row[11])
    # price_dict['current_new']['avg'] = LBEF.float_null(row[12])
    # price_dict['current_new']['qty_avg'] = LBEF.float_null(row[13])
    # price_dict['current_new']['piece_avg'] = LBEF.float_null(row[3])
    #
    # price_dict['current_used']['min'] = LBEF.float_null(row[18])
    # price_dict['current_used']['max'] = LBEF.float_null(row[19])
    # price_dict['current_used']['avg'] = LBEF.float_null(row[20])
    # price_dict['current_used']['qty_avg'] = LBEF.float_null(row[21])
    # price_dict['current_used']['piece_avg'] = LBEF.float_null(row[5])
    #
    # price_dict['historic_new']['min'] = LBEF.float_null(row[6])
    # price_dict['historic_new']['max'] = LBEF.float_null(row[7])
    # price_dict['historic_new']['avg'] = LBEF.float_null(row[8])
    # price_dict['historic_new']['qty_avg'] = LBEF.float_null(row[9])
    # price_dict['historic_new']['piece_avg'] = LBEF.float_null(row[2])
    #
    # price_dict['historic_used']['min'] = LBEF.float_null(row[14])
    # price_dict['historic_used']['max'] = LBEF.float_null(row[15])
    # price_dict['historic_used']['avg'] = LBEF.float_null(row[16])
    # price_dict['historic_used']['qty_avg'] = LBEF.float_null(row[17])
    # price_dict['historic_used']['piece_avg'] = LBEF.float_null(row[4])
    #
    # return price_dict, raiting_dict


def add_daily_prices_to_database(prices):
    """
    (set_id, record_date, price_types[price], prices[price]['avg'], prices[price]['max'], prices[price]['min'], prices[price]['qty_avg'], prices[price]['piece_avg'])
    @param set_id:
    @param record_date:
    @param prices:
    @return:
    """

    con = lite.connect(database)
    with con:
        c = con.cursor()

        for price in prices:
            c.executemany(
                'INSERT OR IGNORE INTO historic_prices(set_id, record_date, price_type, avg, max, min, qty_avg, piece_avg)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?, ?)', prices)


def add_daily_ratings_to_database(raitings):
    con = lite.connect(database)
    with con:
        c = con.cursor()
        c.executemany('INSERT OR IGNORE INTO bs_ratings(set_id, want, own, record_date)'
                      ' VALUES (?, ?, ?, ?)', raitings)


def parse_date(s):
    return arrow.get(s[:4] + "-" + s[4:6] + "-" + s[6:]).timestamp


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