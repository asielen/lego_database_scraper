from apis.bricklink_api import bricklink_piece_info_scrape as BLPI

__author__ = 'andrew.sielen'

import sqlite3 as lite

import arrow

from scrapers import brickset_piece_info as BSPI
import LBEF


def add_set2database(set, verbose=0):
    """
        Takes a set with all the appropriate fields and adds it to the database
                INT id
                TXT set_num
                TXT item_num
                TXT item_seq
                TXT set_name
                INT theme_id
                TXT sub_theme
                INT piece_count
                INT unique_piece_count
                INT figures
                FLT set_weight
                FLT piece_weight
                INT year_released
                TXT date_released
                TXT date_ended
                FLT original_price_us
                FLT original_price_uk
                INT age_low
                INT age_high
                TXT box_size
                FLT box_volume
                TXT last_update
    """
    con = lite.connect('lego_sets.sqlite')

    with con:
        c = con.cursor()

        c.execute('INSERT OR IGNORE INTO sets(set_num, set_name) VALUES (?, ?)', (set['set_num'], set['set_name']))
        c.execute('UPDATE sets SET '
                  'item_num=?,'
                  'item_seq=?,'
                  'theme=?,'
                  'subtheme=?,'
                  'piece_count=?,'
                  'figures=?,'
                  'set_weight=?,'
                  'year_released=?,'
                  'date_released_us=?,'
                  'date_ended_us=?,'
                  'date_released_uk=?,'
                  'date_ended_uk=?,'
                  'original_price_us=?,'
                  'original_price_uk=?,'
                  'age_low=?,'
                  'age_high=?,'
                  'box_size=?,'
                  'box_volume=?,'
                  'last_updated=? '
                  'WHERE set_num=? AND set_name=?;',
                  (set['item_num'],
                   set['item_seq'],
                   set['theme'],
                   set['subtheme'],
                   set['piece_count'],
                   set['figures'],
                   set['set_weight'],
                   set['year_released'],
                   set['date_released_us'],
                   set['date_ended_us'],
                   set['date_released_uk'],
                   set['date_ended_uk'],
                   set['original_price_us'],
                   set['original_price_uk'],
                   set['age_low'],
                   set['age_high'],
                   set['box_size'],
                   set['box_volume'],
                   set['last_update'],
                   set['set_num'],
                   set['set_name']))


def add_BSsetPieces2Database(set_num, brickset_pieces, verbose=0):
    """
        set_num is the fill set number: 1234-2
        brickset_pieces is a list of all the pieces in a set
    """
    if verbose == 1:
        print("Adding Pieces to DB: " + str(set_num))
    con = lite.connect('lego_sets.sqlite')
    set_id = None
    with con:
        c = con.cursor()
        set_id = get_set_id(set_num, c)

    if set_id is not None:
        add_BSinv2database(brickset_pieces, set_id)
        if brickset_pieces is None:
            brickset_pieces = ()
        with con:
            c = con.cursor()
            if len(brickset_pieces) == 0:
                c.execute("UPDATE sets SET unique_piece_count_bs=? WHERE id=?", (None, set_id))
            else:
                c.execute("UPDATE sets SET unique_piece_count_bs=? WHERE id=?", (len(brickset_pieces), set_id))


