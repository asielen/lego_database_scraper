from system import notes_file

__author__ = 'andrew.sielen'

import re  # Regular expressions
import logging
import csv
import gzip
import html.parser
from io import StringIO
import json
from time import sleep

import requests
from bs4 import BeautifulSoup
import arrow


invalid_urls = 0
logger = logging.getLogger('LBEF')


def soupify(url):
    """

    @param url: any url
    @return: returns the soup for that url
    """
    global invalid_urls
    try:
        page = requests.get(url, timeout=10).content
    except:
        try:
            page = requests.get(url, timeout=20).content
        except:
            invalid_urls += 1
            logger.error("INVALID URL {}: Can't reach the url! {}".format(invalid_urls, url))
            return None
    soup = BeautifulSoup(page)
    if soup is None:
        logger.error("Can't make the soup! {}".format(url))
        soup = BeautifulSoup(page)

    # Check that bricklink isn't down
    available = soup.find(text="System Unavailable")
    if available is not None:
        bold = soup.find('b').text[-10:-9]
        logger.warning("bricklink down for maintenence, it will be back in {} minutes.".format(bold))
        logger.info("Waiting to continue")
        for n in range(1, int_zero(bold)):
            sleep(60)
            logger.info("{} minutes remaining".format(int_zero(bold) - n))
        return soupify(url)
    return soup


def is_number(s):
    """

    @param s: an int
    @return:
    """
    try:
        float(s)
        return True
    except ValueError:
        return False


def only_numerics_float(s):
    """

    @param s: a string
    @return: an int stripped of all non-numeric characters or None
    """
    non_decimal = re.compile(r'[^\d.]+')
    s = float_null(non_decimal.sub('', s))
    return s


def only_numerics_int(s):
    """

    @param s: a string
    @return: an int stripped of all non-numeric characters or None
    """
    non_decimal = re.compile(r'[^\d.]+')
    s = int_null(non_decimal.sub('', s))
    return s


def int_null(s):
    """

    @param s: a string
    @return: an int if the string can be converted else None
    """
    n = None
    try:
        n = int(float(s))
    except:
        return None
    return n


def int_zero(s):
    """

    @param s: a string
    @return: an int if the string can be converted else None
    """
    n = None
    try:
        n = int(float(s))
    except:
        return 0
    return n


def float_null(s):
    """

    @param s: a string
    @return: a float if the string can be converted else None
    """
    n = None
    try:
        n = float(s)
    except:
        return None
    return n


def float_zero(s):
    """

    @param s: a string
    @return: a float if the string can be converted else 0
    """
    n = 0
    try:
        n = float(s)
    except:
        return 0
    return n


def zero_2_null(n):
    """

    @param n: a number
    @return: if the number return null
    """
    if n == 0:
        return None
    else:
        return n


def in2cm(n):
    """

    @param n: number in inches
    @return: number in centemters
    """
    return n * 2.54


# ## Data Scrubers ####
def scrub_text2int(s):
    """
        Takes a text string and returns an appropriate integer
        Used In:
            Pieces
            Minifigures/Figures
    """
    return only_numerics_int(s)


def scrub_text2float(s):
    """

    @param s: a string
    @return: a float built out of the string, ignoring all non-numeric characters
    """
    return only_numerics_float(s)


def parse_html_table(table_tags):
    """
        Tables in html are in the following format:
            <table> #attributes about the table are in this tag
                <tbody>
                    <tr>    #tr tags indicate a row
                        <td> </td>  #td tags indicate a cell in a row
                        <td> </td>
                    </tr>
                    <tr>
                        <td> </td>
                        <td> </td>
                    </tr>
                </tbody>
            </table>

        This would be a 2x2 table

    @param table_tags: an html table
    @return: a 2d list (table_array)
    """

    if table_tags is None: return None
    table_array = []  # initiate the array
    try:
        table_body = table_tags.find("tbody")  # find the table body
        line_tags = table_body.findAll("tr")  # make a list of all the rows
    except:
        line_tags = table_tags.findAll("tr")

    for k in line_tags:
        table_array.append([x.get_text().strip() for x in
                            k.findAll("td")])  # add a list of cells to the table array - strip out tags and whitespace

    return table_array


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
        set_num = set_list[0]
        set_seq = set_list[1]
    except:
        set_num = set_id
        set_seq = '1'
    return set_num, set_seq, set_num + '-' + set_seq


def check_in_date_range(date, start, end):
    """
    @param date: the date to check
    @param start: the date to start the range
    @param end: the date to end the range
    @rtype : bool
    """
    start = arrow.get(start)
    end = arrow.get(end)
    date = arrow.get(date)

    if date >= start and date <= end:
        return True
    else:
        return False


def check_in_date_rangeA(date, start, end):
    """
    all dates should already be in arrow format
    @param date: the date to check
    @param start: the date to start the range
    @param end: the date to end the range
    @rtype : bool
    """
    if date >= start and date <= end:
        return True
    else:
        return False


def flatten_list(l):
    """
    usefull for lists returned by sqlite
    @param l: a list of lists ie [(a),(b),(c))
    @return: [a,b,c]
    """
    return [i for sublist in l for i in sublist]


def list_to_dict(l):
    """
    usefull for lists returned by sqlite
    @param l: a list of lists ie [(a,b),(c,d),(e,f))
    @return: {a:b,c:d,e:f}
    """
    return {n[0]: n[1] for n in l}


def input_set_num(type=0):
    """
    @param type: 0 or 1
    @return: if type == 1 xxxx, y, xxxx-y
    @return: else return xxxx-y
    """
    set_num = input("What set num? ")
    if type == 1:
        return expand_set_num(set_num)
    else:
        return expand_set_num(set_num)[2]


def list2string(list):
    return ', '.join(map(str, list))


# source http://stackoverflow.com/questions/1165352/fast-comparison-between-two-python-dictionary
class DictDiffer(object):
    """
    Calculate the difference between two dictionaries as:
    (1) items added
    (2) items removed
    (3) keys same in both but changed values
    (4) keys same in both and unchanged values
    """

    def __init__(self, current_dict, past_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.set_current, self.set_past = set(current_dict.keys()), set(past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)

    def added(self):
        return {s: self.current_dict[s] for s in (self.set_current - self.intersect)}

    def removed(self):
        return self.set_past - self.intersect

    def changed(self):
        return {s: (self.current_dict[s], self.past_dict[s]) for s in
                set(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])}

    def unchanged(self):
        return set(o for o in self.intersect if self.past_dict[o] == self.current_dict[o])


def read_csv_in_memory(csv_string, delimiter='\t'):
    """
    takes a csv string and returns a csv object
    @param csv_string:
    @return:
    """
    string_object = StringIO(csv_string)
    return csv.reader(string_object, delimiter=delimiter)


def read_gzip_csv_from_url(url):
    """
    Takes a url like: http://rebrickable.com/files/set_pieces.csv.gz
    and returns just a csv.reader object
    @param url:
    @return:
    """
    gzip_bytes = gzip.decompress(requests.get(url).content)
    return read_csv_in_memory(gzip_bytes.decode("utf-8"), ",")


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


def read_json_from_url(url, params=None):
    return json.loads(requests.get(url, params=params, verify=False).text)


def read_xml_from_url(url, params=None):
    return BeautifulSoup(requests.get(url, params=params, verify=False).text)


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


def note(string):
    with open(notes_file, 'a')  as text_file:
        print(arrow.now('US/Pacific').format('YYYYMMDD HH:mm') + " @ " + string, file=text_file)


note("TEST")