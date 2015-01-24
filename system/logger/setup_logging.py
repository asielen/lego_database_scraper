__author__ = 'andrew.sielen'

import logging

import arrow


logging_level = logging.INFO

notes_file = "notes.txt"

def get_week_for_log():
    """
    @return: a text string "YYYYMMDD-WKN.log
    """
    today = arrow.now()
    return today.format('YYYY') + "-WK" + str(today.isocalendar()[1]) + ".log"


def setup():
    log = logging.getLogger('LBEF')
    log.setLevel(logging_level)
    print("Logging to " + str(get_week_for_log()))
    fh = logging.FileHandler(str(get_week_for_log()))
    fh.setLevel(logging.WARNING)
    ff = logging.Formatter('%(asctime)s %(name)s %(levelname)-8s: %(message)s')
    fh.setFormatter(ff)
    log.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setLevel(logging_level)
    cf = logging.Formatter('%(name)s %(levelname)s: %(message)s')
    ch.setFormatter(cf)
    log.addHandler(ch)

    return log


log = logging.getLogger('LBEF')

# Needed to set these up because i over
def info(string):
    log.info(string)


def critical(string):
    log.critical(string)


def debug(string):
    log.debug(string)



def note(string):
    with open(notes_file, 'a')  as text_file:
        print(arrow.now('US/Pacific').format('YYYYMMDD HH:mm') + " @ " + string, file=text_file)