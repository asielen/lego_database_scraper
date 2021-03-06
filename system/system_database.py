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

        c.execute("CREATE UNIQUE INDEX IF NOT EXISTS inflation_idx ON inflation(year)")

        c.execute("CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY,"
                  "date INTEGER, event TEXT, count INTEGER);")
        c.execute("CREATE UNIQUE INDEX IF NOT EXISTS event_idx ON events(event, date)")


def main():
    initiate_database()


if __name__ == "__main__":
    main()

