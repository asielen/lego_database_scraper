__author__ = 'andrew.sielen'

import sqlite3 as lite
import os.path

import LBEF



# Todo: Make this all work with the new database structure

database = os.path.abspath('lego_sets.sqlite')

# ### General Database information
def get_sets_between_years(start_year, end_year=None):
    """

    @param start_year:
    @param end_year:
    @return: returns all the set ids between start_year and end_year
    """

    if start_year is None: return None

    # Can be used to get all sets from a single year
    if end_year is None:
        end_year == start_year

    con = lite.connect(database)

    with con:
        c = con.cursor()
        c.execute("SELECT set_num FROM sets WHERE year_released BETWEEN ? AND ?;", (start_year, end_year))
        sets_raw = c.fetchall()
        sets = LBEF.flatten_list(sets_raw)

    return sets


def get_set_year_range():
    """
    @return: A tuple with the first and last years in the database
    """

    min_year = None
    max_year = None
    con = lite.connect(database)

    with con:
        c = con.cursor()
        c.execute("SELECT MIN(year_released) FROM sets;")
        min_year = c.fetchone()[0]

        c.execute("SELECT MAX(year_released) FROM sets;")
        max_year = c.fetchone()[0]

    return min_year, max_year


def get_sets_by_year():
    """

    @return: A dictionary with the number of sets per year
    """
    years = []

    con = lite.connect(database)
    with con:
        c = con.cursor()
        c.execute("SELECT year_released, COUNT(set_num) AS NumberOfSets FROM sets GROUP BY year_released;")
        years = c.fetchall()

    return years


def get_sets_by_theme():
    """

    @return: A dictionary with the number of sets per theme
    """
    themes = []

    con = lite.connect(database)
    with con:
        c = con.cursor()
        c.execute("SELECT theme, COUNT(set_num) AS NumberOfSets FROM sets GROUP BY theme;")
        themes = c.fetchall()

    return themes


def get_number_of_sets():
    """

    @return: The number of sets in the databse
    """
    set_num = 0

    con = lite.connect(database)
    with con:
        c = con.cursor()
        c.execute("SELECT COUNT(set_num) FROM sets")
        set_num = c.fetchone()[0]

    return set_num


