__author__ = 'andrew.sielen'

import sqlite3 as lite
import arrow

from database_management.database_info import database
from database_management.set_info import get_set_id

from data_scrapers import brickset_piece_info as BSPI
from data_scrapers import bricklink_piece_info as BLPI
import LBEF


def add_set_to_database(set):
    """

    @param set:
    @param verbose:
    @return:

     Takes a set with all the appropriate fields and adds it to the database
                INT id
                TXT set_num
                TXT item_num
                TXT item_seq
                TXT set_name
                INT theme_id
                TXT sub_theme
                INT piece_count
                INT unique_piece_count
                INT figures
                FLT set_weight
                FLT piece_weight
                INT year_released
                TXT date_released
                TXT date_ended
                FLT original_price_us
                FLT original_price_uk
                INT age_low
                INT age_high
                TXT box_size
                FLT box_volume
                TXT last_update
    """
    con = lite.connect(database)

    with con:
        c = con.cursor()

        c.execute('INSERT OR IGNORE INTO sets(set_num, set_name) VALUES (?, ?)', (set['set_num'], set['set_name']))
        c.execute('UPDATE sets SET '
                  'item_num=?,'
                  'item_seq=?,'
                  'theme=?,'
                  'subtheme=?,'
                  'piece_count=?,'
                  'figures=?,'
                  'set_weight=?,'
                  'year_released=?,'
                  'date_released_us=?,'
                  'date_ended_us=?,'
                  'date_released_uk=?,'
                  'date_ended_uk=?,'
                  'original_price_us=?,'
                  'original_price_uk=?,'
                  'age_low=?,'
                  'age_high=?,'
                  'box_size=?,'
                  'box_volume=?,'
                  'last_updated=? '
                  'WHERE set_num=? AND set_name=?;',
                  (set['item_num'],
                   set['item_seq'],
                   set['theme'],
                   set['subtheme'],
                   set['piece_count'],
                   set['figures'],
                   set['set_weight'],
                   set['year_released'],
                   set['date_released_us'],
                   set['date_ended_us'],
                   set['date_released_uk'],
                   set['date_ended_uk'],
                   set['original_price_us'],
                   set['original_price_uk'],
                   set['age_low'],
                   set['age_high'],
                   set['box_size'],
                   set['box_volume'],
                   set['last_update'],
                   set['set_num'],
                   set['set_name']))