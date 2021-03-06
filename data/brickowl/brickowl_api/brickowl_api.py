# Internal
import system as syt
import system.soupify.soupify

if __name__ == "__main__": syt.setup_logger()

KEY = '12da35f38a061ef52efc56eba9267ed7c9a8f3d4b5c54c396729378788819a0b'
url = 'https://public_api.brickowl.com/v1/catalog'


def pull_catalog_list(type=None):
    """

    @return:
    """
    parameters = {'key': KEY, '_type': type}
    return system.soupify.soupify.read_json_from_url(url + '/list', params=parameters)


def pull_catalog_item_info(boid):
    """

    @return:
    """
    parameters = {'key': KEY, 'boid': boid}
    return system.soupify.soupify.read_json_from_url(url + '/lookup', params=parameters)


def pull_search_ID(lookup_id, type='Part', id_type=None):
    """
    _type: Set, Part, Minifigure, Gear, Sticker, Packaging
    @return:
    """
    parameters = {'key': KEY, 'id': lookup_id, '_type': type, 'id_type': id_type}
    return system.soupify.soupify.read_json_from_url(url + '/id_lookup', params=parameters)


def pull_bulk(csvlist):
    """
    @param csvlist: comma seperated string of BOIDs (max 100)
    @return:
    """
    parameters = {'key': KEY, 'boids': csvlist}
    return system.soupify.soupify.read_json_from_url(url + '/bulk_lookup', params=parameters)


def pull_set_inventory(boid):
    """
    @param boid:
    @return:
    """
    parameters = {'key': KEY, 'boid': boid}
    return system.soupify.soupify.read_json_from_url(url + '/inventory', params=parameters)


def pull_colors():
    """
    @return:
    """
    parameters = {'key': KEY}
    return system.soupify.soupify.read_json_from_url(url + '/color_list', params=parameters)


def pull_data_types():
    """
    @return:
    """
    parameters = {'key': KEY}
    return system.soupify.soupify.read_json_from_url(url + '/data_type_list', params=parameters)


def pull_conditions():
    """
    @return:
    """
    parameters = {'key': KEY}
    return system.soupify.soupify.read_json_from_url(url + '/condition_list', params=parameters)


def main_menu():
    """
    Main launch menu
    @return:
    """
    options = (
        ("Pull Catalog List", menu_pull_catalog_list),
        ("Pull Item Info", menu_pull_catalog_item_info),
        ("Search Item Ids", menu_pull_search_ID),
        ("Pull Bulk Item list", menu_pull_bulk),
        ("Pull Set Inventory", menu_pull_set_inventory),
        ("SYS Pull Colors", menu_pull_colors),
        ("SYS Pull Data Types", menu_pull_data_types),
        ("SYS Pull Conditions", menu_pull_conditions)
    )
    syt.Menu(name="– Brickowl API testing –", choices=options).run()

def menu_pull_catalog_list():
    jsonfile = pull_catalog_list()
    print(jsonfile)


def menu_pull_catalog_item_info():
    set_num = input("What _set num? ")
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
    set_num = input("What _set num? ")
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