def add_BSinv2database(dic, set_id):
    """
         adds the inventory to the brickset database
    """
    con = lite.connect('lego_sets.sqlite')

    # Need to remove all elements for the set from before REMOVE WHERE?
    with con:
        c = con.cursor()
        c.execute('DELETE FROM bs_inventories WHERE set_id=?', (set_id,))

    current_element = ""

    if dic is not None:
        for i in dic:
            current_element = i[0]
            piece_id = None

            with con:
                # if getting the piece id is successful that means tha the piece
                # exists in both piece tables
                c = con.cursor()
                piece_id = get_element_id(current_element, c)

            if piece_id is None:
                with con:
                    c = con.cursor()
                    piece_dic = BSPI.get_pieceinfo(current_element)
                    if piece_dic is None:
                        raise AssertionError  # if it is in a brickset inventory, it should be on the bs page
                    print("Adding element " + piece_dic['design_num'] + " to the database")

                    design_id = get_design_id(piece_dic['design_num'], c)
                    if design_id is None:
                        add_pieceDesign2Database(piece_dic, c)
                        design_id = get_design_id(piece_dic['design_num'], c)
                        if design_id is None: return None

                    piece_id = add_element2Database(piece_dic, design_id, c)

            if piece_id is None:
                raise AssertionError

            with con:
                c = con.cursor()
                c.execute('INSERT INTO bs_inventories(set_id, piece_id, quantity) VALUES (?,?,?)',
                          (set_id, piece_id, i[1]))

    with con:
        c = con.cursor()
        c.execute('SELECT quantity, weight FROM bs_inventories '
                  'JOIN unique_pieces ON bs_inventories.piece_id = unique_pieces.id '
                  'JOIN piece_designs ON unique_pieces.design_id = piece_designs.id '
                  'WHERE bs_inventories.set_id=?', (set_id,))

        weight_list = c.fetchall()
        calc_weight = sum([x * y for (x, y) in weight_list])
        if calc_weight == 0: calc_weight = None
        c.execute('UPDATE sets SET piece_weight_bs=? WHERE id=?;', (calc_weight, set_id))

        c.execute('UPDATE sets SET last_inv_updated_bs=? WHERE id=?',
                  (arrow.now('US/Pacific').format('YYYY-MM-DD'), set_id))


def add_BLsetPieces2Database(set_num, bricklink_pieces, verbose=0):
    """
        set_num is the fill set number: 1234-2
        bricklink_pieces is a list of all the pieces in a set
    """
    if verbose == 1:
        print("Adding Pieces to DB: " + str(set_num))
    if bricklink_pieces is None:
        return None
    con = lite.connect('lego_sets.sqlite')
    set_id = None
    with con:
        c = con.cursor()
        set_id = get_set_id(set_num, c)

    if set_id is not None:
        add_BLinv2database(bricklink_pieces, set_id)

        with con:
            c = con.cursor()
            if len(bricklink_pieces) == 0:
                c.execute("UPDATE sets SET unique_piece_count_bl=? WHERE id=?", (None, set_id))
            else:
                c.execute("UPDATE sets SET unique_piece_count_bl=? WHERE id=?", (len(bricklink_pieces), set_id))

    pass


def add_BLinv2database(piece_dic, set_id):
    """
         adds the inventory to the brickset database
    """
    con = lite.connect('lego_sets.sqlite')

    # Need to remove all elements for the set from before REMOVE WHERE?
    with con:
        c = con.cursor()
        c.execute('DELETE FROM bl_inventories WHERE set_id=?', (set_id,))

    current_design = ""
    if piece_dic is not None:
        for i in piece_dic:
            current_design = i
            current_quantity = piece_dic[i]
            design_id = None
            with con:
                # if getting the piece id is successful that means tha the piece
                # exists in both piece tables
                c = con.cursor()
                design_id = get_design_id(current_design, c)

            if design_id is None:
                with con:
                    print("Adding element " + current_design + " to the database")

                    piece_info = BLPI.get_pieceinfo(current_design)
                    if piece_info is None:
                        piece_info = BLPI.get_pieceinfo(current_design)
                    if piece_info is None: return None
                    design_id = add_pieceDesign2Database(piece_info, c)

            if design_id is None:
                raise AssertionError

            with con:
                c = con.cursor()
                c.execute('INSERT INTO bl_inventories(set_id, piece_id, quantity) VALUES (?,?,?)',
                          (set_id, design_id, current_quantity))

    with con:
        c = con.cursor()
        c.execute('SELECT quantity, weight FROM bl_inventories '
                  'JOIN piece_designs ON bl_inventories.piece_id = piece_designs.id '
                  'WHERE bl_inventories.set_id=?', (set_id,))

        weight_list = c.fetchall()
        calc_weight = sum([x * y for (x, y) in weight_list])
        if calc_weight == 0: calc_weight = None
        c.execute('UPDATE sets SET piece_weight_bl=? WHERE id=?', (calc_weight, set_id))

        c.execute('UPDATE sets SET last_inv_updated_bl=? WHERE id=?',
                  (arrow.now('US/Pacific').format('YYYY-MM-DD'), set_id))


