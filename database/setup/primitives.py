__author__ = 'andrew.sielen'

import logging

logger = logging.getLogger('LBEF')
import sqlite3 as lite

from profilehooks import profile

from navigation import menu
import data.bricklink.bricklink_api as blapi
import data.rebrickable.rebrickable_api as reapi
import data.update_database as update
import database.database as db
import system as sys



#
# Primitive: {these initiate the database from nothing}
# * init_colors()
# @ Download colors
# * init_parts()
# @ Download parts from Bricklink
#         @ Download parts from Rebrickable
#     * init_price_types()
#         @ Internal, no need to download
#     * init_bl_categories()
#         @ Download categories from Bricklink


def init_colors():
    """
    Download and add colors to the database
    @return:
    """
    update.update_colors()


@profile()
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
    con = lite.connect(db.database)

    with con:
        con.execute("DELETE FROM price_types")
        con.executemany("INSERT OR IGNORE INTO price_types(price_type) VALUES (?)", price_types)


def init_bl_categories():
    """
    Download and add bl_categories to the database
    @return:
    """
    blapi.init_categories()


if __name__ == "__main__":
    def main_menu():
        """
        Main launch menu
        @return:
        """
        sys.setup_logging()
        logger = logging.getLogger('LBEF')
        logger.critical("Primitives testing")
        options = {}

        options['1'] = "Initiate Colors", menu_init_colors
        options['2'] = "Initiate Parts", menu_init_parts
        options['3'] = "Initiate Pricetypes", menu_init_price_types
        options['4'] = "Initiate BL Categories", menu_init_bl_categories
        options['9'] = "Quit", menu.quit

        while True:
            result = menu.options_menu(options)
            if result is 'kill':
                exit()


    def menu_init_colors():
        init_colors()


    def menu_init_parts():
        init_parts()


    def menu_init_price_types():
        init_price_types()

    def menu_init_bl_categories():
        init_bl_categories()

    if __name__ == "__main__":
        print("Running as Test")
        main_menu()