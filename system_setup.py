__author__ = 'andrew.sielen'

import logging
import arrow
import sys


def get_week_for_log():
    """
    @return: a text string "YYYYMMDD-WKN.log
    """
    today = arrow.now()
    return today.format('YYYY') + "-WK" + str(today.isocalendar()[1]) + ".log"


def setup_logging():
    logging.basicConfig(filename=str(get_week_for_log()), level=logging.WARNING)
    logging.basicConfig(format='%(asctime)s : %(message)s')

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)

