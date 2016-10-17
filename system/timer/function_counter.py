__author__ = 'http://stackoverflow.com/questions/13512391/to-count-no-times-a-function-is-called'

import sqlite3 as lite
from collections import Counter
from functools import wraps

import arrow

import system.base.config as vals
from system import logger
from system.system_database import database

if __name__ == "__main__": logger.setup_logger()


def counter(name=None):
    def counter_decorator(function):
        nonlocal name
        if name is None: name = function.__name__
        @wraps(function)
        def wrapper(*args, **kwargs):
            nonlocal name
            vals.event_counts[name] += 1
            return function(*args, **kwargs)
        return wrapper
    return counter_decorator

def get_counts(clear=0):
    return_counts = Counter(vals.event_counts)
    if clear:
        clear_counts()
    return return_counts

def clear_counts():
    vals.event_counts = Counter()

# Manually add to the counters
def add_to_event(event, count=1):
    if count != 1:
        print("ADD to event: {} | Count: {}".format(event,count))
    vals.event_counts[event] += count

def save_todays_events():
    logger.log_info("Saving Event Count")
    today = arrow.get(arrow.now().date()).timestamp
    get_sql = "SELECT event, count FROM EVENTS WHERE date={}".format(today)
    clear_sql = "DELETE FROM events WHERE date={}".format(today)
    update_sql = "INSERT INTO events(date, event, count) VALUES (?,?,?)"
    con = lite.connect(database)
    with con:
        c = con.cursor()
        existing_list = c.execute(get_sql)
        counts = vals.event_counts + Counter({lst[0]:lst[1] for lst in existing_list})
        insert_list = [(today, e, counts[e]) for e in counts]
        c.execute(clear_sql)
        c.executemany(update_sql, insert_list)
        clear_counts()
    logger.log_info("Done Saving Event Count")

def merge_count_dicts(e_counts1, e_counts2=None):
    if e_counts2 is None: e_counts2=vals.event_counts
    return e_counts1 + e_counts2

def set_merge_event_counts(e_counts1):
    vals.event_counts = e_counts1 + vals.event_counts

def pool_skimmer(pool_lists):
    if pool_lists:
        return_list = []
        for n in pool_lists:
            set_merge_event_counts(n[-1])
            return_list.extend(tuple(n[:-1]))
        return return_list
