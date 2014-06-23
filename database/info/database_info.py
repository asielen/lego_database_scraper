from system.base_methods import LBEF

__author__ = 'andrew.sielen'

import sqlite3 as lite

import database as db


# Todo: Make this all work with the new database structure

# database = os.path.abspath('/Users/andrew.sielen/PycharmProjects/lego_database_scraper/lego_sets.sqlite')

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

    @return: The number of sets in the database
    """
    set_num = 0

    con = lite.connect(database)
    with con:
        c = con.cursor()
        c.execute("SELECT COUNT(set_num) FROM sets")
        set_num = c.fetchone()[0]

    return set_num


def get_bl_category_id(category_num):
    """
    @param category_num: the category num used by bricklink
    @return: the primary key for a category in the database
    """

    element_id = None
    con = lite.connect(db.database)
    with con:
        c = con.cursor()
        c.execute('SELECT id FROM bl_categories WHERE bl_category_id=?', (category_num,))
        element_id_raw = c.fetchone()
        if element_id_raw is None:
            return None
        element_id = element_id_raw[0]

    return element_id


def read_bl_categories():
    """

    @return: a list in this format [category_id, id]
    """
    return LBEF.list_to_dict(db.run_sql('SELECT bl_category_id, id FROM bl_categories'))


def read_bl_colors():
    """

    @return: a list in this format {color_id, id}
    """
    return LBEF.list_to_dict(db.run_sql('SELECT bl_color_id, id FROM colors'))


def read_re_colors():
    """

    @return: a list in this format {color_id, id}
    """
    return LBEF.list_to_dict(db.run_sql('SELECT re_color_id, id FROM colors'))


def read_bl_colors_name():
    """

    @return: a list in this format {color_name, id}
    """
    return LBEF.list_to_dict(db.run_sql('SELECT bl_color_name, id FROM colors'))


def read_bl_sets():
    """

    @return: a list in this format {set_num: [set]}
    """
    bl_set_list = db.run_sql('SELECT * FROM sets')
    return {b[1]: b[:] for b in bl_set_list}  # 1 is the position of the bricklink column


def read_bl_set_ids():
    """

    @return: a list in this format {id: set_num}
    """
    bl_set_list = db.run_sql('SELECT * FROM sets')
    return {b[0]: b[1] for b in bl_set_list}  # 1 is the position of the bricklink column


def read_bl_invs():
    """

    @return: a list of the sets who's inventory is in the system
    """
    bl_set_list = db.run_sql('SELECT * FROM bl_inventories')
    bl_set_list = set(b[1] for b in bl_set_list)
    return bl_set_list


def read_re_invs():
    """

    @return: a list of the sets who's inventory is in the system
    """
    re_set_list = db.run_sql('SELECT * FROM re_inventories')
    re_set_list = set(b[1] for b in re_set_list)
    return re_set_list


def read_bl_parts():
    """

    @return: a dict in this format {part_num: id, }
    """
    return LBEF.list_to_dict(db.run_sql('SELECT bricklink_id, id FROM parts'))


def read_re_parts():
    """

    @return: a dict in this format {part_num: id, }
    """
    return LBEF.list_to_dict(db.run_sql('SELECT rebrickable_id, id FROM parts'))