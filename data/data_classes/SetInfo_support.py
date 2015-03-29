__author__ = 'Andrew'

import random

import database as db


def get_random():
    """

    @return: Get a random set from the database (for testing)
    """
    set_list = db.run_sql('SELECT set_num FROM sets')
    return random.choice(set_list)[0]


def input_set_num(type=0):
    """
    @param type: 0 or 1
    @return: if type == 1 xxxx, y, xxxx-y
    @return: else return xxxx-y
    """
    set_num = input("What set num? ")
    if set_num == "rand":
        set_num = get_random()
        print("Random Set: {}".format(set_num))
    if type == 1:
        return expand_set_num(set_num)
    else:
        return expand_set_num(set_num)[2]


def expand_set_num(set_id):
    """

    @param set_id: in standard format xxxx-yy
    @return: xxxx, yy, xxxx-yy
    """

    set_id = set_id.lower()
    try:
        if ' or ' in set_id:
            set_id = set_id.split(' or ')[0]
        set_list = set_id.split("-")
        if len(set_list) > 2: return (None, None, set_id)
        set_num = set_list[0]
        set_seq = set_list[1]
    except:
        set_num = set_id
        set_seq = '1'
    return set_num, set_seq, set_num + '-' + set_seq