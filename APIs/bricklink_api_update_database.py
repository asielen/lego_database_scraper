__author__ = 'andrew.sielen'

import apis.bricklink_api as blapi
from database_management import database
import LBEF

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
    from a blank database - update all pieces
    @return:
    """
    pieces = blapi.pull_part_catalog()
    category_dict = read_bl_categories()  # In format [bl_category_id, table_id]
    # Replace the category ID with the table ID for that catefory
    parts_to_insert = []
    for row in pieces:
        if len(row):
            if LBEF.int_null(row[0]) in category_dict:
                # print("Change {} to {}".format(row[0], category_dict[int(row[0])]))
                row[0] = category_dict[int(row[0])]
            #else:
            #   print("Missing {}".format(row[0]))
            row[4] = LBEF.float_zero(row[4])
            row.pop(1)  # remove the category name which is redundant with the cat_id
        parts_to_insert.append(row)
    database.batch_update(
        'INSERT OR IGNORE INTO parts(bl_category, bricklink_id, design_name, weight) VALUES (?,?,?,?)', parts_to_insert,
        header_len=3)


def read_bl_categories():
    return LBEF.list_to_dict(database.run_sql('SELECT bl_category_id, id FROM bl_categories'))


def add_piece(set_num, cvs_file):
    """
    Adds a inventory to the database
    @param cvs_file:
    @return:
    """
    # Format
    # ['Type', 'Item No', 'Item Name', 'Qty', 'Color ID', 'Extra?', 'Alternate?', 'Match ID', 'Counterpart?']


    # Lookup Item Number (look it up in the database)
    # Get Type
    # If item number isn't in the system, add it
    # Lookup Item Color
    # Get other stats (qty, extra, alternate, match ID, counterpart)


def add_set_inventory(set_num, cvs_file):
    """
    Adds a inventory to the database
    @param cvs_file:
    @return:
    """
    # Format
    # ['Type', 'Item No', 'Item Name', 'Qty', 'Color ID', 'Extra?', 'Alternate?', 'Match ID', 'Counterpart?']


    # Lookup Item Number (look it up in the database)
    # Get Type
    # If item number isn't in the system, add it
    # Lookup Item Color
    # Get other stats (qty, extra, alternate, match ID, counterpart)
