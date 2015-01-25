__author__ = 'Andrew'

# External
import sqlite3 as lite

# Internal
from system import base

# database = os.path.abspath('/Users/andrew.sielen/PycharmProjects/lego_database_scraper/system/system.sqlite')  # for mac
# database = os.path.abspath('system.sqlite')
database = base.make_project_path('system/system.sqlite')

def initiate_database():
    con = lite.connect(database)
    with con:
        c = con.cursor()

        c.execute("CREATE TABLE IF NOT EXISTS inflation(id INTEGER PRIMARY KEY,"
                  "year INTEGER, cpi REAL);")

        c.execute("CREATE UNIQUE INDEX inflation_idx ON inflation(year)")


def main():
    initiate_database()


if __name__ == "__main__":
    main()

