__author__ = 'andrew.sielen'

import sqlite3 as lite

import apis.bricklink_api_update_database as blapi
import apis.rebrickable_api_update_database as reapi
from database_management.create_database import initiate_database
from database_management.database import database


def initiate_database_system():
    """
    Update the database with values that won't change:
        Price Types
        BL categories
        Colors

    @return:
    """

    # Create the database
    initiate_database()

    # Add default system values
    insert_price_types()
    insert_colors()
    insert_bl_categories()

    # Add piece info to database


def insert_price_types():
    price_types = (('current_new',), ('current_used',), ('historic_new',), ('historic_used',))
    con = lite.connect(database)

    with con:
        con.execute("DELETE FROM price_types")
        con.executemany("INSERT OR IGNORE INTO price_types(price_type) VALUES (?)", price_types)


def insert_bl_categories():
    blapi.update_categories()


def insert_colors():
    reapi.update_colors()




