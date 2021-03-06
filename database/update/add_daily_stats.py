# External
import sqlite3 as lite

# Internal
import database as db
from database import info
import system as syt
if __name__ == "__main__": syt.setup_logger()


def add_daily_set_data_to_database(daily_data):
    """

    @param daily_data: in this format [{set_num: ((get_prices), (ratings))}, {set_num: ((get_prices), (ratings))}]
    @return:
    """

    # First format data
    timestamp = syt.get_timestamp()
    cprices_list_to_insert = []
    cratings_list_to_insert = []
    cdates_list_to_insert = []

    # Get list of price types
    price_types = price_types = {'current_new': 1, 'current_used': 2, 'historic_new': 3,
                                 'historic_used': 4}  # This is the same as what it is stored in the database
    assert len(price_types) == 4

    for s in daily_data:
        cset_id = None

        # Each dict should only be a length of one, so it should grab the first one
        for r in s:
            cset_id = r
            break
        if cset_id is None: continue
        cdaily_data = s[cset_id]
        cprices = cdaily_data[0]
        cratings = cdaily_data[1]

        for price in cprices:
            cprices_list_to_insert.append(
                [cset_id, timestamp, _convert_price_type_to_id(price, price_types), cprices[price]['avg'],
                 cprices[price]['lots'], cprices[price]['max'],
                 cprices[price]['min'], cprices[price]['qty'], cprices[price]['qty_avg'], cprices[price]['piece_avg']])

        cratings_list_to_insert.append(
            [cset_id, cratings['bs_want'], cratings['bs_own'], cratings['bs_score'], timestamp])

        cdates_list_to_insert.append([cratings['available_us'][0], cratings['available_us'][1],
                                      cratings['available_uk'][0], cratings['available_uk'][1], timestamp, cset_id])

    # Now add everything to the database

    # Add get_prices
    db.batch_update(
        'INSERT OR IGNORE INTO historic_prices(set_id, record_date, price_type, avg, lots, max, min, qty, qty_avg, piece_avg) '
        'VALUES (?,?,?,?,?,?,?,?,?,?)', cprices_list_to_insert)
    #Add Raitings
    db.batch_update(
        'INSERT OR IGNORE INTO bs_ratings(set_id, want, own, rating, record_date) VALUES (?,?,?,?,?)',
        cratings_list_to_insert)

    #Update Availible Dates and updated date
    db.batch_update(
        'UPDATE sets SET '
        'date_released_us=?,'
        'date_ended_us=?,'
        'date_released_uk=?,'
        'date_ended_uk=?,'
        'last_price_updated=?'
        'WHERE id=?;', cdates_list_to_insert)


def add_daily_prices_to_database(set_id, prices):
    current_date = syt.get_timestamp()

    con = lite.connect(db.database)
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


def _convert_price_type_to_id(price_type, id_dict=None):
    """
    Take a price _type (eg current_new) and convert it to the equivalent id
    @param price_type:
    @param id_dict:
    @return:
    """
    if id_dict is None:
        id_dict = info.get_bl_piece_ids()
        assert len(id_dict) == 4

    return id_dict[price_type]


def add_daily_ratings_to_database(set_id, ratings):
    """

    @param set_id: in standard format xxxx-x
    @param ratings:
    @return:
    """

    con = lite.connect(db.database)
    with con:
        c = con.cursor()
        c.execute('INSERT OR IGNORE INTO bs_ratings(set_id, want, own, _rating, record_date)'
                  ' VALUES (?, ?, ?, ?, ?)',
                  (set_id,
                   ratings['bs_want'],
                   ratings['bs_own'],
                   ratings['bs_score'],
                   syt.get_timestamp()))

    if 'available_us' in ratings or 'available_uk' in ratings:
        check_set_availability_dates(set_id, ratings)


def check_set_availability_dates(set_id, ratings):
    set_dates = {'date_released_us': None, 'date_ended_us': None, 'date_released_uk': None, 'date_ended_uk': None}

    if 'available_us' in ratings:
        set_dates['date_released_us'], set_dates['date_ended_us'] = ratings['available_us']

    if 'available_uk' in ratings:
        set_dates['date_released_uk'], set_dates['date_ended_uk'] = ratings['available_uk']

    con = lite.connect(db.database)
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


        # def price_capture_menu():
        # # SET = input("What is the _set number?: ")
        # # print(get_daily(SET))
        # # price_capture_menu()
        #
        #
        # if __name__ == "__main__":
        # price_capture_menu()