def add_pieceDesign2Database(piece_dic, cursor):
    """
        adds a new piece to the design table
        needs to be already connected to database
    """

    cursor.execute('INSERT OR IGNORE INTO piece_designs(design_num) VALUES (?)', (piece_dic['design_num'],))
    cursor.execute('UPDATE piece_designs SET '
                   'design_name=?,'
                   'weight=?,'
                   'design_alts=?'
                   ' WHERE design_num=?;',
                   (piece_dic['design_name'],
                    piece_dic['weight'],
                    piece_dic['design_alts'],
                    piece_dic['design_num'],))
    return get_design_id(piece_dic['design_num'], cursor)


def add_element2Database(piece_dic, design_id, cursor):
    """
        Adds and element to the unique parts table, note you need the design id key
    """
    cursor.execute('INSERT OR IGNORE INTO unique_pieces(part_num) VALUES (?)', (piece_dic['part_num'],))
    cursor.execute('UPDATE unique_pieces SET '
                   'design_id=?,'
                   'color_name=?'
                   ' WHERE part_num=?;',
                   (design_id,
                    piece_dic['color_name'],
                    piece_dic['part_num'],))

    return get_element_id(piece_dic['part_num'], cursor)


def _chk_last_updated_today(set_num):
    """
        Checks the last updated date, if it is today, return 1 if it is not return 0
    """
    con = lite.connect('lego_sets.sqlite')
    with con:
        c = con.cursor()
        try:
            c.execute("SELECT last_updated FROM sets WHERE set_num=?", (set_num,))
            last_updated = c.fetchone()[0]
            if last_updated is None:
                return False
            last_updated = arrow.get(last_updated)

            return LBEF.check_in_date_range(last_updated, last_updated.replace(days=-15),
                                            last_updated.replace(days=+15))
        except:
            return False
    return False


def _chk_last_inv_updated_today(set_num):
    """
        Checks the last inventory updated date, if it is today, return 1 if it is not return 0
    """
    con = lite.connect('lego_sets.sqlite')
    with con:
        c = con.cursor()
        try:
            c.execute("SELECT last_inv_updated_bl FROM sets WHERE set_num=?", (set_num,))
            last_updated = c.fetchone()[0]
            if last_updated is None:
                return False
            last_updated = arrow.get(last_updated)

            return LBEF.check_in_date_range(last_updated, last_updated.replace(days=-15),
                                            last_updated.replace(days=+15))
        except:
            return False
    return False


def get_set_id(set_num, cursor):
    """
        Returns the primary key for a set in the database
        Requires a connection to the db to be established already
    """
    set_id = None
    try:
        cursor.execute('SELECT id FROM sets WHERE set_num=?', (set_num,))
        set_id = cursor.fetchone()[0]
    except:
        return None
    return set_id


def get_element_id(part_num, cursor):
    """
        Returns the primary key for a piece in the database
        Requires a connection to the db to be established already
    """
    piece_id = None
    try:
        cursor.execute('SELECT id FROM unique_pieces WHERE part_num=?', (part_num,))
        piece_id = cursor.fetchone()[0]
    except:
        return None
    return piece_id


def get_design_id(design_num, cursor):
    """
        Returns the primary key for a piece in the database
        Requires a connection to the db to be established already
    """
    piece_id = None
    try:
        cursor.execute('SELECT id FROM piece_designs WHERE design_num=?', (design_num,))
        piece_id = cursor.fetchone()[0]
    except:
        return None
    return piece_id