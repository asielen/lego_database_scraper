__author__ = 'andrew.sielen'

import navigation.menu

from database import setup


def main():
    options = {}
    options['1'] = "Backup Database", backup_database
    options['2'] = "Database Stat Report", run_databaseReport
    options['3'] = "Dump all set data", run_dumpSets
    options['7'] = "Initiate New Database", init_new_database
    options['8'] = "Initiate Primitives", insert_parts
    options['9'] = "Back", navigation.menu.back

    while True:
        result = navigation.menu.options_menu(options)
        if result is 'back':
            break
    print("Run System")


def backup_database():
    """
    #Todo Backup
    @return:
    """
    print("Backup Database")


def run_databaseReport():
    """
    #Todo Reporting
    @return:
    """
    print("Database Report")


def run_dumpSets():
    """
    #Todo Reporting
    @return:
    """
    print("Dump Sets")


def init_new_database():
    """
    Creates the new database lego_eval.sqlite and populates it with basic info
    @return:
    """
    setup.create_database()


def insert_parts():
    setup.run_primitives()
