# Internal
import data
import database as db
from database import info
import system as syt
if __name__ == "__main__": syt.setup_logger()


def update_colors(update=False):
    """
    Pull colors from bricklink and rebrickable and add them to the database
    @param update: If true, start from scratch - usually a bad idea, would screw up joins and lookups
    @return:
    """
    syt.log_info("$$$ Updating Colors from BL and RE")
    color_list = data.get_colors()  # [bl_id, re_id, bo_id, ldraw_id, lego_id, bl_name, lego_name, hex]
    if color_list is None:
        syt.log_critical("!!! ERROR: Failed to Pull Colors")
        return False

    if update == True:
        check_update = input(
            "Are you sure you want to update the colors? Y/N Only do this if also refreshing parts - it will ruin color lookups")
        if check_update == 'y' or check_update == 'Y':
            syt.log_warning("### WARNING: Rebuilding Color Table")
            db.run_sql('DELETE FROM colors')
            db.batch_update(
                'INSERT INTO colors(bl_color_id, re_color_id, bo_color_id, ldraw_color_id, lego_color_id, bl_color_name, lego_color_name, hex_value)'
                ' VALUES (?,?,?,?,?,?,?,?)', color_list)
            db.run_sql(
                'INSERT INTO colors(id, bl_color_id, re_color_id, bo_color_id, ldraw_color_id, lego_color_id, bl_color_name, lego_color_name, hex_value)'
                ' VALUES (?,?,?,?,?,?,?,?,?)', (
                9999, 9999, 9999, 9999, 9999, 9999, 'unknown', 'unknown', 'unknown'))  # To be used as the unknown color
    else:
        bl_current_colors = info.read_bl_colors()
        re_current_colors = info.read_re_colors()
        for c in color_list:
            if c[0] in bl_current_colors or c[
                1] in re_current_colors:  # Only update colors that are not already in the database
                syt.log_debug("Color {} Already in db".format(c[5]))  # This keeps us from overwriting the id connections
                continue
            else:
                syt.log_debug("New Color! {} {}".format(c[5], c[0]))
                db.run_sql(
                    'INSERT INTO colors(bl_color_id, re_color_id, bo_color_id, ldraw_color_id, lego_color_id, bl_color_name, lego_color_name, hex_value)'
                    ' VALUES (?,?,?,?,?,?,?,?)', c)
                db.run_sql(
                    'INSERT INTO colors(id, bl_color_id, re_color_id, bo_color_id, ldraw_color_id, lego_color_id, bl_color_name, lego_color_name, hex_value)'
                    ' VALUES (?,?,?,?,?,?,?,?,?)', (9999, 9999, 9999, 9999, 9999, 9999, 'unknown', 'unknown',))
    syt.log_info("%%% Done Updating Colors")