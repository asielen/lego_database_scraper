__author__ = 'andrew.sielen'

# external
from system.logger import logger
# other modules
import database as db
import database.info as info
from system.base_methods import LBEF

# internal
import data
from data.bricklink.bricklink_api import bricklink_api as blapi
import data.update_database as update


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

    set_list = blapi.pull_set_catalog()
    update.add_sets_to_database(set_list, id_col=2)


# Categories
def init_categories():
    """

    @return:
    """
    categories = blapi.pull_categories()
    if categories is None: return False
    # No Need for processing, it is in the right format [id, name]
    db.run_sql('DELETE FROM bl_categories')
    db.batch_update('INSERT INTO bl_categories(bl_category_id, bl_category_name) VALUES (?,?)', categories,
                    header_len=2)


def _fix_part_data_order(pl):
    """
    Takes part data in this format: [bl_category, bricklink_id, design_name, weight, type]
    And returns this format: [bricklink_id, brickowl_id, rebrickable_id, lego_id, design_name, weight, bl_type, bl_category]
    @param part_list:
    @return:
    """
    if len(pl) == 5:
        return [pl[1], None, None, None, pl[2], pl[3], pl[4], pl[0]]
    else:
        LBEF.note("CAN'T CONVERT LIST: [{}]".format(LBEF.list2string(pl)))
        logger.warning("CAN'T CONVERT LIST: [{}]".format(LBEF.list2string(pl)))
        return None


def _prep_list(pl):
    """
    Removes None values and headers
    @param pl:
    @return:
    """
    return pl[3:]


def init_parts():
    """
    from a blank database - update all piece designs by pulling them from a master piece file on bricklink.com
    @return:
    """
    pieces = blapi.pull_part_catalog()
    category_dict = info.read_bl_categories()  # In format [bl_category_id, table_id]
    # Replace the category ID with the table ID for that category
    parts_to_insert = []
    for row in pieces:
        if len(row) > 1:  # some rows are empty, ignore them
            if LBEF.int_null(row[0]) in category_dict:  # check to see if the category exists in the category table
                row[0] = category_dict[int(row[0])]
            else:
                logger.critical("#init_parts({})# - Missing {} from category table".format(row[2], row[0]))
            row[4] = LBEF.float_zero(row[4])
            row.pop(1)  # remove the category name which is redundant with the cat_id
            row.append("P")  # Add the Piece tag

        parts_to_insert.append(_fix_part_data_order(row))

    parts_to_insert = _prep_list(parts_to_insert)

    update.add_part_date_to_database(parts_to_insert,
                                     basics=1)  # needs to be in this format, basics one means it won't overwrite other ids


def init_minifigs():
    """
    from a blank database - update all minifig designs by pulling them from a master piece file on bricklink.com
    @return:
    """
    minifigs = blapi.pull_minifig_catalog()
    category_dict = info.read_bl_categories()  # In format [bl_category_id, table_id]
    # Replace the category ID with the table ID for that catefory
    parts_to_insert = []
    for row in minifigs:
        if len(row) > 1:
            if LBEF.int_null(row[0]) in category_dict:
                row[0] = category_dict[int(row[0])]
            else:
                logger.critical("#init_minifigs({})# - Missing {} from category table".format(row[2], row[0]))
            row[4] = LBEF.float_zero(row[4])
            row.pop(1)  # remove the category name which is redundant with the cat_id
            row.append("M")  # Add the Minifig tag
        parts_to_insert.append(_fix_part_data_order(row))

    parts_to_insert = _prep_list(parts_to_insert)

    update.add_part_date_to_database(parts_to_insert, basics=1)


def init_part_color_codes():
    """
    Pull the color part codes from bricklink and insert them into the database
    @return:
    """
    color_dict = info.read_bl_colors_name()
    part_dict = info.read_bl_parts()
    codes = blapi.pull_part_color_codes()

    # Process codes
    codes_processed = []
    for code in codes:
        if code[1] == 'Color': continue
        if code[0] in part_dict:
            code[0] = part_dict[code[0]]
            code[1] = color_dict[code[1]]
            codes_processed.append(code)
        else:
            logger.error("Could not find part {} in the database".format(code[0]))
            # now in this format [part_id, color_id, color_code]

    db.batch_update(
        'INSERT OR IGNORE INTO part_color_codes(part_id, color_id, element_color_code) VALUES (?,?,?)',
        parts_to_insert, header_len=0)
    logger.debug("Added Color Codes to Database")


def add_bl_set_inventory_to_database(set_num, parts):
    """
    Adds a inventory to the database
    @param set_num: xxxx-xx
    @param parts: ['Type', 'Item No', 'Item Name', 'Qty', 'Color ID', 'Extra?', 'Alternate?', 'Match ID', 'Counterpart?']
        With - 2 - lines for heading
    @return:
    """
    color_dict = info.read_bl_colors()
    set_id = _get_set_id(set_num, add=True)  # True means add if it is missing
    parts_to_insert = []
    for row in parts:
        if len(row):
            row.pop(0)  # remove the type which can be found in the pieces table
            row[0] = _get_bl_piece_id(row[0], add=True)
            row.pop(1)  # remove the item name which can be found in the pieces table
            if LBEF.int_null(row[2]) in color_dict:
                row[2] = color_dict[int(row[2])]
            else:
                logger.critical(
                    "#add_bl_set_inventory_to_database({})# - Missing {} from color table".format(set_num, row[2]))
                row[2] = None
            row.insert(0, set_id)  # Add the set_id to the front
            # Now list is in this format ['set_id', 'piece_id',  'quantity', 'color_id', 'Extra?', 'Alternate?', 'Match ID', 'Counterpart?']
            # Just need to remove the last 4 items
            del row[4:]
        parts_to_insert.append(row)

        # TODO: Update with database call
        # db.batch_update(
        # 'INSERT OR IGNORE INTO parts(set_id, piece_id, quantity, color_id) VALUES (?,?,?,?)', parts_to_insert,
        # header_len=3)


def add_part_to_database(part_num):
    """
    It is much more efficient to add many
    @param part_list:
    @return:
    """
    # These calls shouldn't need to be called every time we add one
    part_database = info.read_bl_parts()  # Used so we don't do double duty and update parts in the system

    if part_num in part_database: return

    bl_categories = info.read_bl_categories()  # To convert the category ids to table ids

    part_row = data.get_piece_info(bl_id=part_num)
    part_row[4] = bl_categories[part_row[4]]  # Adjust the category


    # TODO: Add it to the database...
    return _get_bl_piece_id(part_num)


def _get_set_id(set_num, add=False):
    """
    Wrapper for the get_set_id method in db.info
    @param set_num:
    @param add: if True, Add the set if it is missing in the database
    @return: the id column num of the set in the database
    """
    set_id = info.get_set_id(set_num)
    if set_id is None and add:
        update.add_set_to_database(data.get_basestats(set_num))
        return info.get_set_id(set_num)
    return set_id


def _get_bl_piece_id(part_num, add=False):
    """
    Wrapper for the get_bl_piece_id method in db.info
    @param part_num: the number used by bricklink for pieces
    @return: the primary key for a piece in the database
    """
    piece_id = info.get_bl_piece_id(part_num)
    if piece_id is None and add:
        add_part_to_database(part_num)
        return info.get_bl_piece_id(part_num)
    return piece_id


if __name__ == "__main__":
    def _main():
        print(init_part_color_codes())


    if __name__ == "__main__":
        print("Running as Test")
        _main()


