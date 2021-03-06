__author__ = 'andrew.sielen'

# external
from multiprocessing import Pool as _pool
from time import sleep

# internal
import data
from data.bricklink.bricklink_api import bricklink_api as blapi
from data.data_classes.SetInfo_HPA_Class import SetInfo
from data.update_secondary import add_sets_database as secondary_sets
from data.update_secondary import add_parts_database as secondary_parts
import database as db
import database.info as info
import system as syt
if __name__ == "__main__": syt.setup_logger()


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
    secondary_sets.add_sets_to_database(set_list, id_col=2, update=check_update)


# Categories
def init_categories():
    """
    Pull categories from bricklink and insert them, no need for an update tag because it doesn't delete anything
    Now safe because of the index on the bl_category column
    @return:
    """
    syt.log_info("$$$ Updating categories")
    categories = blapi.pull_categories()
    if categories is None:
        syt.log_critical("!!! Could not pull category data")
        return False
    # No Need for processing, it is in the right format [id, name]
    db.run_sql('INSERT OR IGNORE INTO bl_categories(bl_category_id, bl_category_name) VALUES (?,?)', (0, 'unknown'))
    db.batch_update('INSERT OR IGNORE INTO bl_categories(bl_category_id, bl_category_name) VALUES (?,?)', categories,
                    header_len=2)
    syt.log_info("%%% Categories Updated")


