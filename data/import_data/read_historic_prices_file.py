__author__ = 'Andrew'

import csv

import arrow

import database as db
from database import info
from system.logger import logger
from system import base_methods as LBEF


def open_dm_csv(file_name='Eval_Data.csv'):
    """
    Takes a csv file, opens it, reads it and adds the data to the database
    @param file_name:
    @return:
    """
    logger.info("$$$ Adding historic prices from csv file")
    set_id_dict = LBEF.list_to_dict(info.get_set_id())

    total_rows = 0

    with open(file_name, 'r') as csvfile:  # Read it through on
        historic_prices = list(csv.reader(csvfile))
        total_rows = len(historic_prices)

    assert total_rows > 0

    price_rows_to_process = []
    rating_rows_to_process = []
    current_price_row = []
    current_rating_row = ()

    timer = LBEF.process_timer("Add historic data to database")

    for idx, r in enumerate(historic_prices):

        current_price_row, current_rating_row = get_rows(r, set_id_dict)
        if current_price_row is None or current_rating_row is None: continue

        price_rows_to_process.extend(current_price_row)
        rating_rows_to_process.append(current_rating_row)

        current_price_row = []
        current_rating_row = ()

        if idx % 1000 == 0:
            logger.info("@@@ Inserting {} Rows".format(len(price_rows_to_process)))
            add_daily_prices_to_database(price_rows_to_process)
            add_daily_ratings_to_database(rating_rows_to_process)
            timer.log_time(len(rating_rows_to_process), total_rows - idx)

            price_rows_to_process = []
            rating_rows_to_process = []

    print("Inserting Final Rows")

    add_daily_prices_to_database(price_rows_to_process)
    add_daily_ratings_to_database(rating_rows_to_process)

    timer.end()


def get_rows(row, set_id_dict):
    set_id = None
    try:
        set_id = set_id_dict[row[0]]
    except:
        try:
            set_id = set_id_dict[LBEF.expand_set_num(row[0])]
        except:
            if len(row) > 0:
                logger.warning("Can't find set: {}".format(row[0]))
            return None, None

    date = parse_date(row[5])

    scrubbed_prices, scrubbed_raiting = scrub_row(set_id, date, row[6:28])
    return scrubbed_prices, scrubbed_raiting


def scrub_row(set_id, date, row):
    price_types = {'current_new': 1, 'current_used': 2, 'historic_new': 3,
                   'historic_used': 4}  # This is the same as what it is stored in the database
    price_list = [(set_id, date, price_types['current_new'], LBEF.float_null(row[12]), LBEF.float_null(row[11]),
                   LBEF.float_null(row[10]), LBEF.float_null(row[13]), LBEF.float_null(row[3])),
                  (set_id, date, price_types['current_used'], LBEF.float_null(row[20]), LBEF.float_null(row[19]),
                   LBEF.float_null(row[18]), LBEF.float_null(row[21]), LBEF.float_null(row[5])),
                  (set_id, date, price_types['historic_new'], LBEF.float_null(row[8]), LBEF.float_null(row[7]),
                   LBEF.float_null(row[6]), LBEF.float_null(row[9]), LBEF.float_null(row[2])),
                  (set_id, date, price_types['historic_used'], LBEF.float_null(row[16]), LBEF.float_null(row[15]),
                   LBEF.float_null(row[14]), LBEF.float_null(row[17]), LBEF.float_null(row[4]))]

    rating_list = (set_id, LBEF.int_null(row[1]), LBEF.int_null(row[0]), date)

    return price_list, rating_list

    # price_dict = {'current_new': dict(set_id=None, date=None, avg=None, max=None, min=None, qty_avg=None, tot=None, qty=None, price_avg=None),
    # 'current_used': dict(set_id=None, date=None, avg=None, max=None, min=None, qty_avg=None, tot=None, qty=None, price_avg=None),
    # 'historic_new': dict(set_id=None, date=None, avg=None, max=None, min=None, qty_avg=None, tot=None, qty=None, price_avg=None),
    # 'historic_used': dict(set_id=None, date=None, avg=None, max=None, min=None, qty_avg=None, tot=None, qty=None, price_avg=None)}
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
    db.batch_update(
        'INSERT OR IGNORE INTO historic_prices(set_id, record_date, price_type, avg, max, min, qty_avg, piece_avg) '
        'VALUES (?,?,?,?,?,?,?,?)', prices)
    # con = lite.connect(db)
    # with con:
    # c = con.cursor()
    #
    #     for price in prices:
    #         c.executemany(
    #             'INSERT OR IGNORE INTO historic_prices(set_id, record_date, price_type, avg, max, min, qty_avg, piece_avg)'
    #             ' VALUES (?, ?, ?, ?, ?, ?, ?, ?)', prices)


def add_daily_ratings_to_database(ratings):
    db.batch_update(
        'INSERT OR IGNORE INTO bs_ratings(set_id, want, own, record_date) VALUES (?,?,?,?)',
        ratings)
    # con = lite.connect(db)
    # with con:
    # c = con.cursor()
    #     c.executemany('INSERT OR IGNORE INTO bs_ratings(set_id, want, own, record_date)'
    #                   ' VALUES (?, ?, ?, ?)', ratings)


def parse_date(s):
    return arrow.get(s[:4] + "-" + s[4:6] + "-" + s[6:]).timestamp

#
# def get_all_set_ids():
    # con = lite.connect(db)
    #     with con:
    #         c = con.cursor()
    #
    #         c.execute("SELECT set_num, id FROM sets")
    #         set_id_list = LBEF.list_to_dict(c.fetchall())
    #
    #     return set_id_list


    # def main():
    # set = input("Press Enter")
    #     open_csv_file()
    #
    #
    # if __name__ == "__main__":
    #     main()