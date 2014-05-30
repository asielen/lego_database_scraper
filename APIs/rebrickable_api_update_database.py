__author__ = 'andrew.sielen'

import apis.rebrickable_api as reapi
from database_management import database


def update_colors():
    color_list_raw = reapi.pull_colors()

    if color_list_raw is None: return False
    color_list = []
    # Process Color list
    # [0'',1rebrickable ID, 2Name, 3rgb hex, 4num parts, 5num sets, 6start year, 7start end, 8lego name, 9ldraw color, 0bricklink color, 11peeron color]
    for row in color_list_raw:
        color_list.append((row[10].strip('{}'), row[1], None, row[2], row[3], None, None))

    database.run_sql('DELETE FROM colors')
    database.batch_update(
        'INSERT INTO colors(bl_color_id, re_color_id, bo_color_id, color_name, hex_value, bl_color_type, bl_category)'
        ' VALUES (?,?,?,?,?,?,?)', color_list, header_len=1)


