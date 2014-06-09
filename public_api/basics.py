from system.base_methods import LBEF

__author__ = 'andrew.sielen'

#
# Automated: {run over all sets to update info}
# * add_bl_inventory(set_num)
# * add_re_inventory(set_num)
# @ Api call
#
# Basic: {once the database is initlaized, these are used to update one at a time}
# * add_set(set_num)
#         @ Scrape data from Bricklink & Brickset
#     * add_part(part_num)
#         @ Scrape data from Bricklink & Brickset

# external
import logging

# other modules
import database.info as info
from navigation import menu
import system as sys

import public_api
import data.update_database as update


def add_set_to_database(set_num):
    """
    Takes a set num, pulls all the base stats for it and then adds it to the database
    @param set_num: in the format xxxx-xx
    @return:
    """
    update.add_set_to_database(public_api.get_basestats(set_num, 1))


def add_piece_to_database(bl_id="", bo_id="", re_id=""):
    """

    @param bl_id:
    @return:
    """
    if bl_id == "" and bo_id == "":
        return None

    update.add_part_to_database(public_api.get_piece_info(bl_id=bl_id, bo_id=bo_id, re_id=re_id, type=1))


def add_bl_inventory_to_database(set):
    """

    @param set: in standard format xxxx–x
    @param force:
    @return:
    """
    set_num, set_seq, set = LBEF.expand_set_num(set)

    logging.info("Updating bricklink inventory for set {}".format(set))
    blapi.add_bl_set_inventory_to_database(set)


def get_re_inventory(set):
    pass

    # def get_bs_inventory(set, bs_elements_in_database):
    #     """
    #
    #     @param set:
    #     @param bs_elements_in_database:
    #     @param force:
    #     @return:
    #     """
    #     set_num, set_seq, set = expand_set_num(set)
    #
    #     logging.info("Updating brickset inventory for set {}".format(set))
    #     brickset_pieces = BSP.get_setpieces(set_num, set_seq)
    #     if brickset_pieces is not None:
    #         add_inventories.add_bs_set_pieces_to_database(set, brickset_pieces)


if __name__ == "__main__":
    def main_menu():
        """
        Main launch menu
        @return:
        """
        sys.setup_logging()
        logging.critical("Basics testing")
        options = {}

        options['1'] = "Add Set To Database", menu_add_set_to_database
        options['2'] = "Add Part To Database", menu_add_piece_to_database
        options['3'] = "Add bl_inv to database", menu_add_bl_inventory_to_database
        options['9'] = "Quit", menu.quit

        while True:
            result = menu.options_menu(options)
            if result is 'kill':
                exit()


    def menu_add_set_to_database():
        set_num = LBEF.input_set_num()
        add_set_to_database(set_num)
        print("Added set {} to database? - {}".format(set_num, info.get_set_id(set_num)))


    def menu_add_piece_to_database():
        part_num = input("What part num? ")
        add_piece_to_database(part_num)
        print("Added piece {} to database? - {}".format(part_num, info.get_bl_piece_id(part_num)))


    def menu_add_bl_inventory_to_database():
        set_num = LBEF.input_set_num()
        add_bl_inventory_to_database(set_num)


    if __name__ == "__main__":
        print("Running as Test")
        main_menu()
