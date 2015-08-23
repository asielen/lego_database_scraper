
# External
import gzip
import html
import json
from time import sleep

from bs4 import BeautifulSoup
import requests



# Internal
import system as syt
if __name__ == "__main__": syt.setup_logger()


invalid_urls = 0


@syt.timer.counter
def soupify(url, params=None, verify=True):
    """

    @param url: any url
    @return: returns the soup for that url
    """
    global invalid_urls
    try:
        page = requests.get(url, params=params, verify=verify, timeout=10).content
    except:
        try:
            page = requests.get(url, params=params, verify=verify, timeout=20).content
        except:
            invalid_urls += 1
            syt.log_error("INVALID URL {}: Can't reach the url! {} + {}".format(invalid_urls, url, params))
            return None
    soup = BeautifulSoup(page)
    if soup is None:
        syt.log_error("Can't make the soup! {}".format(url))
        soup = BeautifulSoup(page)

    # Check that bricklink isn't down
    available = soup.find(text="System Unavailable")
    if available is not None:
        bold = soup.find('font',{'face','Tahoma,Arial'}).text[-10:-9]
        print(bold)
        syt.log_info("Bricklink down for maintenance, it will be back in {} minutes.".format(bold))
        syt.log_info("Waiting to continue")
        for n in range(1, syt.int_zero(bold)):
            sleep(60)
            # logger.info("{} minutes remaining".format(int_zero(bold) - n))
        return soupify(url)
    return soup


def read_gzip_csv_from_url(url):
    """
    Takes a url like: http://rebrickable.com/files/set_pieces.csv.gz
    and returns just a csv.reader object
    @param url:
    @return:
    """
    gzip_bytes = gzip.decompress(requests.get(url).content)
    return syt.read_csv_in_memory(gzip_bytes.decode("utf-8"), ",")


def read_csv_from_url(url, params=None, delimiter='\t'):
    """
    Wrapper to make syntax simpler
    also handles errors
    @param url:
    @param params:
    @param delimiter:
    @return:
    """
    return syt.read_csv_in_memory(html.unescape(requests.get(url, params=params, verify=False).text), delimiter)


def read_json_from_url(url, params=None):
    return json.loads(requests.get(url, params=params, verify=False).text)


def read_xml_from_url(url, params=None):
    return soupify(url, params=params, verify=False)