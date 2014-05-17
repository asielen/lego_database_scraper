__author__ = 'andrew.sielen'

from database_management.database_info import database
import sqlite3 as lite


con = lite.connect(database)
with con:
    c = con.cursor()
    c.execute("SELECT name FROM sqlite_master;")
    tet = c.fetchall()

print(tet)