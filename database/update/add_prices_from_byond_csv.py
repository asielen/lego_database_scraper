__author__ = 'Andrew'

import csv
import sqlite3 as lite

import LBEF
from database.info.database_info import database


BYOND_EVAL_FILE = 'Eval_Data.csv'


def open_csv_file():
    set_id_dict = get_all_set_ids()

    with open(BYOND_EVAL_FILE, 'r') as csvfile:
        historic_prices_generator = csv.reader(csvfile)

        for idx, r in enumerate(historic_prices_generator):
            add_to_database(r, set_id_dict)


def add_to_database(row, set_id_dict):
    set_id = None
    try:
        set_id = set_id_dict[row[0]]
    except:
        try:
            set_id = set_id_dict[LBEF.expand_set_num(row[0])]
        except:

            return None

    date = parse_date(row[4])

    return set_id, date


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


def add_daily_prices_to_database(set_id, price_type, prices):
    current_date = arrow.now('US/Pacific').format('YYYY-MM-DD')

    con = lite.connect(database)
    with con:
        c = con.cursor()

        for price in prices:
            c.execute(
                'INSERT OR IGNORE INTO historic_prices(set_id, record_date, price_type, avg, max, min, qty_avg, piece_avg)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (set_id,
                 current_date,
                 price_type,
                 prices[price]['avg'],
                 prices[price]['max'],
                 prices[price]['min'],
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


def main():
    set = input("Press Enter")
    open_csv_file()


if __name__ == "__main__":
    main()



# row		column	table	price type
# 0	number	set_id	both
# 5	dates	redord_date	both
# 6	BS_own	own	bs_ratings
# 7	BS_want	want	bs_ratings
# 8	BL_P_N6	piece_avg	historic_prices	historic_new
# 9	BL_P_NC	piece_avg	historic_prices	current_new
# 10	BL_P_U6	piece_avg	historic_prices	historic_used
# 11	BL_P_UC	piece_avg	historic_prices	current_used
# 12	BL_N6_Min	min	historic_prices	historic_new
# 13	BL_N6_Max	max	historic_prices	historic_new
# 14	BL_N6_Avg	avg	historic_prices	historic_new
# 15	BL_N6_QAvg	qty_avg	historic_prices	historic_new
# 16	BL_NC_Min	min	historic_prices	current_new
# 17	BL_NC_Max	max	historic_prices	current_new
# 18	BL_NC_Avg	avg	historic_prices	current_new
# 19	BL_NC_QAvg	qty_avg	historic_prices	current_new
# 20	BL_U6_Min	min	historic_prices	historic_used
# 21	BL_U6_Max	max	historic_prices	historic_used
# 22	BL_U6_Avg	avg	historic_prices	historic_used
# 23	BL_U6_QAvg	qty_avg	historic_prices	historic_used
# 24	BL_UC_Min	min	historic_prices	current_used
# 25	BL_UC_Max	max	historic_prices	current_used
# 26	BL_UC_Avg	avg	historic_prices	current_used
# 27	BL_UC_QAvg	qty_avg	historic_prices	current_used
