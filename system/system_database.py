__author__ = 'Andrew'

import os.path


database = os.path.abspath('/Users/andrew.sielen/PycharmProjects/lego_database_scraper/system/system.sqlite')  # for mac
# database = os.path.abspath('system.sqlite')

import sqlite3 as lite


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

