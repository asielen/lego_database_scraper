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


def setup_logging():
    logger = logging.getLogger('LBEF')
    logger.setLevel(logging_level)
    print("Logging to " + str(get_week_for_log()))
    fh = logging.FileHandler(str(get_week_for_log()))
    fh.setLevel(logging.WARNING)
    ff = logging.Formatter('%(asctime)s %(name)s %(levelname)-8s: %(message)s')
    fh.setFormatter(ff)
    logger.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setLevel(logging_level)
    cf = logging.Formatter('%(name)s %(levelname)s: %(message)s')
    ch.setFormatter(cf)
    logger.addHandler(ch)

    return logger


logger = logging.getLogger('LBEF')


def note(string):
    with open(notes_file, 'a')  as text_file:
        print(arrow.now('US/Pacific').format('YYYYMMDD HH:mm') + " @ " + string, file=text_file)