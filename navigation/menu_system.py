__author__ = 'andrew.sielen'

import navigation.menu

from database_management.setup_database import initiate_database_system
from apis.bricklink_api.bricklink_update_database import init_parts


def main():
    options = {}
    options['1'] = "Backup Database", backup_database
    options['2'] = "Database Stat Report", run_databaseReport
    options['3'] = "Dump all set data", run_dumpSets
    options['7'] = "Initiate New Database", init_new_database
    options['8'] = "Insert parts", insert_parts
    options['9'] = "Back", navigation.menu.back

    while True:
        result = navigation.menu.options_menu(options)
        if result is 'back':
            break
    print("Run System")


def backup_database():
    print("Backup Database")


def run_databaseReport():
    print("Database Report")


def run_dumpSets():
    print("Dump Sets")


def init_new_database():
    """
    Creates the new database lego_eval.sqlite and populates it with basic info
    @return:
    """
    initiate_database_system()


def insert_parts():
    init_parts()
