__author__ = 'andrew.sielen'

from io import StringIO
import csv
import json
import html.parser

import requests


def read_csv_from_url(url, params=None, delimiter='\t'):
    """
    Wrapper to make syntax simpler
    also handles errors
    @param url:
    @param parameters:
    @return:
    """
    h = html.parser.HTMLParser()
    return read_csv_in_memory(h.unescape(requests.get(url, params=params, verify=False).text), delimiter)


def read_csv_in_memory(csv_string, delimiter='\t'):
    """
    takes a csv string and returns a csv object
    @param csv_string:
    @return:
    """
    string_object = StringIO(csv_string)
    return csv.reader(string_object, delimiter=delimiter)


def print4(list):
    """
    Print the first four items of a list or iterable
    @param list:
    @return:
    """
    print()
    for idx, r in enumerate(list):
        print(r)
        if idx >= 4: break


def read_json_from_url(url, params=None):
    return json.loads(requests.get(url, params=params, verify=False).text)
