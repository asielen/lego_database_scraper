import configparser
import os
from collections import defaultdict

import arrow


config_file = os.path.abspath('/Users/andrew.sielen/PycharmProjects/lego_database_scraper/config.ini')


def read_config(value_list=None):
    """
    @param value_list: Format: [[section,field],[section,field]
    @return:
    """
    config = configparser.ConfigParser()
    config.read(config_file)
    return_dict = defaultdict(defaultdict)  # So I don't have to initialize the keys

    # Get all values in the config file
    if value_list is None:
        sections = config.sections()
        for s in sections:
            for key in config[s]:
                return_dict[s][key] = config[s][key]
    else:
        for v in value_list:
            if v[0] in config:
                # Supplied Key and field
                if len(v) == 2:
                    return_dict[v[0]][v[1]] = config[v[0]][v[1]]
                else:
                    # Just supplied the key
                    for key in config[v[0]]:
                        return_dict[v[0]][key] = config[v[0]][key]
    return return_dict


def set_config(value_list=None):
    """
    @param value_list: Format: [[section, field, value], [section, field, value]]
    @return:
    """
    config = configparser.ConfigParser()
    config.read(config_file)
    for v in value_list:
        if v[0] not in config:
            config.add_section(v[0])
        config[v[0]][v[1]] = str(v[2])

    with open(config_file, 'w') as cfile:
        config.write(cfile)


def read_config_date(section="", field=""):
    return arrow.get(read_config([[section, field]]))


def set_config_date(ts=None, section="", field=""):
    set_config([[section, field, ts]])


def test():
    if __name__ != "__main__": return
    import pprint as pp

    pp.pprint(read_config())
    pp.pprint(read_config([["Database"]]))
    pp.pprint(read_config([["Test"]]))
    pp.pprint(read_config([["Test", "test_value_1"]]))
    set_config([["Test", "test_value_1", 1], ["Test", "test_value_1", "2"], ["Test", "test_value_3", "3"]])
    pp.pprint(read_config([["Test"]]))
    set_config_date(ts=1412971424, section="Dates", field="date_1")
    pp.pprint(read_config([["Dates"]]))


if __name__ == "__main__":
    test()