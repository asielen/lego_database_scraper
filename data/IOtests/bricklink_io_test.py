__author__ = 'Andrew'

from data.bricklink import bricklink_api as bapi
import system as sys
if __name__ == "__main__": sys.setup_logger()

def run_test(result, comp, test_name):
    sys.log_info("Running -{}- test".format(test_name))
    pull = list(result)
    if pull[0] != comp:
        sys.log_info("FAILED -{}- test\n".format(test_name))
    else:
        sys.log_info("PASSED -{}- test\n".format(test_name))

def run_bl_tests():
    run_primitives_test()
    run_set_tests()
    run_piece_tests()

#############################
def run_primitives_test():
    test_set_catalog_pull()
    test_part_catalog_pull()
    test_minifigure_catalog_pull()
    test_item_types_pull()
    test_categories_pull()
    test_colors_pull()
    test_part_codes_pull()

def test_set_catalog_pull():
    comp_header = ['Category ID', 'Category Name', 'Number', 'Name', 'Year Released', 'Weight (in Grams)', 'Dimensions']
    test_name = 'Pull catalog of all sets'
    run_test(bapi.pull_set_catalog(), comp_header, test_name)

def test_part_catalog_pull():
    comp_header = ['Category ID', 'Category Name', 'Number', 'Name', 'Weight (in Grams)']
    test_name = 'Pull catalog of all parts'
    run_test(bapi.pull_part_catalog(), comp_header, test_name)


def test_minifigure_catalog_pull():
    comp_header = ['Category ID', 'Category Name', 'Number', 'Name', 'Year Released', 'Weight (in Grams)']
    test_name = 'Pull catalog of all minifigures'
    run_test(bapi.pull_minifig_catalog(), comp_header, test_name)


def test_item_types_pull():
    comp_header = ['Item Type ID', 'Item Type Name']
    test_name = 'Pull item types'
    run_test(bapi.pull_item_types(), comp_header, test_name)

def test_categories_pull():
    comp_header = ['Category ID', 'Category Name']
    test_name = 'Pull categories'
    run_test(bapi.pull_categories(), comp_header, test_name)

def test_colors_pull():
    comp_header = ['Color ID', 'Color Name', 'RGB', 'Type', 'Parts', 'In Sets', 'Wanted', 'For Sale', 'Year From', 'Year To']
    test_name = 'Pull colors'
    run_test(bapi.pull_colors(), comp_header, test_name)


def test_part_codes_pull():
    comp_header = ['Item No', 'Color', 'Code']
    test_name = 'Pull part codes'
    run_test(bapi.pull_part_color_codes(), comp_header, test_name)

##########################

def run_set_tests():
    pass

def test_get_set_info():
    pass

def test_historic_price_info():
    pass

def test_get_set_inventory():
    pass

###########################

def run_piece_tests():
    pass

if __name__ == "__main__":
    run_bl_tests()