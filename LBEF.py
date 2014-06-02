__author__ = 'andrew.sielen'

import re
import logging

import requests
from bs4 import BeautifulSoup
import arrow


def soupify(url):
    """

    @param url: any url
    @return: returns the soup for that url
    """
    try:
        page = requests.get(url, timeout=10).content
    except:
        try:
            page = requests.get(url, timeout=10).content
        except:
            logging.warning("Can't reach the url! {}".format(url))
            return None
    soup = BeautifulSoup(page)
    if soup is None:
        logging.warning("Can't make the soup! {}".format(url))
        soup = BeautifulSoup(page)
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
    table_array = []  #initiate the array
    try:
        table_body = table_tags.find("tbody")  #find the table body
        line_tags = table_body.findAll("tr")  #make a list of all the rows
    except:
        line_tags = table_tags.findAll("tr")

    for k in line_tags:
        table_array.append([x.get_text().strip() for x in
                            k.findAll("td")])  #add a list of cells to the table array - strip out tags and whitespace

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
    @return: [a,b,c
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


#source http://stackoverflow.com/questions/1165352/fast-comparison-between-two-python-dictionary
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