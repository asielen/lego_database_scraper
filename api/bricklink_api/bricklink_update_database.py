__author__ = 'andrew.sielen'

# external
import logging
from multiprocessing import Pool as _pool

# other modules
import LBEF
import api
import database as db
import database.info as info
import database.update.add_set as update


# internal
from api.bricklink_api import bricklink_api as blapi
from api.bricklink_api import bricklink_piece_info_scrape as blpis


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

    set_dict = _read_bl_sets()

    print("Pulling Sets")
    set_list = blapi.pull_set_catalog()

    print("Pulling Data")
    sets_to_scrape = []
    sets_to_insert = []
    pool = _pool(50)
    for idx, row in enumerate(set_list):
        if len(row) == 0: continue
        if row[2] in set_dict:
            continue
        else:
            sets_to_scrape.append(row)
        if idx > 0 and idx % 150 == 0:
            sets_to_insert.extend(pool.map(_parse_get_basestats, sets_to_scrape))
            print("Completed {}".format(idx))
            print(len(sets_to_insert))
            sets_to_scrape = []
    sets_to_insert.extend(pool.map(_parse_get_basestats, sets_to_scrape))
    print("Completed {}".format(idx))
    print(len(sets_to_insert))

    pool.close()
    pool.join()  # TODO: Test with database insert
    # db.batch_update('INSERT OR IGNORE INTO sets('
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


def _parse_get_basestats(row):
    """
    Wrapper for the get_basestats method to make it work easier with multiprocess
    @param row:
    @return:
    """
    return api.get_basestats(row[2], 1)


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


def init_parts():
    """
    from a blank database - update all piece designs by pulling them from a master piece file on bricklink.com
    @return:
    """
    pieces = blapi.pull_part_catalog()
    category_dict = _read_bl_categories()  # In format [bl_category_id, table_id]
    # Replace the category ID with the table ID for that category
    parts_to_insert = []
    for row in pieces:
        if len(row):  # some rows are empty, ignore them
            if LBEF.int_null(row[0]) in category_dict:  # check to see if the category exists in the category table
                row[0] = category_dict[int(row[0])]
            else:
                logging.critical("#init_parts({})# - Missing {} from category table".format(row[2], row[0]))
            row[4] = LBEF.float_zero(row[4])
            row.pop(1)  # remove the category name which is redundant with the cat_id
            row.append("P")  # Add the Piece tag
        parts_to_insert.append(row)
    db.batch_update(
        'INSERT OR IGNORE INTO parts(bl_category, bricklink_id, design_name, weight, bl_type) VALUES (?,?,?,?,?)',
        parts_to_insert,
        header_len=3)


def init_minifigs():
    """
    from a blank database - update all minifig designs by pulling them from a master piece file on bricklink.com
    @return:
    """
    minifigs = blapi.pull_minifig_catalog()
    category_dict = _read_bl_categories()  # In format [bl_category_id, table_id]
    # Replace the category ID with the table ID for that catefory
    parts_to_insert = []
    for row in minifigs:
        if len(row):
            if LBEF.int_null(row[0]) in category_dict:
                row[0] = category_dict[int(row[0])]
            else:
                logging.critical("#init_minifigs({})# - Missing {} from category table".format(row[2], row[0]))
            row[4] = LBEF.float_zero(row[4])
            row.pop(1)  # remove the category name which is redundant with the cat_id
            row.append("M")  # Add the Minifig tag
        parts_to_insert.append(row)
    db.batch_update(
        'INSERT OR IGNORE INTO parts(bl_category, bricklink_id, design_name, weight, bl_type) VALUES (?,?,?,?,?)',
        parts_to_insert,
        header_len=3)


def _read_bl_categories():
    """

    @return: a list in this format [category_id, id]
    """
    return LBEF.list_to_dict(db.run_sql('SELECT bl_category_id, id FROM bl_categories'))


