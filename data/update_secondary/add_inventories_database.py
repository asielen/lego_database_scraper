__author__ = 'andrew.sielen'

from data.bricklink import bricklink_api as blapi


def add_re_inventories_to_database():
    pass


def add_bl_inventories_to_database():
    blapi.update_bl_set_inventories()


