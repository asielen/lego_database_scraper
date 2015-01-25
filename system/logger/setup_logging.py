__author__ = 'andrew.sielen'

# External
import logging

import arrow


# Only internal dependency is base
from system import base

logging_level = logging.INFO

notes_file = "notes.txt"

def get_week_for_log():
    """
    @return: a text string "YYYYMMDD-WKN.log
    """
    today = arrow.now()
    return today.format('YYYY') + "-WK" + str(today.isocalendar()[1]) + ".log"


def setup_logger():
    log = logging.getLogger('LBEF')
    log.setLevel(logging_level)
    log_path = base.make_project_path(get_week_for_log())
    print("Logging to " + log_path)
    fh = logging.FileHandler(log_path)
    fh.setLevel(logging.WARNING)
    ff = logging.Formatter('%(asctime)s %(name)s %(levelname)-8s: %(message)s')
    fh.setFormatter(ff)
    log.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setLevel(logging_level)
    cf = logging.Formatter('%(name)s %(levelname)s: %(message)s')
    ch.setFormatter(cf)
    log.addHandler(ch)

    #return log


log = logging.getLogger('LBEF')

# Needed to set these up because i over
def log_info(string): log.info(string)
def log_critical(string): log.critical(string)
def log_debug(string): log.debug(string)
def log_error(string): log.error(string)
def log_warning(string): log.warning(string)


def log_note(string):
    with open(notes_file, 'a')  as text_file:
        print(arrow.now('US/Pacific').format('YYYYMMDD HH:mm') + " @ " + string, file=text_file)