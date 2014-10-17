__author__ = 'andrew.sielen'

from system import config_parser

#
# This file is for global instance variables
#

price_types_lookup = {}
inflation_lookup = {}
update_history = {}

SLOWPOOL = 10
FASTPOOL = 35
RUNNINGPOOL = FASTPOOL


def init_lookups():
    pass


def init_update_history():
    global update_history
    database_config = config_parser.read_config([["Database"]])
    update_history = database_config["Database"]


def init_price_types_lookup():
    global price_types_lookup
    pass


def init_inflation_lookup():
    global inflation_lookup
    pass