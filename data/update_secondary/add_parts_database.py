# External
from time import sleep
import sys
from multiprocessing import Pool as _pool

# Internal
import data
import database as db
from database import info
import system as syt
if __name__ == "__main__": syt.setup_logger()


def add_part_to_database(part_num, type='bl'):
    """

    @param part_num: the part num in standard format 3001
    @param type: optional, bl should work for most
    @return:
    """
    # Todo: Wrap this into the plural version 20141008
    bl_categories = info.read_bl_categories()
    if type == 'bl':
        part_database = info.read_bl_parts()
        if part_num in part_database:
            syt.log_info('{} not added to database, already there'.format(part_num))
            return
        part_data = [_parse_get_bl_pieceinfo(part_num)]
    elif type == 're':
        part_database = info.read_re_parts()
        if part_num in part_database:
            syt.log_info('{} not added to database, already there'.format(part_num))
            return
        part_data = [_parse_get_re_pieceinfo(part_num)]
    else: return
    part_data = _process_categories(part_data, bl_categories)
    add_part_data_to_database(part_data)
    syt.log_info('{} was added to the database'.format(part_num))


    #
    # piece_data[7] = info.get_bl_category_id(piece_data[7])
    # db.run_sql(
    # 'INSERT OR IGNORE INTO parts(bricklink_id, brickowl_id, rebrickable_id, lego_id) VALUES (?,?,?,?)',
    # piece_data[:4])
    # return db.run_sql(
    # 'UPDATE parts SET design_name=?, weight=?, bl_type=?, bl_category=? WHERE bricklink_id=?',
    # (piece_data[4], piece_data[5], piece_data[6], piece_data[7], piece_data[0]))


def add_parts_to_database(part_id_list, type="bl"):
    """
    Adds a parts to the database from a list
    @param part_id_list: list of bl_part numbers to look up and add
    @return:
    """
    syt.log_info("$$$ Adding {} parts to the database from {}".format(len(part_id_list), type))

    part_database = {}

    parts_to_scrape = []
    parts_to_insert = []
    pool = _pool(syt.RUNNINGPOOL)
    bl_categories = info.read_bl_categories()  # To convert the category ids to table ids

    timer = syt.process_timer("Add parts to database")
    total_ids = len(part_id_list)
    if type == "bl":  # TODO need to update this with all the changes to the re side of things
        part_database = info.read_bl_parts()
        for idx, part in enumerate(part_id_list):
            if part in part_database:
                continue
            else:
                parts_to_scrape.append(part)
                # parts_to_insert.extend(_parse_get_bl_pieceinfo(part)) #Todo this is a test just to see where an error is

            # Scrape
            if idx > 0 and idx % (syt.RUNNINGPOOL * 3) == 0:
                parts_to_insert.extend(pool.map(_parse_get_bl_pieceinfo, parts_to_scrape))

                syt.log_info("@@@ Running Pool {}".format(idx))

                timer.log_time(len(parts_to_scrape), total_ids - idx)

                parts_to_scrape = []
                sleep(.5)

            # Insert
            if idx > 0 and len(parts_to_insert) >= 1500:
                syt.log_info("@@@ Inserting {} pieces".format(len(parts_to_insert)))
                parts_to_insert = _process_categories(parts_to_insert, bl_categories)
                add_part_data_to_database(parts_to_insert)
                parts_to_insert = []

        parts_to_insert.extend(pool.map(_parse_get_bl_pieceinfo, parts_to_scrape))
        parts_to_insert = _process_categories(parts_to_insert, bl_categories)
        add_part_data_to_database(parts_to_insert)

    elif type == "re":
        part_database = info.read_re_parts()
        syt.log_debug("Number of Parts in Re Database = {}".format(len(part_database)))
        for idx, part in enumerate(part_id_list):
            if part in part_database:
                continue
            if "-" in part:
                syt.log_note("Set in part list? {}".format(part))
                syt.log_warning("Set in part list? {}".format(part))
                continue
            else:
                parts_to_scrape.append(part)
                # parts_to_insert.extend(_parse_get_re_pieceinfo(part)) #Todo this is a test just to see where an error is
            if idx > 0 and idx % 150 == 0:
                syt.log_info("@@@ Running Pool {}".format(idx))
                parts_to_insert.extend(pool.map(_parse_get_re_pieceinfo, parts_to_scrape))
                timer.log_time(len(parts_to_scrape), total_ids - idx)
                parts_to_scrape = []
                sleep(.5)
            if idx > 0 and idx % 1500 == 0:
                syt.log_info("@@@ Inserting {} pieces".format(len(parts_to_insert)))
                parts_to_insert = _process_categories(parts_to_insert, bl_categories)
                add_part_data_to_database(parts_to_insert)
                parts_to_insert = []
        parts_to_insert.extend(pool.map(_parse_get_re_pieceinfo, parts_to_scrape))
        parts_to_insert = _process_categories(parts_to_insert, bl_categories)
        add_part_data_to_database(parts_to_insert)

    timer.log_time(len(parts_to_scrape), 0)
    timer.end()
    syt.log_info("%%% Finished adding parts to the database from {}".format(type))


