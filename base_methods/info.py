__author__ = 'andrew.sielen'

import sqlite3 as lite

from database_management.database import database
from base_methods import basics


def get_set_id(set_num, add=False):
    """
    @param set_num:
    @param add: if True, Add the set if it is missing in the databse
    @return: the id column num of the set in the database
    """
    print(database)
    con = lite.connect(database)
    with con:
        c = con.cursor()
        c.execute('SELECT id FROM sets WHERE set_num=?', (set_num,))
        set_id_raw = c.fetchone()
    if set_id_raw is None:
        if add == True:
            basics.add_set_to_database(set_num)
            return get_set_id(set_num)
        else:
            return None
    else:
        return set_id_raw[0]


