# Internal
import re  # Regular expressions
import csv
import gzip
import html
from io import StringIO
import json
import os

import requests
from bs4 import BeautifulSoup
import arrow



# THIS FILE SHOULD HAVE NO INTERNAL DEPENDENCIES


##
# SYSTEM
##
def runningWindows():
    if os.name == 'nt':
        return True
    return False

def make_project_path(string=""):
    """
     Windows uses \, mac uses /
    @return: the path to the price_capture_menu project folder with an optional string
    """
    path = os.path.dirname(os.path.realpath(__file__)).split("lego_database_scraper")[0]
    if string != "":
        string = string.replace("/", os.sep)  # To fix mac > pc
        string = string.replace("\\", os.sep)  # To fix pc > mac
        return os.path.abspath(path+'lego_database_scraper'+os.sep+string)
    else:
        return os.path.abspath(path+"lego_database_scraper"+os.sep)

def make_dir(path, add_project_path=True):
    """

    @param path: The path to check
    @param add_project_path: If True, add the path to the home path of the project
    @return: return the path to be used
    """
    dir_path, file_name = os.path.split(path) #Just get the directory without the file name
    if add_project_path:
        mod_path = make_project_path(dir_path)
    else:
        mod_path = dir_path
    os.makedirs(mod_path, exist_ok=True)
    return os.path.join(mod_path, file_name)

# #
# Web
# #


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
    # Todo: Pretty sure this isn't used at all
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
    @param params:
    @param delimiter:
    @return:
    """
    return read_csv_in_memory(html.unescape(requests.get(url, params=params, verify=False).text), delimiter)


def csv_replace_comma(text):
    return str(text).replace(',', " /")

def read_json_from_url(url, params=None):
    return json.loads(requests.get(url, params=params, verify=False).text)


def read_xml_from_url(url, params=None):
    return BeautifulSoup(requests.get(url, params=params, verify=False).text)


# #
# Data Methods
# #
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
    dict = {}
    for n in l:
        if len(n) > 2:
            dict[n[0]] = n[1:]
        else:
            dict[n[0]] = n[1]
    return dict


def list2string(list):
    return ', '.join(map(str, list))


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


# #
# Set Methods - Todo: Move to SetInfo Class?
##



# Todo, I think i can trash this because all dates are now stored as timestamps 20141008
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


# #
# Time Methods - Todo: Also maybe put in SetInfo
##
def old_data(date, date_range=90):
    """

    @param date: date in get_timestamp format
    @return: True if it is outside 90 days and needs to be updated, False otherwise
    """
    today = arrow.now()
    past = today.replace(days=-date_range)
    return not (check_in_date_rangeA(arrow.get(date), past, today))


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


def check_if_the_same_day(dateA, dateB):
    """
        Useful for daily stats
    @param dateA: Date in unix format
    @param dateB: Date in unix format
    @return: if A and B are in the same day, return True: else False
    """
    if dateA is None or dateB is None:
        return False
    dateAA = arrow.get(dateA)
    dateBA = arrow.get(dateB)
    if dateAA.date() == dateBA.date():
        return True
    return False


def get_timestamp(date=None, day=False):
    """

    @param date: In the format: YYYY-MM-DD
    @return:
    """
    if date is None:
        dte = arrow.now('US/Pacific')
        if day is True:
            return dte.floor('day').timestamp
        else:
            return dte.timestamp
    return arrow.get(date, 'YYYY-MM-DD')


def get_date(timestamp=None, default=None):
    """

    @param timestamp: If get_timestamp is None, return the current date, else return the get_timestamp date
    @return:
    """
    if timestamp is None:
        if default is None:
            return None
        else:
            return arrow.now('US/Pacific').format('YYYY-MM-DD')
    elif timestamp != "":
        return arrow.get(timestamp).format('YYYY-MM-DD')
    else:
        return None


def get_ts_day(timestamp):
    """
    Strip out the time part of a date
    @param timestamp:
    @return:
    """
    return arrow.get(timestamp).floor('day').timestamp


def get_closest_list(num, num_list):
    assert isinstance(num, int)
    return min(num_list, key=lambda x: abs(x - num))


def get_days_between(dateA, dateB):
    """
    Return the number of days between two dates
    @param dateA:
    @param dateB:
    @return:
    """

    if dateA is None or dateB is None:
        return False
    if check_if_the_same_day(dateA, dateB):
        return 0
    dateAA = arrow.get(dateA)
    dateBA = arrow.get(dateB)
    date_dif = dateAA.date() - dateBA.date()
    return date_dif.days



def input_part_num():
    """
    @return:
    """
    part_num = input("What part num? ")
    return part_num


class DictDiffer(object):
    """
    Calculate the difference between two dictionaries as:
    (1) items added
    (2) items removed
    (3) keys same in both but changed values
    (4) keys same in both and unchanged values

    source http://stackoverflow.com/questions/1165352/fast-comparison-between-two-python-dictionary

    """
    #Todo: I don't think this is used
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


def print4(list, n=4):
    """
    Print the first four items of a list or iterable
    @param list:
    @param n: number to print, defaults to 4
    @return:
    """
    print()
    try:
        for idx, r in enumerate(list):
            print(r)
            if idx >= n: break
    except TypeError:
        print(list)

