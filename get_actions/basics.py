__author__ = 'andrew.sielen'

# The purpose of this file is to create a high level interface to do basic things:
# - Add a set to the database that isn't currently in it - (by scraping/API)
#

from get_actions.get_sets_basestats import get_basestats


def add_set_to_database(set_num):
    """
    Takes a set num, pulls all the base stats for it and then adds it to the database
    @param set_num: in the format xxxx-xx
    @return:
    """
    get_basestats(set_num)


def add_bl_inventory_to_database():
    pass


def add_bs_inventory_to_database():
    pass


def add_bo_inventory_to_database():
    pass