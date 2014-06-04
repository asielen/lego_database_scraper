__author__ = 'andrew.sielen'

from io import StringIO
import csv
import json
import html.parser
import gzip

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


def read_gzip_csv_from_url(url):
    """
    Takes a url like: http://rebrickable.com/files/set_pieces.csv.gz
    and returns just a csv.reader object
    @param url:
    @return:
    """
    gzip_bytes = gzip.decompress(requests.get(url).content)
    return read_csv_in_memory(gzip_bytes.decode("utf-8"), ",")


def read_csv_in_memory(csv_string, delimiter='\t'):
    """
    takes a csv string and returns a csv object
    @param csv_string:
    @return:
    """
    string_object = StringIO(csv_string)
    return csv.reader(string_object, delimiter=delimiter)


def print4(list, n=4):
    """
    Print the first four items of a list or iterable
    @param list:
    @param n: number to print, defaults to 4
    @return:
    """
    print()
    for idx, r in enumerate(list):
        print(r)
        if idx >= n: break


def read_json_from_url(url, params=None):
    return json.loads(requests.get(url, params=params, verify=False).text)