def _process_categories(parts_to_insert, bl_categories):
    parts_to_insert_processed = []
    for part_row in parts_to_insert:
        try:
            current_cat = syt.int_null(part_row[7])
            if current_cat in bl_categories:
                part_row[7] = bl_categories[current_cat]
            else:
                part_row[7] = None
                syt.log_note("Missing Category: Category {} could not be found. For _set bl_id={}".format(current_cat,
                                                                                                      part_row[0]))
        except:
            import pprint as pp

            syt.log_warning("### Can't insert part_row {}".format(pp.pformat(part_row)))
        if part_row is not None:
            parts_to_insert_processed.append(part_row)
    return parts_to_insert_processed


def add_part_data_to_database(insert_list, basics=0):
    """
    Way more complicated than it should be because of the multiple IDs
    @param insert_list: A list of part data lists [[bricklink_id, brickowl_id, rebrickable_id, lego_id, design_name, weight, bl_type, bl_category],[...]]
    @param basics: if 1 then only insert part details and not ids
    @return:
    """
    bl_add = []
    re_add = []
    ol_add = []
    lg_add = []

    for row in insert_list:
        if row[0] is not None:
            bl_add.append(row)
        elif row[1] is not None:
            ol_add.append(row)
        elif row[2] is not None:
            re_add.append(row)
        elif row[3] is not None:
            lg_add.append(row)

    syt.log_info("Inserting: {} BL [{}%] ; {} OL [{}%] ; {} RE [{}%] ; {} LG [{}%] Parts ; Total {}".format(
        len(bl_add), round(len(bl_add) / len(insert_list) * 100, 2),
        len(ol_add), round(len(ol_add) / len(insert_list) * 100, 2),
        len(re_add), round(len(re_add) / len(insert_list) * 100, 2),
        len(lg_add), round(len(lg_add) / len(insert_list) * 100, 2),
        len(insert_list)))

    if len(bl_add) > 0:  # If Bricklink Id is _set
        try:
            syt.log_info("adding {} bl_rows".format(len(bl_add)))
            db.batch_update(
                'INSERT OR IGNORE INTO parts(bricklink_id) VALUES (?)', ((p[0],) for p in bl_add))
            if basics == 1:
                db.batch_update(
                    'UPDATE parts SET design_name=?, weight=?, bl_type=?, bl_category=? '
                    'WHERE bricklink_id=?', (tuple(p[4:] + [p[0]]) for p in bl_add))
            else:
                db.batch_update(
                    'UPDATE parts SET brickowl_id=?, rebrickable_id=?, lego_id=?, design_name=?, weight=?, bl_type=?, bl_category=? '
                    'WHERE bricklink_id=?', (tuple(p[1:] + [p[0]]) for p in bl_add))
        except:
            syt.log_note("ERROR: {}".format(sys.exc_info()[0]))
            syt.log_note("Can't insert BL row: {} / {}".format(len(bl_add), syt.list2string(bl_add)))
            for r in bl_add:
                syt.log_note("Can't insert row: {}".format(syt.list2string(r)))

    if len(ol_add) > 0:  # If BrickOwl Id is _set and not bricklink
        try:
            syt.log_info("adding {} bo_rows".format(len(ol_add)))
            db.batch_update(
                'INSERT OR IGNORE INTO parts(bricklink_id, brickowl_id) VALUES (?,?)', (tuple(p[:2]) for p in ol_add))
            db.batch_update(
                'UPDATE parts SET rebrickable_id=?, lego_id=?, design_name=?, weight=?, bl_type=?, bl_category=? '
                'WHERE bricklink_id=? AND brickowl_id=?', (tuple(p[2:] + p[0:2]) for p in ol_add))
        except:
            syt.log_critical("Add BO failed, check notes")
            syt.log_note("ERROR: {}".format(sys.exc_info()[0]))
            syt.log_note("Can't insert BO row: {} / {}".format(len(ol_add), syt.list2string(ol_add)))
            for r in ol_add:
                syt.log_note("Can't insert row: {}".format(syt.list2string(r)))

    if len(re_add) > 0:  # If rebrickable ID is _set and not brickowl or bricklink
        try:
            syt.log_info("adding {} re_rows".format(len(re_add)))
            db.batch_update(
                'INSERT OR IGNORE INTO parts(bricklink_id, brickowl_id, rebrickable_id) VALUES (?,?,?)',
                (tuple(p[:3]) for p in re_add))
            db.batch_update(
                'UPDATE parts SET lego_id=?, design_name=?, weight=?, bl_type=?, bl_category=? '
                'WHERE bricklink_id=? AND brickowl_id=? AND rebrickable_id=?', (tuple(p[3:] + p[0:3]) for p in re_add))
        except:
            syt.log_critical("Add RE failed, check notes")
            syt.log_note("ERROR: {}".format(sys.exc_info()[0]))
            syt.log_note("Can't insert RE row: {} / {}".format(len(re_add), syt.list2string(re_add)))
            for r in re_add:
                syt.log_note("Can't insert row: {}".format(syt.list2string(r)))

    if len(lg_add) > 0:  # only lego ID is _set
        try:
            syt.log_info("adding {} lg_rows".format(len(lg_add)))
            db.batch_update(
                'INSERT OR IGNORE INTO parts(bricklink_id, brickowl_id, rebrickable_id, lego_id) VALUES (?,?,?,?)',
                (tuple(p[:4]) for p in lg_add))
            db.batch_update(
                'UPDATE parts SET design_name=?, weight=?, bl_type=?, bl_category=? '
                'WHERE bricklink_id=? AND brickowl_id=? AND rebrickable_id=? AND lego_id=?',
                (tuple(p[4:] + p[0:4]) for p in lg_add))
        except:
            syt.log_critical("Add LG failed, check notes")
            syt.log_note("ERROR: {}".format(sys.exc_info()[0]))
            syt.log_note("Can't insert LG row: {} / {}".format(len(lg_add), syt.list2string(lg_add)))
            for r in lg_add:
                syt.log_note("Can't insert row: {}".format(syt.list2string(r)))


def _parse_get_bl_pieceinfo(part_num):
    """
    Wrapper for the get_bl_piece_info method to make it work easier with multiprocess
    @param part_num:
    @return:
    """
    syt.log_debug("Getting info on bl part {}".format(part_num))
    return data.get_piece_info(bl_id=part_num)


def _parse_get_re_pieceinfo(part_num):
    """
    Wrapper for the get_bl_piece_info method to make it work easier with multiprocess
    @param part_num:
    @return:
    """
    syt.log_debug("Getting info on re part {}".format(part_num))
    return data.get_piece_info(re_id=part_num)


if __name__ == "__main__":

    def main_menu():
        """
        Main launch menu
        @return:
        """

        options = (
            ("Add Part", menu_add_part_to_database),
        )

        syt.Menu("– Update Database – add parts –", choices=options).run()


    def menu_add_part_to_database():
        part_num = input("What part num? ")
        add_part_to_database(part_num, 're')


    if __name__ == "__main__":
        main_menu()