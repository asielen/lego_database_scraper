__author__ = 'andrew.sielen'

import navigation.menu

from database import setup
from system.logger import logger


def main():
    options = {}
    options['1'] = "Backup Database", backup_database  # Todo
    options['2'] = "Database Stat Report", run_databaseReport  # Todo
    options['3'] = "Dump all set data", run_dumpSets  # Todo
    options['6'] = "Initiate New Database", init_new_database  # Working 2014-10-5
    options['7'] = "Initiate Primitives", menu_run_primitives  # Working 2014-10-5
    options['8'] = "Build All", menu_build_all
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


def menu_run_primitives():
    setup.run_primitives()


def menu_build_all():
    logger.info("Creating Database")
    setup.create_database()
    logger.info("Creating Primitives")
    setup.run_primitives()
    logger.info("Creating Secondaries")
    setup.run_secondary()


if __name__ == "__main__":
    main()