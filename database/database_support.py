__author__ = 'andrew.sielen'

import logging
import sqlite3 as lite
import sys

from database import database
import system.base_methods as LBEF


logger = logging.getLogger('LBEF')

def batch_update(sql_text, csvfile, header_len=0):
    """

    @param sql_text:
    @param table:
    @param csvfile:
    @return:
    """
    rows_to_process = []
    for idx, row in enumerate(csvfile):
        if idx < header_len:
            continue

        if row is None: continue

        rows_to_process.append(row)

        if idx % 100 == 0:
            logger.info("{} rows processed".format(idx))
            run_batch_sql(sql_text, rows_to_process)
            rows_to_process = []

    logger.info("Inserting Final Rows")
    run_batch_sql(sql_text, rows_to_process)


def run_batch_sql(sql_text, values):
    con = lite.connect(database)

    with con:
        c = con.cursor()
        try:
            c.executemany(sql_text, values)
        except:
            LBEF.note("ERROR: {}".format(sys.exc_info()[0]))
            LBEF.note("Can't insert row: {} / {}".format(len(values), LBEF.list2string(values)))
            for r in values:
                LBEF.note("Can't insert row: {}".format(LBEF.list2string(r)))


def run_sql(sql_text, insert_list=None, one=False):
    con = lite.connect(database)

    result = None
    with con:
        c = con.cursor()
        if insert_list is not None:
            c.execute(sql_text, tuple(insert_list))
        else:
            c.execute(sql_text)
        if one:
            result = c.fetchone()
        else:
            result = c.fetchall()
    return result
