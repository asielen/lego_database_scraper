__author__ = 'Andrew'
# Todo, have an option to update the inflation rate automatically from here:
#http://inflationdata.com/Inflation/Consumer_Price_Index/HistoricalCPI.aspx?reloaded=true#Table
# External
import csv
import sqlite3 as lite

import arrow





# Internal - Should have none outside system
from system import base
from system.system_database import database


inflation_sheet = base.make_project_path('system/historic_cpi.csv')


def get_cpis():
    """
    get a dict of all cpis to lookup
    @return:
    """
    result = None
    con = lite.connect(database)
    with con:
        c = con.cursor()
        c.execute("SELECT year, cpi FROM inflation")
        result = base.list_to_dict(c.fetchall())
    return result


def adj_dict_for_inf(price_dict, inf_year=None):
    """

    @param price_dict: In the format {date_ts:price,date_ts:price}
    @param inf_year: the year to adjust to
    @return:
    """
    if not isinstance(inf_year, int):
        inf_year = arrow.get().year
    cpi_dict = get_cpis()
    inf_year = min(inf_year, max(cpi_dict.keys()))
    for pd in price_dict:
        cyear = arrow.get(pd).year
        rate = _get_inflation_rate(cpi_dict[min(cyear, inf_year)], cpi_dict[inf_year])
        price_dict[pd] = _get_adjusted_price(price_dict[pd], rate)
    return price_dict


def _get_inflation_rate(start_cpi, end_cpi):
    return ((end_cpi - start_cpi) / start_cpi)


def _get_adjusted_price(price, inflation_rate):
    if price is None:
        print("ERROR")
    return (price * inflation_rate) + price


def get_inflation_rate(year_start, year_end=2015):
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
    @return:
    """
    with open(inflation_sheet, 'r') as csvfile:
        inflation_chart = csv.reader(csvfile)
        inflation_chart = base.list_to_dict(inflation_chart)
        del inflation_chart['year']

    con = lite.connect(database)

    with con:
        c = con.cursor()

        for n in inflation_chart:
            c.execute('INSERT OR IGNORE INTO inflation(year, cpi) VALUES (?, ?)', (n, inflation_chart[n]))
            c.execute('UPDATE inflation SET cpi=? WHERE year=?', (n, inflation_chart[n]))


def main():
    update_inflation_database()
    print(get_inflation_rate(1915, 2015))

if __name__ == "__main__":
    main()