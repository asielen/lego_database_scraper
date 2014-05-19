__author__ = 'Andrew'

import requests

KEY = '12da35f38a061ef52efc56eba9267ed7c9a8f3d4b5c54c396729378788819a0b'




print(r.text)

def get_conditions_list():
    """

    @return:
    """
    payload = {'key': KEY}
    r = requests.get('https://api.brickowl.com/v1/catalog/condition_list', params=payload, verify=False)

def get_data_type_list():
    """

    @return:
    """
    payload = {'key': KEY}
    r = requests.get('https://api.brickowl.com/v1/catalog/data_type_list', params=payload, verify=False)

def get_color_list():
    """

    @return:
    """
    payload = {'key': KEY}
    r = requests.get('https://api.brickowl.com/v1/catalog/color_list', params=payload, verify=False)


def get_set_inventory(boid):
    """

    @param boid:
    @return:
    """
    payload = {'key': KEY, 'boid': str(boid)}
    r = requests.get('https://api.brickowl.com/v1/catalog/inventory', params=payload, verify=False)


def search_brickowl(query):
    """
    query - Your search term. To browse use the term 'All'.
    page (Optional) - Page number, usually 1 - 50
    missing_data (Optional) - Missing data filter. You can get the possible values from this query http://www.brickowl.com/search/catalog?query=All&show_missing=1 on the left
    @return:
    """
    payload = {'key': KEY, 'boid': str(boid)}
    r = requests.get('https://api.brickowl.com/v1/catalog/search', params=payload, verify=False)

def lookup_boids(boids):
    """
    boids - A comma separated list of boids. Maximum amount: 100
    @param boids:
    @return:
    """
    payload = {'key': KEY, 'boid': str(boid)}
    r = requests.get('https://api.brickowl.com/v1/catalog/bulk_lookup', params=payload, verify=False)


def lookup_boid(boid):
    """
    boid - BOID
    @param boid:
    @return:
    """
    payload = {'key': KEY, 'boid': str(boid)}
    r = requests.get('https://api.brickowl.com/v1/catalog/lookup', params=payload, verify=False)

def lookup_boid_id(set_num):
    """
    id - ID
    type - Filter by item type. Set, Part, Minifigure, Gear, Sticker, Packaging
    id_type (Optional) - Filter by ID type.
    @param set_num:
    @return:
    """
    payload = {'key': KEY, 'id': str(set_num), 'type': }
    r = requests.get('https://api.brickowl.com/v1/catalog/id_lookup', params=payload, verify=False)

def get_catalog_list():
    """
    type (Optional) - Filter by item type. Set, Part, Minifigure, Gear, Sticker, Packaging
    brand (Optional) - Filter by brand
    @return:
    """
    payload = {'key': KEY}
    r = requests.get('https://api.brickowl.com/v1/catalog/list', params=payload, verify=False)