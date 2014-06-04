__author__ = 'andrew.sielen'


#
# Primitive: {these initiate the database from nothing}
# * init_colors()
#         @ Download colors
#     * init_parts()
#         @ Download parts from Bricklink
#         @ Download parts from Rebrickable
#     * init_price_types()
#         @ Internal, no need to download
#     * init_bl_categories()
#         @ Download categories from Bricklink

import sqlite3 as lite

import apis.bricklink_api.bricklink_update_database as blapi
import apis.rebrickable_api.rebrickable_update_database as reapi
from database_management.database import database


def init_colors():
    """
    Download and add colors to the database
    @return:
    """
    reapi.update_colors()


def init_parts():
    """
    Pull parts from bulk downloads on bricklink and rebrickable
    @return:
    """
    blapi.init_parts()
    blapi.init_minifigs()
    reapi.update_parts()


def init_price_types():
    """
    Create price_types table
    @return:
    """
    price_types = (('current_new',), ('current_used',), ('historic_new',), ('historic_used',))
    con = lite.connect(database)

    with con:
        con.execute("DELETE FROM price_types")
        con.executemany("INSERT OR IGNORE INTO price_types(price_type) VALUES (?)", price_types)


def init_bl_categories():
    """
    Download and add bl_categories to the database
    @return:
    """
    blapi.init_categories()