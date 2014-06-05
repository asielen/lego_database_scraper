__author__ = 'andrew.sielen'

# other modules
import database as db
import api.bricklink_api as blapi

#internal
from  api.rebrickable_api import rebrickable_api as reapi


def update_colors():
    color_list_raw = reapi.pull_colors()

    if color_list_raw is None: return False
    color_list = []
    # Process Color list
    # [0'',1rebrickable ID, 2Name, 3rgb hex, 4num parts, 5num sets, 6start year, 7start end, 8lego name, 9ldraw color, 0bricklink color, 11peeron color]
    for row in color_list_raw:
        color_list.append((row[10].strip('{}'), row[1], None, row[2], row[3], None, None))

    db.run_sql('DELETE FROM colors')
    db.batch_update(
        'INSERT INTO colors(bl_color_id, re_color_id, bo_color_id, color_name, hex_value, bl_color_type, bl_category)'
        ' VALUES (?,?,?,?,?,?,?)', color_list, header_len=1)


def update_parts():
    """
    Pull all parts from the database and update them it in the database.
        this doesn't add them directly from the list, it first sees if the part is in the database, if it isn't add it
        from a bricklink scrape
    @return:
    """
    part_list = [x[0] for x in reapi.pull_all_pieces()]  # ['piece_id', 'descr', 'category')
    blapi.add_parts_to_database(part_list)
    # Todo: need to create a scraper for rebrickable piece num information


update_parts()