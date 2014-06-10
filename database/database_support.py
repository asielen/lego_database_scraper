__author__ = 'andrew.sielen'

import logging
import sqlite3 as lite

from database import database


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
            logging.info("{} rows processed".format(idx))
            run_batch_sql(sql_text, rows_to_process)
            rows_to_process = []

    logging.info("Inserting Final Rows")
    run_batch_sql(sql_text, rows_to_process)


def run_batch_sql(sql_text, list):
    con = lite.connect(database)

    with con:
        c = con.cursor()
        c.executemany(sql_text, list)


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
