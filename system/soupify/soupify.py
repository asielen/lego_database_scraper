# External
import gzip
import html
import json
from time import sleep

import requests
import tldextract
from bs4 import BeautifulSoup

# Internal
import system as syt
if __name__ == "__main__": syt.setup_logger()


invalid_urls = 0
requests_made = 0


def get_webpage(url, params=None, verify=False, timeout=10):
    global invalid_urls
    global requests_made
    page = None
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'}
    post = False
    if url.find('.asp'):
        post = True
    try:
        requests_made+=1
        if post:
            page = requests.post(url, data=params, headers=headers)
        else:
            page = requests.get(url, params=params, headers=headers, verify=verify, timeout=timeout)
        syt.add_to_event("SYSTEM: Request Page")
        syt.add_to_event("SYSTEM: Request Site <{}>".format(tldextract.extract(url).domain))
        # syt.add_to_event("SYSTEM ONE PAGE: <{}>".format(url))
        syt.log_note(url)
    except:
        try:
            requests_made+=1
            if post:
                page = requests.post(url, data=params, headers=headers)
            else:
                page = requests.get(url, params=params, headers=headers, verify=verify, timeout=timeout*2)
            syt.add_to_event("SYSTEM: Request Page")
            syt.add_to_event("SYSTEM: Request Site <{}>".format(tldextract.extract(url).domain))
            # syt.add_to_event("SYSTEM ONE PAGE: <{}>".format(url))
            syt.log_note(url)
        except:
            invalid_urls += 1
            syt.log_error("INVALID URL {}: Can't reach the url! {} + {}".format(invalid_urls, url, params))
            syt.add_to_event("SYSTEM: Request Page FAILED")
            syt.add_to_event("SYSTEM: Request Site FAILED <{}>".format(tldextract.extract(url).domain))

            return None
    if page.status_code != 200:
        syt.log_error("Server Error:{} - {}".format(page.status_code, url))
        syt.add_to_event("SYSTEM: Request Page FAILED")
        syt.add_to_event("SYSTEM: Request Site FAILED <{}>".format(tldextract.extract(url).domain))
        return None
    return page


@syt.counter(name="SYSTEM: Soupify")
def soupify(url, params=None, verify=True, bl_check=False):
    """

    @param url: any url
    @return: returns the soup for that url
    """
    html =  get_webpage(url, params, verify)
    if html is None: return None
    soup = BeautifulSoup(html.content, "html.parser")
    if soup is None:
        syt.log_error("Can't make the soup! {}".format(url))
        soup = BeautifulSoup(html, "html.parser")
    if bl_check:
        #Check that bricklink isn't down
        available = soup.find(text="System Unavailable")
        if available is not None:
            bold = soup.find('font',{'face','Tahoma,Arial'}).text[-10:-9]
            print(bold)
            syt.log_info("Bricklink down for maintenance, it will be back in {} minutes.".format(bold))
            syt.log_info("Waiting to continue")
            for n in range(1, syt.int_zero(bold)):
                sleep(60)
                syt.info("{} minutes remaining".format(syt.int_zero(bold) - n))
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
    syt.add_to_event("SYSTEM: Request Page")
    syt.add_to_event("SYSTEM: Request Site <{}>".format(tldextract.extract(url).domain))
    # syt.add_to_event("SYSTEM ONE PAGE: {}".format(url))
    return syt.read_csv_in_memory(gzip_bytes.decode("utf-8"), ",")

def read_csv_from_url_post(url, headers, cookies, data, delimiter='\t'):
    request = requests.post(url=url, headers=headers, cookies=cookies, data=data)
    if request is None: return None
    return syt.read_csv_in_memory(html.unescape(request.text), delimiter)

def read_csv_from_url(url, params=None, delimiter='\t', bl_check=False, post=False):
    """
    Wrapper to make syntax simpler
    also handles errors
    @param url:
    @param params:
    @param delimiter:
    @return:
    """
    page = get_webpage(url, params=params, verify=False)
    if page is None: return None
    return syt.read_csv_in_memory(html.unescape(page.text), delimiter)


def read_json_from_url(url, params=None):
    return json.loads(get_webpage(url, params=params, verify=False).text)


def read_xml_from_url(url, params=None):
    return soupify(url, params=params, verify=False)
