__author__ = 'andrew.sielen'

import data
import database as db
from database import info
from system.logger import logger


def update_colors(update=False):
    """
    Pull colors from bricklink and rebrickable and add them to the database
    @param update: If true, start from scratch - usually a bad idea, would screw up joins and lookups
    @return:
    """
    color_list = data.get_colors()  # [bl_id, re_id, bo_id, ldraw_id, lego_id, bl_name, lego_name, hex]
    if color_list is None:
        logger.warning("Failed to Pull Colors")
        return False

    if update == True:

        db.run_sql('DELETE FROM colors')
        db.batch_update(
            'INSERT INTO colors(bl_color_id, re_color_id, bo_color_id, ldraw_color_id, lego_color_id, bl_color_name, lego_color_name, hex_value)'
            ' VALUES (?,?,?,?,?,?,?,?)', color_list)
        db.run_sql(
            'INSERT INTO colors(id, bl_color_id, re_color_id, bo_color_id, ldraw_color_id, lego_color_id, bl_color_name, lego_color_name, hex_value)'
            ' VALUES (?,?,?,?,?,?,?,?,?)', (9999, 9999, 9999, 9999, 9999, 9999, 'unknown', 'unknown', 'unknown'))
    else:
        bl_current_colors = info.read_bl_colors()
        re_current_colors = info.read_re_colors()
        for c in color_list:
            if c[0] in bl_current_colors or c[1] in re_current_colors:
                logger.debug("Color {} Already in db", format(c[5]))
                continue
            else:
                logger.debug("New Color! {} {}".format(c[5], c[0]))
                db.run_sql(
                    'INSERT INTO colors(bl_color_id, re_color_id, bo_color_id, ldraw_color_id, lego_color_id, bl_color_name, lego_color_name, hex_value)'
                    ' VALUES (?,?,?,?,?,?,?,?)', c)
