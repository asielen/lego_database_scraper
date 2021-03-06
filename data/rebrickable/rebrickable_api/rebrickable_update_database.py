# External
from functools import partial
from multiprocessing import Pool as _pool
from time import sleep

# Internal
from data.rebrickable.rebrickable_api import rebrickable_api as reapi
from data.update_secondary import add_sets_database as secondary_sets
from data.update_secondary import add_parts_database as secondary_parts
import database.info as info
import database as db
from data.data_classes import SetInfo
import system as syt
if __name__ == "__main__": syt.setup_logger()


def update_parts():
    """
    Pull all parts from rebrickable and update them it in the database.
        this doesn't add them directly from the list, it first sees if the part is in the database, if it isn't add it
        from a bricklink scrape
    @return:
    """
    syt.log_info("$$$ Get Rebrickable Part info")
    part_list = [x[0] for x in reapi.pull_all_pieces()]  # ['piece_id', 'descr', 'category')
    part_list.pop(0)  # Remove the header
    secondary_parts.add_parts_to_database(part_list, type="re")
    # Todo: need to create a scraper for rebrickable piece num information
    syt.log_info("%%% Rebrickable Part info added to parts table")


def update_sets(check_update=1):
    """
    Pulls the list of sets from rebrickable and then looks up all their data on bricklink and brickset
    @return:
    """

    set_list = reapi.pull_set_catalog()
    secondary_sets.add_sets_to_database(set_list, update=check_update)


def update_one_set_inventory(set_num):
    """
    Update a single set inventory
    @param set_num:
    @return:
    """
    set_inv = reapi.pull_set_inventory(set_num)


def update_set_inventories(check_update=1):
    """
    Insert and update all set inventories from a master list of pieces - may not be as up to date as the api call
    @return:
    """
    syt.log_info("$$$ Adding RE inventories to database")
    set_inventories = list(reapi.pull_all_set_parts())
    last_updated = info.read_inv_update_date('last_inv_updated_re')
    set_inv = info.read_re_invs()

    sets = info.read_bl_set_num_id()
    parts = info.read_re_parts()
    parts.update(info.read_bl_parts())  # Add bl parts in there just in case
    colors = info.read_re_colors()

    timer = syt.process_timer(name="Add Re Inventories")

    syt.log_info("Running Rebrickable Update")

    sets_to_skip = []
    rows_to_scrape = []
    parts_to_insert = []
    pool = _pool(syt.RUNNINGPOOL)
    for idx, row in enumerate(set_inventories):
        if row[0] == 'set_id': continue
        if row[0] in sets_to_skip: continue
        if row[0] in set_inv:
            if check_update == 0 or not syt.old_data(last_updated[row[0]]):
                sets_to_skip.append(row[0])
                continue
        # print("2222 {} | {} SET {}".format(idx, len(parts_to_insert), row[0]))
        rows_to_scrape.append(row)

        # Get pieces
        if idx > 0 and idx % (syt.RUNNINGPOOL * 10) == 0:
            syt.log_info("@@@ Scraping {} rows".format(len(rows_to_scrape)))
            _process_data = partial(_process_data_for_inv_db, sets=sets, parts=parts, colors=colors)
            parts_to_insert.extend(pool.map(_process_data, rows_to_scrape))
            # print("$[{}]".format(len(rows_to_scrape)))
            rows_to_scrape = []
            sleep(0.01)

        #Insert data
        if idx > 0 and len(parts_to_insert) >= (syt.RUNNINGPOOL * 30):
            parts_to_insert = list(filter(None, parts_to_insert))
            syt.log_info("@@@ Inserting rows >[{}]".format(len(parts_to_insert)))
            _add_re_inventories_to_database(parts_to_insert)
            timer.log_time(300, len(set_inventories) - idx)
            parts_to_insert = []

    _add_re_inventories_to_database(parts_to_insert)
    timer.log_time(len(parts_to_insert))
    timer.end()

    pool.close()
    pool.join()
    syt.log_info("%%% Finished RE inventories to database")


def _process_data_for_inv_db(row=None, sets=None, parts=None, colors=None):
    """
    So pool will work, could also use partial but this is a little more control
    @return:
    """
    # print("Getting data for row {}".format(row[0]))
    row[0] = secondary_sets.get_set_id(row[0], sets=sets, add=True)  # Set Id
    # print("Got ID {}".format(row[0]))
    if row[0] is not None:
        row[1] = get_re_piece_id(row[1], parts=parts, add=False)  # Re_piece Id
        # print("Got Piece {}".format(row[1]))
        row[2] = syt.int_zero(row[2])  # Quantity
        row[3] = info.get_color_id(row[3], colors=colors)  # Color ID
        # print("Got Color {}".format(row[3]))

        del row[-1]
        return row

    else:
        return None


def _add_re_inventories_to_database(invs):
    """
    Adds a inventory to the database
    @param invs: ['Type', 'Item No', 'Item Name', 'Qty', 'Color ID', 'Extra?', 'Alternate?', 'Match ID', 'Counterpart?']
        With - 2 - lines for heading
    @return:
    """

    set_ids_to_delete = set(
        [n[0] for n in filter(None, invs)])  # list of just the _set ids to remove them from the database

    timestamp = syt.get_timestamp()
    for s in set_ids_to_delete:
        db.run_sql("DELETE FROM re_inventories WHERE set_id = ?", (s,))
        db.run_sql("UPDATE sets SET last_inv_updated_re = ? WHERE id = ?", (timestamp, s))
    db.batch_update(
        'INSERT OR IGNORE INTO re_inventories(set_id, piece_id, quantity, color_id) VALUES (?,?,?,?)',
        invs)

    syt.log_debug("Added {} unique pieces to database for {}".format(len(invs), len(set_ids_to_delete)))


def get_re_piece_id(part_num, parts=None, add=False):
    """
    Wrapper for the get_bl_piece_ids method in db.info
    @param part_num: the number used by bricklink for pieces
    @return: the primary key for a piece in the database
    """
    piece_id = None
    if parts is not None:
        try:
            piece_id = parts[part_num]
        except:
            piece_id = None
    if piece_id is None:
        piece_id = info.get_re_piece_id(part_num)
    if piece_id is None and add:
        syt.log_debug('{} part not in db'.format(part_num))
        secondary_parts.add_part_to_database(part_num, type='re')
        return get_re_piece_id(part_num)
    return piece_id


if __name__ == "__main__":

    def main_menu():
        """
        Main launch menu
        @return:
        """

        options = (
            ("Update Parts", menu_update_parts),
            ("Update Sets", menu_update_sets),
            ("Update One _set Inventory", menu_update_one_set_inventory),
            ("Update Set Inventories", menu_update_set_inventories)

        )
        syt.Menu(name="– Debug Rebrickable API testing –", choices=options, quit_tag="Exit").run()

    def menu_update_parts():
        update_parts()


    def menu_update_sets():
        update_sets()

    def menu_update_one_set_inventory():
        set_num = SetInfo.input_set_num()
        update_one_set_inventory(set_num)

    def menu_update_set_inventories():
        update_set_inventories()

    if __name__ == "__main__":
        main_menu()



