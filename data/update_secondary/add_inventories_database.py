__author__ = 'andrew.sielen'

from data.bricklink import bricklink_api as blapi
from data.rebrickable import rebrickable_api as reapi


def add_re_inventories_to_database(update=0):
    reapi.update_set_inventories(update)


def add_bl_inventories_to_database(update=0):
    blapi.update_bl_set_inventories(update)


