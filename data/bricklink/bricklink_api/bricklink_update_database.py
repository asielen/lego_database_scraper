__author__ = 'andrew.sielen'

# external
from system.logger import logger
# other modules
import database as db
import database.info as info
import system.base_methods as LBEF

# internal
import data
from data.bricklink.bricklink_api import bricklink_api as blapi
import data.update_database as update


def update_sets(check_update=1):
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
    update.add_sets_to_database(set_list, id_col=2, update=check_update)


# Categories
def init_categories():
    """

    @return:
    """
    categories = blapi.pull_categories()
    if categories is None: return False
    # No Need for processing, it is in the right format [id, name]
    # db.run_sql('DELETE FROM bl_categories')
    db.run_sql('INSERT OR IGNORE INTO bl_categories(bl_category_id, bl_category_name) VALUES (?,?)', (0, 'unknown'))
    db.batch_update('INSERT OR IGNORE INTO bl_categories(bl_category_id, bl_category_name) VALUES (?,?)', categories,
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

    update.add_part_data_to_database(parts_to_insert,
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

    update.add_part_data_to_database(parts_to_insert, basics=1)


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

    db.run_sql('DELETE FROM part_color_codes')
    db.batch_update(
        'INSERT OR IGNORE INTO part_color_codes(part_id, color_id, element_color_code) VALUES (?,?,?)',
        codes_processed)
    logger.debug("Added {} Color Codes to Database".format(len(codes_processed)))


def update_bl_set_inventories(check_update=0):
    """
    Go through all bricklink sets and get their inventories
    @return:
    """
    sets = info.read_bl_set_ids()
    set_inv = info.read_bl_invs()
    colors_dict = info.read_bl_colors()
    num_sets = len(sets)
    completed_sets = 0
    timer = LBEF.process_timer()
    for idx, s in enumerate(sets):
        if s in set_inv and check_update == 0:
            continue
        add_bl_set_inventory_to_database(sets[s], colors=colors_dict)
        if idx > 0 and idx % 10 == 0:
            logger.info(
                "## Processed {} of {} sets ({}% complete)".format(idx, num_sets, round((idx / num_sets) * 100)))
        completed_sets += 1
        if idx > 0 and completed_sets % 50 == 0:
            timer.log_time(completed_sets, num_sets - idx)
            completed_sets = 0
    timer.log_time(num_sets)


def add_bl_set_inventory_to_database(set_num, colors=None):
    """
    Adds a inventory to the database
    @param set_num: xxxx-xx
    @param parts: ['Type', 'Item No', 'Item Name', 'Qty', 'Color ID', 'Extra?', 'Alternate?', 'Match ID', 'Counterpart?']
        With - 2 - lines for heading
    @return:
    """
    if set_num is None:
        return
    if colors is None:
        colors = info.read_bl_colors()
    set_id = _get_set_id(set_num, add=True)  # True means add if it is missing
    if set_id is None:
        logger.warning("Could not find set id for {}".format(set_num))
        return

    parts_to_insert = _get_set_inventory(set_num, set_id, colors)
    # todo if adding gear or books, need to fix the weight, the year is being placed in the weight (use minifig method?)
    if parts_to_insert is not None:
        db.run_sql("DELETE FROM bl_inventories WHERE set_id = ?", (set_id,))
        db.batch_update(
            'INSERT OR IGNORE INTO bl_inventories(set_id, piece_id, quantity, color_id) VALUES (?,?,?,?)',
            parts_to_insert)
    logger.debug("Added {} unique pieces to database for set {}/{}".format(len(parts_to_insert), set_num, set_id))


def _get_set_inventory(set_num, set_id, colors=None):
    """
    returns a list of all the pieces in the correct format
    @param set_num:
    @param colors:
    @return:
    """
    logger.info("Getting Set Inventory {}".format(set_num))

    if colors is None:
        colors = info.read_bl_colors()
    parts = blapi.pull_set_inventory(set_num)
    if parts is None:
        logger.warning("Could not find set inventory for {}".format(set_num))
        return []
    parts_to_insert = []
    for row in parts:
        if len(row):
            if len(row) < 10: continue
            if row[0] == 'Type': continue
            if row[0] == 'S':  # All this stupid code takes care of subsets (sets of sets)
                sub_set_id = _get_set_id(row[1], add=True)
                sub_set = _get_set_inventory(row[1], sub_set_id, colors)
                for sr in sub_set:  # change the set id to the set main id
                    sr[0] = set_id
                logger.info('Adding {} parts in subset {}'.format(len(sub_set), row[1]))
                parts_to_insert.extend(sub_set)
                continue
            row.pop(0)  # remove the type which can be found in the pieces table
            row[0] = get_bl_piece_id(row[0], add=True)
            row.pop(1)  # remove the item name which can be found in the pieces table
            row[1] = int(row[1])  # Make the qty a number not a string
            if LBEF.int_null(row[2]) in colors:
                row[2] = colors[int(row[2])]
            else:
                logger.critical(
                    "#add_bl_set_inventory_to_database({})# - Missing {} from color table".format(set_num, row[2]))
                row[2] = None
            row.insert(0, set_id)  # Add the set_id to the front
            # Now list is in this format ['set_id', 'piece_id',  'quantity', 'color_id', 'Extra?', 'Alternate?', 'Match ID', 'Counterpart?']
            # Just need to remove the last 4 items
            del row[4:]
            parts_to_insert.append(row)

    if len(parts_to_insert) == 0:
        logger.warning("No inventory found for {}".format(set_num))
    logger.info("{} Unique Parts in Set {}".format(len(parts_to_insert), set_num))
    return parts_to_insert


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
    part_row[7] = bl_categories[LBEF.int_zero(part_row[7])]  # Adjust the category

    update.add_part_to_database(part_row)

    logger.debug("Adding {} to part db (Values: {})".format(part_num, LBEF.list2string(part_row)))

    return get_bl_piece_id(part_num)


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


def get_bl_piece_id(part_num, add=False):
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
    from navigation import menu

    def main_menu():
        """
        Main launch menu
        @return:
        """

        logger.info("Bricklink Update Database testing")
        options = {}

        options['1'] = "Update Sets", menu_update_sets
        options['2'] = "Init Categories", menu_init_categories
        options['3'] = "Init Parts", menu_init_parts
        options['4'] = "Init Minifigs", menu_pull_minifig_catalog
        options['5'] = "Init Color Codes", menu_init_part_color_codes
        options['6'] = "Update all inventories", menu_update_bl_set_inventories
        options['7'] = "Update one inventory", menu_add_bl_set_inventory_to_database
        options['8'] = "Add part to database", menu_add_part_to_database
        options['9'] = "Quit", menu.quit

        while True:
            result = menu.options_menu(options)
            if result is 'kill':
                exit()


    def menu_update_sets():
        update_sets()


    def menu_init_categories():
        init_categories()


    def menu_init_parts():
        init_parts()

    def menu_pull_minifig_catalog():
        init_minifigs()

    def menu_init_part_color_codes():
        init_part_color_codes()


    def menu_update_bl_set_inventories():
        update_bl_set_inventories()


    def menu_add_bl_set_inventory_to_database():
        set_num = LBEF.input_set_num()
        add_bl_set_inventory_to_database(set_num)


    def menu_add_part_to_database():
        part_num = input("What part?")
        add_part_to_database(part_num)


    if __name__ == "__main__":
        main_menu()
