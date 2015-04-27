__author__ = 'andrew.sielen'

import database as db
import system as syt

def get_basic_database_info():
    """

    """
    total_set_weight = db.run_sql('SELECT SUM(set_weight) FROM sets;', one=True)
    total_num_pieces = db.run_sql('SELECT SUM(piece_count) FROM sets;', one=True)
    num_of_themes = db.run_sql('SELECT COUNT(DISTINCT theme) FROM sets;', one=True)
    num_of_sets = db.run_sql('SELECT COUNT(DISTINCT set_num) FROM sets;', one=True)
    db_range_min, db_range_max = db.run_sql('SELECT MIN(year_released), max(year_released) FROM sets;', one=True)
    total_ppp = db.run_sql('SELECT SUM(original_price_us)/SUM(piece_count) FROM sets;', one=True)
    min_price, max_price = db.run_sql('SELECT MIN(original_price_us), max(original_price_us) FROM sets;', one=True)

    stat_string = ""
    stat_string += "    Database contains: {} sets in {} themes representing:\n".format(num_of_sets, num_of_themes)
    stat_string += "            Years {} to {}\n".format(db_range_min, db_range_max)
    stat_string += "            Prices {} to {}\n".format(min_price, max_price)
    stat_string += "            Total number of pieces: {}\n".format(total_num_pieces)
    stat_string += "            Total weight: {}\n".format(total_set_weight)
    stat_string += "            Total price per piece: {}\n".format(total_ppp)
    syt.log_info(stat_string)

def page_size():
    psize = db.run_sql('PRAGMA PAGE_COUNT;', one=True)
    return psize

