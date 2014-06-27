__author__ = 'andrew.sielen'

# Secondary: {initiate the database, rely on primitives but can still be downloaded in bulk}
# * init_part_color_codes()
# @ Download from Bricklink and add to the database
# * init_sets()
# @ Download sets from Bricklink
# @ Download sets from Rebrickable
#     * init_inventories()
#         @ Download from Rebrickable Api and add to the database
# todo: need to implement this

from profilehooks import profile

import data.bricklink.bricklink_api as blapi
import data.rebrickable.rebrickable_api as reapi
from system.logger import logger
from navigation import menu


def init_part_color_codes():
    """
    Download the part color codes from bricklink and insert them into the database
    @return:
    """
    blapi.init_part_color_codes()


def init_sets():
    """
    Download the list of sets from bricklink and get all their data
    @return:
    """
    blapi.update_sets(check_update=0)
    reapi.update_sets(check_update=0)


@profile
def init_inventories():
    """
    Download inventories for rebrickable and bricklink
    @return:
    """
    blapi.update_bl_set_inventories(check_update=0)
    reapi.update_set_inventories(check_update=0)
    pass


if __name__ == "__main__":
    def main_menu():
        """
        Main launch menu
        @return:
        """
        logger.critical("Secondary testing")
        options = {}

        options['1'] = "Initiate Color Codes", menu_init_part_color_codes
        options['2'] = "Initiate Sets", menu_init_sets
        options['3'] = "Initiate Inventories", menu_init_re_inventories
        options['9'] = "Quit", menu.quit

        while True:
            result = menu.options_menu(options)
            if result is 'kill':
                exit()


    def menu_init_part_color_codes():
        init_part_color_codes()


    def menu_init_sets():
        init_sets()

    def menu_init_re_inventories():
        init_inventories()

    if __name__ == "__main__":
        main_menu()