def _fix_part_data_order(pl):
    """
    Takes part data in this format: [bl_category, bricklink_id, design_name, year, weight, type]
    And returns this format: [bricklink_id, brickowl_id, rebrickable_id, lego_id, design_name, weight, bl_type, bl_category]
    @param pl:
    @return:
    """
    if len(pl) == 5 and type(pl[4]) is str:
        return [pl[1], None, None, None, pl[2], pl[3], pl[4], pl[0]]
    elif len(pl) == 6 and type(pl[5]) is str:
        return [pl[1], None, None, None, pl[2], pl[4], pl[5], pl[0]]

    else:
        syt.log_note("CAN'T CONVERT LIST: [{}]".format(syt.list2string(pl)))
        syt.log_warning("### CAN'T CONVERT LIST: [{}]".format(syt.list2string(pl)))
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
    Update safe because of the unique index
    """
    syt.log_info("$$$ Building Parts Table")
    pieces = blapi.pull_part_catalog()
    category_dict = info.read_bl_categories()  # In format [bl_category_id, table_id]
    # Replace the category ID with the table ID for that category
    parts_to_insert = []
    for row in pieces:
        if len(row) > 1:  # some rows are empty, ignore them
            if syt.int_null(row[0]) in category_dict:  # check to see if the category exists in the category table
                row[0] = category_dict[int(row[0])]
            else:
                syt.log_critical("!!! #init_parts({})# - Missing {} from category table".format(row[2], row[0]))
            row[4] = syt.float_zero(row[4])
            row.pop(1)  # remove the category name which is redundant with the cat_id
            row.append("P")  # Add the Piece tag

        parts_to_insert.append(_fix_part_data_order(row))

    parts_to_insert = _prep_list(parts_to_insert)

    secondary_parts.add_part_data_to_database(parts_to_insert,
                                     basics=1)  # needs to be in this format, basics one means it won't overwrite other ids
    syt.log_info("%%% Parts Table Built")


def init_minifigs():
    """
    from a blank database - update all minifig designs by pulling them from a master piece file on bricklink.com
    @return:
    """
    syt.log_info("$$$ Getting Minifigs from BL to parts table")
    minifigs = blapi.pull_minifig_catalog()
    category_dict = info.read_bl_categories()  # In format [bl_category_id, table_id]
    # Replace the category ID with the table ID for that catefory
    parts_to_insert = []
    for row in minifigs:
        if len(row) > 1:
            if syt.int_null(row[0]) in category_dict:
                row[0] = category_dict[int(row[0])]
            else:
                syt.log_critical("!!! #init_minifigs({})# - Missing {} from category table".format(row[2], row[0]))
            row[4] = syt.float_zero(row[4])
            row.pop(1)  # remove the category name which is redundant with the cat_id
            row.append("M")  # Add the Minifig tag
        parts_to_insert.append(_fix_part_data_order(row))

    parts_to_insert = _prep_list(parts_to_insert)

    secondary_parts.add_part_data_to_database(parts_to_insert, basics=1)
    syt.log_info("%%% Minifigs added to Parts table")


def init_part_color_codes():
    """
    Pull the color part codes from bricklink and insert them into the database
    Have to update colors first
    Safe to update if colors are updated first
    @return:
    """
    syt.log_info("$$$ Adding part color codes from BL")
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
            syt.log_error("Could not find part {} in the database".format(code[0]))
            # now in this format [part_id, color_id, color_code]

    db.run_sql('DELETE FROM part_color_codes')
    db.batch_update(
        'INSERT OR IGNORE INTO part_color_codes(part_id, color_id, element_color_code) VALUES (?,?,?)',
        codes_processed)
    syt.log_info("%%% Added {} Color Codes to Database".format(len(codes_processed)))


def update_bl_set_inventories(check_update=0):
    """
    Go through all bricklink sets and get their inventories
    @return:
    """
    syt.log_info("$$$ Adding BL inventories to database")
    sets = info.read_bl_set_id_num()
    last_updated = info.read_inv_update_date('last_inv_updated_bl')
    set_inv = info.read_bl_invs()
    colors_dict = info.read_bl_colors()

    num_sets = len(sets)

    set_invs_to_scrape = []
    set_invs_to_insert = []
    pool = _pool(syt.RUNNINGPOOL)
    timer = syt.process_timer("Upadate Bricklink Inventories")
    for idx, s in enumerate(sets):
        if s in set_inv:
            if check_update == 0 or not syt.old_data(last_updated[s]):
                continue
        set_invs_to_scrape.append((sets[s], s))

        # Scrape Pieces
        if idx > 0 and idx % syt.RUNNINGPOOL == 0:
            temp_list = [y for x in syt.pool_skimmer(pool.map(_get_set_inventory_pool, set_invs_to_scrape)) for y in x]  # flattens the lis
            set_invs_to_insert.extend(temp_list)
            syt.log_info(
                "@@@ Running Pool {} of {} sets ({}% complete)".format(idx, num_sets, round((idx / num_sets) * 100)))
            timer.log_time(len(set_invs_to_scrape), num_sets - idx)
            set_invs_to_scrape = []
            sleep(.5)
        # Insert Pieces
        if idx > 0 and len(set_invs_to_insert) >= 200:
            syt.log_info("@@@ Inserting {} pieces".format(len(set_invs_to_insert)))

            _process_colors(set_invs_to_insert, colors_dict)
            _add_bl_inventories_to_database(set_invs_to_insert)
            set_invs_to_insert = []

    # Final Scrape and insert
    temp_list = [y for x in syt.pool_skimmer(pool.map(_get_set_inventory_pool, set_invs_to_scrape)) for y in x]  # flattens the lis
    set_invs_to_insert.extend(temp_list)
    _process_colors(set_invs_to_insert, colors_dict)
    _add_bl_inventories_to_database(set_invs_to_insert)

    pool.close()
    pool.join()

    timer.log_time(num_sets)
    timer.end()
    syt.log_info("%%% Finished adding BL inventories to database")


def add_bl_set_inventory_to_database(set_num):
    """
    Adds a single set inventory, mostly this is for testing
    @param set_num:
    @return:

    """
    set_id = SetInfo.get_set_id(set_num)
    if set_id is None:
        return None

    set_inv = _get_set_inventory((set_num, set_id))
    _process_colors(set_inv)
    _add_bl_inventories_to_database(set_inv)


def _add_bl_inventories_to_database(invs):
    """
    Adds a inventory to the database
    @param invs: ['Type', 'Item No', 'Item Name', 'Qty', 'Color ID', 'Extra?', 'Alternate?', 'Match ID', 'Counterpart?']
        With - 2 - lines for heading
    @return:
    """
    set_ids_to_delete = set([n[0] for n in invs])  # list of just the set ids to remove them from the database

    timestamp = syt.get_timestamp()
    for s in set_ids_to_delete:
        db.run_sql("DELETE FROM bl_inventories WHERE set_id = ?", (s,))
        db.run_sql("UPDATE sets SET last_inv_updated_bl = ? WHERE id = ?", (timestamp, s))
    db.batch_update(
        'INSERT OR IGNORE INTO bl_inventories(set_id, piece_id, quantity, color_id) VALUES (?,?,?,?)',
        invs)

    syt.log_debug("Added {} unique pieces to database for {}".format(len(invs), len(set_ids_to_delete)))


def _process_colors(invs, colors=None):
    """

    @param invs:
    @param colors:
    @return:
    """
    if colors is None: colors = info.read_bl_colors()
    for inv in invs:
        if syt.int_null(inv[3]) in colors:
            inv[3] = colors[int(inv[3])]
        else:
            syt.log_critical(
                "Missing {} from color table".format(inv[2]))
            inv[2] = None

def _get_set_inventory_pool(set_dat=None):
    return _get_set_inventory(set_dat), syt.get_counts(1)

def _get_set_inventory(set_dat=None):
    """
    returns a list of all the pieces in the correct format
    @param set_dat: [set_num, set_id]
    @return:
    """

    if len(set_dat) != 2:
        syt.log_warning("### Missing Set Num or Set Id {}".format(set_dat))

    set_num = set_dat[0]
    set_id = set_dat[1]

    syt.log_debug("Getting Set Inventory {}".format(set_num))

    parts = blapi.pull_set_inventory(set_num)
    if parts is None:
        syt.log_warning("### Could not find set inventory for {}".format(set_num))
        return []
    parts_to_insert = []
    valid_file = False
    for row in parts:
        if len(row):
            # The first row should start with 'Type'
            #  If it does mark it as valid and continue
            #  Else break as it is not a valid file
            if valid_file is False and row[0] == 'Type':
                valid_file = True
                continue
            # There is a blank row between the header and the content
            if len(row) < 10: continue
            # If it has made  it this far but the file isn't valid, break
            if valid_file is False: break
            if row[0] == 'S':  # All this stupid code takes care of subsets (sets of sets)
                sub_set_id = _get_set_id(row[1], add=True)
                sub_set = _get_set_inventory((row[1], sub_set_id))
                for sr in sub_set:  # change the set id to the set price_capture_menu id
                    sr[0] = set_id
                syt.log_debug('Adding {} parts in subset {}'.format(len(sub_set), row[1]))
                parts_to_insert.extend(sub_set)
                continue
            row.pop(0)  # remove the _type which can be found in the pieces table
            row[0] = get_bl_piece_id(row[0], add=True)
            row.pop(1)  # remove the item name which can be found in the pieces table
            row[1] = int(row[1])  # Make the qty a number not a string

            row.insert(0, set_id)  # Add the set_id to the front
            # Now list is in this format ['set_id', 'piece_id',  'quantity', 'color_num', 'Extra?', 'Alternate?', 'Match ID', 'Counterpart?']
            # Just need to remove the last 4 items
            del row[4:]
            parts_to_insert.append(row)

    if len(parts_to_insert) == 0:
        syt.log_warning("### No inventory found for {}".format(set_num))
    syt.log_debug("Found {} Unique Parts in Set {}".format(len(parts_to_insert), set_num))
    return parts_to_insert


def add_part_to_database(part_num):
    """
    It is much more efficient to add many
    @param part_num:
    @return:
    """
    secondary_parts.add_part_to_database(part_num)

    return get_bl_piece_id(part_num)


def _get_set_id(set_num, add=False):
    """
    Wrapper for the get_set_id method in db.info
    @param set_num:
    @param add: if True, Add the set if it is missing in the database
    @return: the id column num of the set in the database
    """
    set_id = SetInfo.get_set_id(set_num)
    if set_id is None and add:
        secondary_sets.add_set_to_database(data.get_basestats(set_num))
        return SetInfo.get_set_id(set_num)
    return set_id


def get_bl_piece_id(part_num, add=False):
    """
    Wrapper for the get_bl_piece_ids method in db.info
    @param part_num: the number used by bricklink for pieces
    @return: the primary key for a piece in the database
    """
    piece_id = info.get_bl_piece_ids(part_num)
    if piece_id is None and add:
        add_part_to_database(part_num)
        return info.get_bl_piece_ids(part_num)
    return piece_id


if __name__ == "__main__":

    def main_menu():
        """
        Main launch menu
        @return:
        """

        syt.log_info("Bricklink Update Database testing")

        options = (
            ("Update Sets", menu_update_sets),
            ("Init Categories", menu_init_categories),
            ("Init Parts", menu_init_parts),
            ("Init Minifigs", menu_pull_minifig_catalog),
            ("Init Color Codes", menu_init_part_color_codes),
            ("Update all inventories", menu_update_bl_set_inventories),
            ("Update one inventory", menu_add_bl_set_inventory_to_database),
            ("Add part to database", menu_add_part_to_database)
        )

        syt.Menu(choices=options, name="– Bricklink Update Database Testing –", quit_tag="Exit").run()

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
        set_num = si.input_set_num()
        add_bl_set_inventory_to_database(set_num)


    def menu_add_part_to_database():
        part_num = input("What part?")
        add_part_to_database(part_num)


    if __name__ == "__main__":
        main_menu()
