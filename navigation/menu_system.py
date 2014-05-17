__author__ = 'andrew.sielen'

import navigation.menu

def main():
    options = {}
    options['1'] = "Backup Database", backup_database
    options['2'] = "Database Stat Report", run_databaseReport
    options['3'] = "Dump all set data", run_dumpSets
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