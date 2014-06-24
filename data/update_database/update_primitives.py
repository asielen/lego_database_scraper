__author__ = 'andrew.sielen'

import data
import database as db


def update_colors():
    color_list = data.get_colors()

    if color_list is None: return False

    db.run_sql('DELETE FROM colors')
    db.batch_update(
        'INSERT INTO colors(bl_color_id, re_color_id, bo_color_id, ldraw_color_id, lego_color_id, bl_color_name, lego_color_name, hex_value)'
        ' VALUES (?,?,?,?,?,?,?,?)', color_list)
    db.run_sql(
        'INSERT INTO colors(bl_color_id, re_color_id, bo_color_id, ldraw_color_id, lego_color_id, bl_color_name, lego_color_name, hex_value)'
        ' VALUES (?,?,?,?,?,?,?,?)', (9999, 9999, 9999, 9999, 9999, 'unknown', 'unknown', 'unknown'))