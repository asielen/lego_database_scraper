import configparser

config_file = os.path.abspath('/Users/andrew.sielen/PycharmProjects/lego_database_scraper/config.ini')


def read_config():
    config = configparser.ConfigParser()
    config.sections()
    config.read(config_file)
    