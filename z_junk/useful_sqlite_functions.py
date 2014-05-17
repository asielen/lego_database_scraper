__author__ = 'andrew.sielen'

import sqlite3 as lite
import arrow
import LBEF

def compare_dateRange(column, set_num, checkDate, interval=5, inclusive=1):
    """
    Checks if a date [checkDate] is between two dates in the sets table

    @param column: which column in the database
    @param set_num: which set to check
    @param checkDate: the
    @param startDate:
    @param endDate:
    @param inclusive: 1 includes the ends dates, 0 excludes them
    @return: True if the end date is between startDate and endDate, False otherwise
    """

    try:
        con = lite.connect('lego_sets.sqlite')
        with con:
            c = con.cursor()
            c.execute("SELECT ? FROM sets WHERE set_num=?", (column, set_num,))
            last_updated = c.fetchone()[0]
            if last_updated is None:
                return False
            last_updated = arrow.get(last_updated)

            return LBEF.check_in_date_range(last_updated, last_updated.replace(days=-interval),
                                                        last_updated.replace(days=+interval))
    except:
        return False
