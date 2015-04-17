# Internal

from database import setup

import system as syt
if __name__ == "__main__": syt.setup_logger()



def main():
    options = (
        ("Backup Database", backup_database),
        ("Database Stat Report", run_databaseReport),
        ("Dump all _set data", run_dumpSets),
        ("Initiate New Database", init_new_database),
        ("Initiate Primitives", menu_run_primitives),
        ("Build All", menu_build_all),
    )
    syt.Menu(name="– System –", choices=options).run()


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
    syt.log_info("Creating Database")
    setup.create_database()
    syt.log_info("Creating Primitives")
    setup.run_primitives()
    syt.log_info("Creating Secondaries")
    setup.run_secondary()


if __name__ == "__main__":
    main()