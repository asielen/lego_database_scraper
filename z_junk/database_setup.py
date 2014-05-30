__author__ = 'Andrew'

import sqlite3 as lite

from database_management.database_info import database


def initiate_database():
    con = lite.connect(database)
    with con:
        c = con.cursor()
        # Build pieces table
        c.execute("CREATE TABLE IF NOT EXISTS piece_designs(id INTEGER PRIMARY KEY,"
                  "design_num TEXT,"
                  "design_name TEXT,"
                  "design_alts TEXT,"
                  "weight REAL, "
                  "piece_type TEXT);")

        c.execute("CREATE TABLE IF NOT EXISTS price_types(id INTEGER PRIMARY KEY,"
                  "price_type TEXT);")

        c.execute("CREATE TABLE IF NOT EXISTS bl_cataegories(id INTEGER PRIMARY KEY,"
                  "bl_category_id INTEGER, "
                  "category TEXT);")


        #need to add default values for price_types

        c.execute("CREATE TABLE IF NOT EXISTS unique_pieces(id INTEGER PRIMARY KEY,"
                  "part_num TEXT,"
                  "design_id INTEGER,"
                  "color_name TEXT,"
                  "FOREIGN KEY (design_id) REFERENCES piece_designs(id));")

        #Build sets table
        c.execute("CREATE TABLE IF NOT EXISTS sets(id INTEGER PRIMARY KEY,"
                  "set_num TEXT,"
                  "item_num TEXT,"
                  "item_seq TEXT,"
                  "set_name TEXT,"
                  "theme TEXT,"
                  "subtheme TEXT,"
                  "piece_count INTEGER,"
                  "figures INTEGER,"
                  "set_weight REAL,"
                  "year_released INTEGER,"
                  "date_released_us TEXT,"
                  "date_ended_us TEXT,"
                  "date_released_uk TEXT,"
                  "date_ended_uk TEXT,"
                  "original_price_us REAL,"
                  "original_price_uk REAL,"
                  "age_low INTEGER,"
                  "age_high INTEGER,"
                  "box_size TEXT,"
                  "box_volume REAL,"
                  "last_updated TEXT,"
                  "last_inv_updated_bs TEXT,"
                  "last_inv_updated_bl TEXT,"
                  "last_price_updated TEXT);")

        #Build historic_prices table
        c.execute("CREATE TABLE IF NOT EXISTS historic_prices(id INTEGER PRIMARY KEY,"
                  "set_id INTEGER,"
                  "record_date INTEGER,"
                  "price_type INTEGER,"  #current_new, current_used, historic_new, historic_used
                  "avg REAL,"
                  "lots REAL,"
                  "max REAL,"
                  "min REAL,"
                  "qty REAL,"
                  "qty_avg REAL,"
                  "piece_avg REAL,"
                  "FOREIGN KEY (set_id) REFERENCES sets(id),"
                  "FOREIGN KEY (price_type) REFERENCES price_types(id));")

        #Build inventories table
        c.execute("CREATE TABLE IF NOT EXISTS bs_inventories(id INTEGER PRIMARY KEY,"
                  "set_id INTEGER,"
                  "piece_id INTEGER,"
                  "quantity INTEGER,"
                  "FOREIGN KEY (set_id) REFERENCES sets(id),"
                  "FOREIGN KEY (piece_id) REFERENCES unique_pieces(id));")

        c.execute("CREATE TABLE IF NOT EXISTS bl_inventories(id INTEGER PRIMARY KEY,"
                  "set_id INTEGER,"
                  "piece_id INTEGER,"
                  "quantity INTEGER,"
                  "FOREIGN KEY (set_id) REFERENCES sets(id),"
                  "FOREIGN KEY (piece_id) REFERENCES unique_pieces(id));")

        c.execute("CREATE TABLE IF NOT EXISTS bs_ratings(id INTEGER PRIMARY KEY,"
                  "set_id INTEGER,"
                  "want INTEGER,"
                  "own INTEGER,"
                  "rating INTEGER,"
                  "record_date INTEGER,"
                  "FOREIGN KEY (set_id) REFERENCES sets(id));")

        c.execute("CREATE UNIQUE INDEX price_type_idx ON price_types(price_type)")

        c.execute("CREATE UNIQUE INDEX design_num_idx ON piece_designs(design_num)")

        c.execute("CREATE UNIQUE INDEX part_num_idx ON unique_pieces(part_num)")

        c.execute("CREATE UNIQUE INDEX set_num_idx ON sets(set_num)")
        c.execute("CREATE INDEX set_name_idx ON sets(set_name)")

        c.execute("CREATE UNIQUE INDEX price_type_date_idx ON historic_prices(set_id, price_type, record_date)")

        c.execute("CREATE UNIQUE INDEX rating_type_date_idx ON bs_ratings(set_id, record_date)")


initiate_database()