def _read_bl_colors():
    """

    @return: a list in this format [color_id, id]
    """
    return LBEF.list_to_dict(db.run_sql('SELECT bl_color_id, id FROM colors'))


def _read_bl_sets():
    """

    @return: a list in this format [set_num, id]
    """
    return LBEF.list_to_dict(db.run_sql('SELECT set_num, id FROM sets'))


def _read_bl_parts():
    """

    @return: a dict in this format {part_num: id, }
    """
    return LBEF.list_to_dict(db.run_sql('SELECT bricklink_id, id FROM parts'))


def add_set_inventory_to_database(set_num, parts):
    """
    Adds a inventory to the database
    @param set_num: xxxx-xx
    @param parts: ['Type', 'Item No', 'Item Name', 'Qty', 'Color ID', 'Extra?', 'Alternate?', 'Match ID', 'Counterpart?']
        With - 2 - lines for heading
    @return:
    """
    color_dict = _read_bl_colors()
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
                logging.critical(
                    "#add_set_inventory_to_database({})# - Missing {} from color table".format(set_num, row[2]))
                row[2] = None
            row.insert(0, set_id)  # Add the set_id to the front
            # Now list is in this format ['set_id', 'piece_id',  'quantity', 'color_id', 'Extra?', 'Alternate?', 'Match ID', 'Counterpart?']
            # Just need to remove the last 4 items
            del row[4:]
        parts_to_insert.append(row)

        # TODO: Update with database call
        # db.batch_update(
        # 'INSERT OR IGNORE INTO parts(set_id, piece_id, quantity, color_id) VALUES (?,?,?,?)', parts_to_insert,
        #     header_len=3)


def add_parts_to_database(part_list):
    """
    Adds a parts to the database from a list
    @param part_list: list of bl_part numbers to look up and add
    @return:
    """
    logging.debug("Adding {} parts to the database".format(len(part_list)))

    part_database = _read_bl_parts()  # Used so we don't do double duty and update parts in the system
    bl_categories = _read_bl_categories()  # To convert the category ids to table ids

    parts_to_scrape = []
    parts_to_insert = []
    pool = _pool(10)
    for idx, part in enumerate(part_list):
        if part in part_database:
            continue
        else:
            parts_to_scrape.append(part)
        if idx > 0 and idx % 10 == 0:
            parts_to_insert.extend(pool.map(_parse_get_pieceinfo, parts_to_scrape))
            parts_to_scrape = []
    parts_to_insert.extend(pool.map(_parse_get_pieceinfo, parts_to_scrape))

    for part_row in parts_to_insert:
        part_row[4] = bl_categories[part_row[4]]

    # TODO: DEBUG Statement - need to remove
    for idx, part in enumerate(parts_to_insert):
        print(part)
        if idx >= 10: break

        # TODO: Update with database call
        # db.batch_update(
        # 'INSERT INTO parts(bricklink_id, design_name, weight, bl_type, bl_category)'
        #     ' VALUES (?,?,?,?,?)', parts_to_insert, header_len=0)


def _parse_get_pieceinfo(part_num):
    """
    Wrapper for the get_pieceinfo method to make it work easier with multiprocess
    @param part:
    @return:
    """
    return blpis.get_pieceinfo(part_num, type=1)


def add_set_to_database(set_num):
    update.add_set_to_database_from_dict(api.get_basestats(set_num))


def add_part_to_database(part_num):
    """
    It is much more efficient to add many
    @param part_list:
    @return:
    """
    # These calls shouldn't need to be called every time we add one
    part_database = _read_bl_parts()  # Used so we don't do double duty and update parts in the system

    if part_num in part_database: return

    bl_categories = _read_bl_categories()  # To convert the category ids to table ids

    part_row = blpis.get_pieceinfo(part_num, type=1)
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
        add_set_to_database(set_num)
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


def _main():
    print(_get_bl_piece_id(3004))


if __name__ == "__main__":
    print("Running as Test")
    _main()


