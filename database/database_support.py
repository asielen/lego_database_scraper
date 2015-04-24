# External
import sqlite3 as lite
import sys

# Internal
from database import database
import system as syt
if __name__ == "__main__": syt.setup_logger()


def batch_update(sql_text, csvfile, header_len=0):
    """

    @param sql_text:
    @param csvfile:
    @param header_len;
    @return:
    """
    rows_to_process = []
    for idx, row in enumerate(csvfile):
        if idx < header_len:
            continue

        if row is None: continue

        rows_to_process.append(row)

        if idx % 100 == 0:
            syt.log_debug("{} rows processed".format(idx))
            run_batch_sql(sql_text, rows_to_process)
            rows_to_process = []

    syt.log_debug("Inserting Final Rows")
    run_batch_sql(sql_text, rows_to_process)


def run_batch_sql(sql_text, values):
    con = lite.connect(database)

    with con:
        c = con.cursor()
        try:
            c.executemany(sql_text, values)
        except:
            syt.log_note("ERROR: {}".format(sys.exc_info()[0]))
            syt.log_note("Can't insert row: {} / {}".format(len(values), syt.list2string(values)))
            syt.log_error("ERROR: {} | Can't insert row: {} / {}".format(sys.exc_info()[0], len(values),
                                                                        syt.list2string(values)))
            for r in values:
                syt.log_note("Can't insert row: {}".format(syt.list2string(r)))

def run_many_sql(sql_list):
    con = lite.connect(database)

    with con:
        c = con.cursor()
        try:
            for sql_text in sql_list:
                c.execute(sql_text)
        except Exception as e:
            syt.log_error("Database Exception {}".format(e))

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
            if result is not None and isinstance(result, tuple) and len(result) == 1:  # To keep from returning (xxx,)
                result = result[0]
        else:
            result = c.fetchall()
    return result
