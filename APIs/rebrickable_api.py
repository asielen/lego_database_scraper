__author__ = 'Andrew'

import requests

KEY = 'LmtbQqIRtP'


def get_colors():
    """

    @param set_num:
    @return:
    """
    payload = {'key': KEY,  'format': 'json'}
    return requests.get('http://rebrickable.com/api/get_colors', params=payload, verify=False)

def get_set_info(set_id):
    """
    key - API Key
    set_id - The Set ID to look up (e.g. 8043-1)
    format - How to display output data. Valid values: xml, json, csv, tsv
    @param set_num:
    @return:
    """
    payload = {'key': KEY, 'set_id': str(set_id),  'format': 'json'}
    return requests.get('http://rebrickable.com/api/get_set', params=payload, verify=False)

def get_set_inventory(set_num):
    """
    key - API Key
    set - The Set ID to look up (e.g. 8258-1)
    format - How to display output data. Valid values: xml, json, csv, tsv
    @param set_num:
    @return:
    """
    payload = {'key': KEY, 'set': str(set_num), 'format': 'json'}
    return requests.get('http://rebrickable.com/api/get_set_parts', params=payload, verify=False)

def get_piece_info(part_id):
    """
    key - API Key
    part_id - The Part ID to look up (e.g. 3001)
    inc_rels - Optional flag (1 or 0) to include Part Relationships in return data (may be a lot of data for some parts)
    inc_ext - Optional flag (1 or 0) to include external Part IDs (may be a lot of data for some parts due to LEGO element ids)
    format - How to display output data. Valid values: xml, json
    @param piece:
    @return:
    """
    payload = {'key': KEY, 'part_id': part_id, 'inc_ext': 1, format': 'json'}
    return requests.get('http://rebrickable.com/api/get_part', params=payload, verify=False)