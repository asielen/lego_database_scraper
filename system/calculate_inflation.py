from system.base_methods import LBEF

__author__ = 'Andrew'

import csv
import sqlite3 as lite

from system.system_database import database

inflation_sheet = 'system/historic_cpi.csv'


def get_inflation_rate(year_start, year_end=2013):
    """

    @param year_start:
    @param year_end:
    @return: the multiplier for system
    """

    con = lite.connect(database)
    with con:
        c = con.cursor()

        c.execute("SELECT cpi FROM inflation WHERE year=?", (year_start,))
        year_start_raw = c.fetchone()
        if year_start_raw is None: return None
        start_cpi = year_start_raw[0]

        c.execute("SELECT cpi FROM inflation WHERE year=?", (year_end,))
        year_end_raw = c.fetchone()
        if year_end_raw is None:
            c.execute("SELECT cpi FROM inflation WHERE year=?", (2013,))
            year_end_raw = c.fetchone()
        end_cpi = year_end_raw[0]

    return ((end_cpi - start_cpi) / start_cpi)


def update_inflation_database():
    """

    @param inflation_sheet:
    @return:
    """
    with open(inflation_sheet, 'r') as csvfile:
        inflation_chart = csv.reader(csvfile)
        inflation_chart = LBEF.list_to_dict(inflation_chart)

    con = lite.connect(database)

    with con:
        c = con.cursor()

        for n in inflation_chart:
            c.execute('INSERT OR IGNORE INTO inflation(year, cpi) VALUES (?, ?)', (n, inflation_chart[n]))
            c.execute('UPDATE inflation SET cpi=? WHERE year=?', (n, inflation_chart[n]))


def main():
    print(get_inflation(1915, 2013))


if __name__ == "__main__":
    main()