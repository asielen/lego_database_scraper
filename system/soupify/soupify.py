
# External
from time import sleep

from bs4 import BeautifulSoup
import requests


# Internal
from system import base
from system import timer
from system import logger
if __name__ == "__main__": logger.setup_logger()


invalid_urls = 0


@timer.counter
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
            logger.log_error("INVALID URL {}: Can't reach the url! {}".format(invalid_urls, url))
            return None
    soup = BeautifulSoup(page)
    if soup is None:
        logger.log_error("Can't make the soup! {}".format(url))
        soup = BeautifulSoup(page)

    # Check that bricklink isn't down
    available = soup.find(text="System Unavailable")
    if available is not None:
        bold = soup.find('b').text[-10:-9]
        logger.log_info("Bricklink down for maintenance, it will be back in {} minutes.".format(bold))
        logger.log_info("Waiting to continue")
        for n in range(1, base.int_zero(bold)):
            sleep(60)
            # logger.info("{} minutes remaining".format(int_zero(bold) - n))
        return soupify(url)
    return soup