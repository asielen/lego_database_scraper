__author__ = 'andrew.sielen'

import os

import system as syt
import database as db


def backup_database():
    """
    take the current set database and copy it to the system_files/database_backups/ folder
    @return:
    """
    backup_filename = syt.make_project_path("/resources/database_backups/"+syt.add_timestamp_to_filename(db.database))
    syt.log_info("Backing up the database")
    syt.copy_file(db.database, backup_filename)
    syt.log_info("Backedup to {}".format(backup_filename))


def restore_database():
    """
    load a menu with database backups and then take the selected file and copy it to the main database folder
    @return:
    """
    database_backup_menu()

def database_backup_menu():
    """
    Supply a menu of backed up databases and return the selected one
    @return:
    """
    saves_dir = syt.make_dir('/resources/database_backups/')
    def find_backup_databases():
        filenames = os.listdir(saves_dir)
        dbs = []
        for file in filenames:
            if file.endswith(".sqlite"):
                dbs.append(file)
        return dbs

    def _load(file_name):
        print(file_name)
        # return pickle.load(open(saves_dir+file_name, "rb"))

    return syt.Load_Menu(name="- Load Database -", choices=find_backup_databases(), function=_load).run()


def validate_backup_database():
    """
    Give basic stats on the database of choice
    TBD
    @return:
    """
    pass