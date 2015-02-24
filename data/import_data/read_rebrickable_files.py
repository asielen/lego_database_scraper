# TODO - Not needed anymore?
# External
import csv
import sqlite3 as lite
import pprint as pp

import arrow




# Internal
import system as syt
if __name__ == "__main__": syt.setup_logger()

from database import database as db

# Todo, this whole file I think can be replaced with the rebrickable_api

REBRICKABLE_COLORS = 'colors.csv'
REBRICKABLE_PIECES = 'pieces.csv'
REBRICKABLE_INVENTORIES = 'set_pieces.csv'


def create_color_database():
    """
    Add colors to the database from a colors.csv file
    @return:
    """

    con = lite.connect(db)
    with con:
        c = con.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS colors(id INTEGER PRIMARY KEY,"
                  "of_color_id INTEGER, "
                  "color_name TEXT);")

        c.execute("CREATE UNIQUE INDEX IF NOT EXISTS color_name_idx ON colors(color_name)")
        c.execute("CREATE UNIQUE INDEX IF NOT EXISTS color_idx ON colors(of_color_id)")

    with open(REBRICKABLE_COLORS, 'r') as csvfile:
        colors_get = list(csv.reader(csvfile))[1:]

        with con:
            c = con.cursor()
            c.executemany('INSERT OR IGNORE INTO colors(of_color_id, color_name) VALUES(?, ?)', colors_get)


def check_pieces():
    """
    # Todo fix add part to database call
    compare the pieces in the database to the pieces in the csv file
    @return:
    """
    con = lite.connect(db)
    database_pieces = {}
    with con:
        c = con.cursor()
        c.execute("SELECT design_num, design_name FROM piece_designs")
        database_pieces = syt.list_to_dict(c.fetchall())

    with open(REBRICKABLE_PIECES, 'r', encoding='utf-8') as csvfile:
        pieces_list = {t[0]: t[1] for t in csv.reader(csvfile)}

    diff = syt.DictDiffer(pieces_list, database_pieces)

    # update piece names
    changed_list = dict(diff.changed())
    with con:
        c = con.cursor()
        for rec in changed_list:
            print(changed_list[rec][0], rec)
            c.execute("UPDATE piece_designs SET design_name=? WHERE design_num=?", (changed_list[rec][0], rec))
            # database_pieces = syt.list_to_dict(c.fetchall())

    # add missing pieces
    missing_pieces = diff.added()

    for piece in missing_pieces:
        print("Adding blds element to database: design = " + piece)

        piece_info = BLPI.get_bl_piece_info(piece, missing_pieces[piece])

        if piece_info is None:
            print("blds design info cannot be found: design = " + piece)
            continue

            # add_part_to_database(piece_info)

    pp.pprint(len(missing_pieces))


# #######


# @profile
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
            set_id = set_id_dict[syt.expand_set_num(row[0])]
        except:
            if len(row) > 0:
                syt.log_warning("Can't find set: {}".format(row[0]))
            return None, None

    date = parse_date(row[5])

    scrubbed_prices, scrubbed_raiting = scrub_row(set_id, date, row[6:28])
    return scrubbed_prices, scrubbed_raiting


def add_daily_prices_to_database(prices):
    """
    (set_id, record_date, price_types[price], prices[price]['avg'], prices[price]['max'], prices[price]['min'], prices[price]['qty_avg'], prices[price]['piece_avg'])
    @param set_id:
    @param record_date:
    @param prices:
    @return:
    """

    con = lite.connect(db)
    with con:
        c = con.cursor()

        for price in prices:
            c.executemany(
                'INSERT OR IGNORE INTO historic_prices(set_id, record_date, price_type, avg, max, min, qty_avg, piece_avg)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?, ?)', prices)


def add_daily_ratings_to_database(raitings):
    con = lite.connect(db)
    with con:
        c = con.cursor()
        c.executemany('INSERT OR IGNORE INTO bs_ratings(set_id, want, own, record_date)'
                      ' VALUES (?, ?, ?, ?)', raitings)


def parse_date(s):
    return arrow.get(s[:4] + "-" + s[4:6] + "-" + s[6:]).timestamp


def get_all_set_ids():
    con = lite.connect(db)
    print(db)
    with con:
        c = con.cursor()

        c.execute("SELECT set_num, id FROM sets")
        set_id_list = syt.list_to_dict(c.fetchall())

    return set_id_list


def main():
    set = input("Press Enter")
    check_pieces()


if __name__ == "__main__":
    main()