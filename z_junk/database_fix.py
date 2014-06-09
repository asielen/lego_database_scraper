from system.base_methods import LBEF

__author__ = 'Andrew'

import sqlite3 as lite

from database.info.database_info import database


def main():
    con = lite.connect(database)

    with con:
        c = con.cursor()
        c.execute("SELECT id, set_num FROM sets;")
        sets_raw = c.fetchall()
        set_processed = [(n[0], n[1].lower()) for n in sets_raw]

        for set in set_processed:
            set_a, set_b, set_t = LBEF.expand_set_num(set[1])
            c.execute("UPDATE sets SET set_num=?, item_num=?, item_seq=? WHERE id=?;", (set_t, set_a, set_b, set[0]))
        c.execute("SELECT id, set_num FROM sets;")
        sets_raw = c.fetchall()
        print(sets_raw)


if __name__ == "__main__":
    main()