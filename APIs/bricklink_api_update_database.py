__author__ = 'andrew.sielen'

import logging
from multiprocessing import Pool

import apis.bricklink_api as blapi
from database_management import database
from database_management import get_set_info
from database_management import get_piece_info
from get_actions.basics import get_basestats
import LBEF


def update_sets():
    """
    Version: V2 added multiprocess
    Uses the pull_set_catalog() method to download all the sets and add them to the database
    Insert:
        ['Category ID', 'Category Name', 'Number', 'Name', 'Year Released', 'Weight (in Grams)', 'Dimensions']
    into:
        set_num, item_seq, item_seq, set_name, year_released, set_weight, box_size, box_volume
    @return:
    """

    set_dict = read_bl_sets()

    print("Pulling Sets")
    set_list = blapi.pull_set_catalog()

    print("Pulling Data")
    sets_to_scrape = []
    sets_to_insert = []
    pool = Pool(50)
    for idx, row in enumerate(set_list):
        if len(row) == 0: continue
        if row[2] in set_dict:
            continue
        else:
            sets_to_scrape.append(row)
        if idx > 0 and idx % 150 == 0:
            sets_to_insert.extend(pool.map(parse_get_basestats, sets_to_scrape))
            print("Completed {}".format(idx))
            print(len(sets_to_insert))
            sets_to_scrape = []
    sets_to_insert.extend(pool.map(parse_get_basestats, sets_to_scrape))
    print("Completed {}".format(idx))
    print(len(sets_to_insert))

    pool.close()
    pool.join()  # TODO: Test with database insert
    # database.batch_update('INSERT OR IGNORE INTO sets('
    # 'set_name, '
    # 'set_num, '
    #                       'item_num, '
    #                       'item_seq, '
    #                       'theme, '
    #                       'subtheme, '
    #                       'piece_count, '
    #                       'figures, '
    #                       'set_weight, '
    #                       'year_released, '
    #                       'date_released_us, '
    #                       'date_ended_us, '
    #                       'date_released_uk, '
    #                       'date_ended_uk, '
    #                       'original_price_us, '
    #                       'original_price_uk, '
    #                       'age_low, '
    #                       'age_high, '
    #                       'box_size, '
    #                       'box_volume, '
    #                       'last_updated, '
    #                       ') VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', sets_to_insert,
    #                       header_len=0)


def parse_get_basestats(row):
    """
    Wrapper for the get_basestats method to make it work easier with multiprocess
    @param row:
    @return:
    """
    return get_basestats(row[2], 1)


# Categories
def update_categories():
    """

    @return:
    """
    categories = blapi.pull_categories()
    if categories is None: return False
    # No Need for processing, it is in the right format [id, name]
    database.run_sql('DELETE FROM bl_categories')
    database.batch_update('INSERT INTO bl_categories(bl_category_id, bl_category_name) VALUES (?,?)', categories,
                          header_len=2)


def update_pieces():
    """
    from a blank database - update all piece designs by pulling them from a master piece file on bricklink.com
    @return:
    """
    pieces = blapi.pull_part_catalog()
    category_dict = read_bl_categories()  # In format [bl_category_id, table_id]
    # Replace the category ID with the table ID for that category
    parts_to_insert = []
    for row in pieces:
        if len(row):  # some rows are empty, ignore them
            if LBEF.int_null(row[0]) in category_dict:  # check to see if the category exists in the category table
                row[0] = category_dict[int(row[0])]
            else:
                logging.critical("#update_pieces({})# - Missing {} from category table".format(row[2], row[0]))
            row[4] = LBEF.float_zero(row[4])
            row.pop(1)  # remove the category name which is redundant with the cat_id
            row.append("P")  # Add the Piece tag
        parts_to_insert.append(row)
    database.batch_update(
        'INSERT OR IGNORE INTO parts(bl_category, bricklink_id, design_name, weight, bl_type) VALUES (?,?,?,?,?)',
        parts_to_insert,
        header_len=3)


def update_minifigs():
    """
    from a blank database - update all minifig designs by pulling them from a master piece file on bricklink.com
    @return:
    """
    minifigs = blapi.pull_minifig_catalog()
    category_dict = read_bl_categories()  # In format [bl_category_id, table_id]
    # Replace the category ID with the table ID for that catefory
    parts_to_insert = []
    for row in minifigs:
        if len(row):
            if LBEF.int_null(row[0]) in category_dict:
                row[0] = category_dict[int(row[0])]
            else:
                logging.critical("#update_minifigs({})# - Missing {} from category table".format(row[2], row[0]))
            row[4] = LBEF.float_zero(row[4])
            row.pop(1)  # remove the category name which is redundant with the cat_id
            row.append("M")  # Add the Minifig tag
        parts_to_insert.append(row)
    database.batch_update(
        'INSERT OR IGNORE INTO parts(bl_category, bricklink_id, design_name, weight, bl_type) VALUES (?,?,?,?,?)',
        parts_to_insert,
        header_len=3)


def read_bl_categories():
    """

    @return: a list in this format [category_id, id]
    """
    return LBEF.list_to_dict(database.run_sql('SELECT bl_category_id, id FROM bl_categories'))


def read_bl_colors():
    """

    @return: a list in this format [color_id, id]
    """
    return LBEF.list_to_dict(database.run_sql('SELECT bl_color_id, id FROM colors'))


def read_bl_sets():
    """

    @return: a list in this format [set_num, id]
    """
    return LBEF.list_to_dict(database.run_sql('SELECT set_num, id FROM sets'))


def add_set_inventory(set_num, parts):
    """
    Adds a inventory to the database
    @param set_num: xxxx-xx
    @param parts: ['Type', 'Item No', 'Item Name', 'Qty', 'Color ID', 'Extra?', 'Alternate?', 'Match ID', 'Counterpart?']
        With - 2 - lines for heading
    @return:
    """
    color_dict = read_bl_colors()
    set_id = get_set_info.get_set_id(set_num, True)  # True means add if it is missing
    parts_to_insert = []
    for row in parts:
        if len(row):
            row.pop(0)  # remove the type which can be found in the pieces table
            row[0] = get_piece_info.get_bl_piece_id(row[0])
            row.pop(1)  # remove the item name which can be found in the pieces table
            if LBEF.int_null(row[2]) in color_dict:
                row[2] = color_dict[int(row[2])]
            else:
                logging.critical("#add_set_inventory({})# - Missing {} from color table".format(set_num, row[2]))
                row[2] = None
            row.insert(0, set_id)  # Add the set_id to the front
            # Now list is in this format ['set_id', 'piece_id',  'quantity', 'color_id', 'Extra?', 'Alternate?', 'Match ID', 'Counterpart?']
            # Just need to remove the last 4 items
            del row[4:]
        parts_to_insert.append(row)


        # database.batch_update(
        # 'INSERT OR IGNORE INTO parts(set_id, piece_id, quantity, color_id) VALUES (?,?,?,?)', parts_to_insert,
        #     header_len=3)


def add_piece(set_num, cvs_list):
    """
    Adds a single piece to the database
    @param cvs_list:
    @return:
    """


    # Lookup Item Number (look it up in the database)
    # Get Type
    # If item number isn't in the system, add it
    # Lookup Item Color
    # Get other stats (qty, extra, alternate, match ID, counterpart)


def menu_pull_set_inventory():
    set_num = LBEF.input_set_num()
    csvfile = blapi.pull_set_inventory(set_num)
    add_set_inventory(set_num, csvfile)


def main():
    update_sets()


if __name__ == "__main__":
    print("Running as Test")
    main()