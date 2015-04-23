# Internal
from data.bricklink.bricklink_api import bricklink_api as blapi
from data.rebrickable import rebrickable_api as reapi
from data.update_secondary import add_sets_database as secondary_sets


def add_re_inventories_to_database(update=0):
    reapi.update_set_inventories(update)


def add_bl_inventories_to_database(update=0):
    blapi.update_bl_set_inventories(update)


def updates_inv_database_from_api():
    """
    Update the database from an public_api call to bricklink and parses it and updates based on it
    ['Category ID', 'Category Name', 'Number', 'Name', 'Year Released', 'Weight (in Grams)', 'Dimensions']
    And then update all inventories
    @return:
    """
    set_list = blapi.pull_set_catalog()
    secondary_sets.add_sets_to_database(set_list, id_col=2, update=0)
    add_bl_inventories_to_database(update=0)
    add_re_inventories_to_database(update=0)