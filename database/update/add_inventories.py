# External
import sqlite3 as lite

# Internal
from database import database
import database.info as info
from data.data_classes.SetInfo_HPA_Class import SetInfo
import data.bricklink.bricklink_api as blapi
import system as syt
if __name__ == "__main__": syt.setup_logger()

def add_bl_set_pieces_to_database(set_num, bricklink_pieces):
    """

    @param set_num: standard format xxxx-x
    @param bricklink_pieces: list of pieces [[x, q],[x, q]]
    @return:
    """

    con = lite.connect(database)

    set_id = SetInfo.get_set_id(set_num)

    if set_id is not None:
        add_bl_inventory_to_database(set_id, bricklink_pieces)


def add_bl_inventory_to_database(set_id, set_dict):
    """

    @param set_id: the row id from the sets table
    @param set_dict: the dictionary of the inventory of a _set [element, qty]
    @return:
    """

    if set_dict is None or set_id is None:
        syt.log_warning("Can't add blds inventory to database: set_id = {}".format(set_id))
        return None

    con = lite.connect(database)

    # Remove the previous inventory from the database
    with con:
        c = con.cursor()
        c.execute('DELETE FROM bl_inventories WHERE set_id=?', (set_id,))

    current_design = ""

    for e_set in set_dict:
        current_design = e_set
        current_quantity = set_dict[e_set]

        # Check to see if the design is in the database
        design_id = info.get_bl_piece_ids(current_design)

        # If it isn't in the database yet, add it
        if design_id is None:
            syt.log_debug("Adding blds element to database: design = " + current_design)

            design_id = blapi.add_part_to_database(current_design)

        with con:
            c = con.cursor()
            c.execute('INSERT INTO bl_inventories(set_id, piece_id, quantity) VALUES (?,?,?)',
                      (set_id, design_id, current_quantity))

    with con:  # Update the last date
        c = con.cursor()
        c.execute('UPDATE sets SET last_inv_updated_bl=? WHERE id=?',
                  (syt.get_timestamp(), set_id))