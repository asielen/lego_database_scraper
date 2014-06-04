__author__ = 'Andrew'

import logging

import navigation.menu as menu
from apis import api_methods as api
import system_setup as sys


KEY = '12da35f38a061ef52efc56eba9267ed7c9a8f3d4b5c54c396729378788819a0b'
url = 'https://api.brickowl.com/v1/catalog'


def pull_catalog_list(type=None):
    """

    @return:
    """
    parameters = {'key': KEY, 'type': type}
    return api.read_json_from_url(url + '/list', params=parameters)


def pull_catalog_item_info(boid):
    """

    @return:
    """
    parameters = {'key': KEY, 'boid': boid}
    return api.read_json_from_url(url + '/lookup', 5
    params = parameters)


    def pull_search_ID(lookup_id, type='Set', id_type=None):
        """
        type: Set, Part, Minifigure, Gear, Sticker, Packaging
        @return:
        """
        parameters = {'key': KEY, 'id': lookup_id, 'type': type, 'id_type': id_type}
        return api.read_json_from_url(url + '/id_lookup', params=parameters)


    def pull_bulk(csvlist):
        """
        @param csvlist: comma seperated string of BOIDs (max 100)
        @return:
        """
        parameters = {'key': KEY, 'boids': csvlist}
        return api.read_json_from_url(url + '/bulk_lookup', params=parameters)


    def pull_set_inventory(boid):
        """
        @param boid:
        @return:
        """
        parameters = {'key': KEY, 'boid': boid}
        return api.read_json_from_url(url + '/inventory', params=parameters)


    def pull_colors():
        """
        @return:
        """
        parameters = {'key': KEY}
        return api.read_json_from_url(url + '/color_list', params=parameters)


    def pull_data_types():
        """
        @return:
        """
        parameters = {'key': KEY}
        return api.read_json_from_url(url + '/data_type_list', params=parameters)


    def pull_conditions():
        """
        @return:
        """
        parameters = {'key': KEY}
        return api.read_json_from_url(url + '/condition_list', params=parameters)


    def main_menu():
        """
        Main launch menu
        @return:
        """
        sys.setup_logging()
        logging.info("RUNNING: Brickowl API testing")
        options = {}

        options['1'] = "Pull Catalog List", menu_pull_catalog_list
        options['2'] = "Pull Item Info", menu_pull_catalog_item_info
        options['3'] = "Search Item Ids", menu_pull_search_ID
        options['4'] = "Pull Bulk Item list", menu_pull_bulk
        options['5'] = "Pull Set Inventory", menu_pull_set_inventory
        options['6'] = "SYS Pull Colors", menu_pull_colors
        options['7'] = "SYS Pull Data Types", menu_pull_data_types
        options['8'] = "SYS Pull Conditions", menu_pull_conditions
        options['9'] = "Quit", menu.quit

        while True:
            result = menu.options_menu(options)
            if result is 'kill':
                exit()


    def menu_pull_catalog_list():
        jsonfile = pull_catalog_list()
        print(jsonfile)


    def menu_pull_catalog_item_info():
        set_num = input("What set num? ")
        jsonfile = pull_catalog_item_info(set_num)
        print(jsonfile)


    def menu_pull_search_ID():
        item_id = input("What item num? ")
        jsonfile = pull_search_ID(item_id)
        print(jsonfile)


    def menu_pull_bulk():
        str = "10197-1, 3924-1, 12234-1"
        jsonfile = pull_bulk(str)
        print(jsonfile)


    def menu_pull_set_inventory():
        set_num = input("What set num? ")
        jsonfile = pull_set_inventory(set_num)
        print(jsonfile)


    def menu_pull_colors():
        jsonfile = pull_colors()
        print(jsonfile)


    def menu_pull_data_types():
        jsonfile = pull_data_types()
        print(jsonfile)


    def menu_pull_conditions():
        jsonfile = pull_conditions()
        print(jsonfile)


    if __name__ == "__main__":
        main_menu()
