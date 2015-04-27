__author__ = 'andrew.sielen'

import database as db
import system as syt
if __name__ == "__main__": syt.setup_logger()

def integrity_check():
    int_check = db.run_sql('PRAGMA integrity_check;', one=True)
    if int_check != 'ok':
        syt.log_error("Database integrity check did not pass, please restore from backup")
    else:
        syt.log_info("    Database OK")


def validate_parts_tables():
    bl_id, bl_id_check = db.run_sql('SELECT COUNT(bricklink_id), COUNT(DISTINCT bricklink_id) FROM parts;', one=True)
    if bl_id != bl_id_check:
        syt.log_error("Bricklink ID is not unique in the parts table [Total: {} |Distinct: {}]".format(bl_id, bl_id_check))
    else:
        syt.log_info("    {} unique Bricklink parts".format(bl_id))
    re_id, re_id_check = db.run_sql('SELECT COUNT(rebrickable_id), COUNT(DISTINCT rebrickable_id)  FROM parts;', one=True)
    if re_id != re_id_check:
        syt.log_error("Rebrickable ID is not unique in the parts table [Total: {} |Distinct: {}]".format(re_id, re_id_check))
    else:
        syt.log_info("    {} unique Rebrickable parts".format(re_id))

def validate_sets_table():
    set_num, set_num_check = db.run_sql('SELECT COUNT(set_num), COUNT(DISTINCT set_num) FROM sets;', one=True)
    if set_num != set_num_check:
        syt.log_error("Count of Set nums is not unique in the sets table [Total: {} |Distinct: {}]".format(set_num, set_num_check))
    else:
        syt.log_info("    {} unique Sets ".format(set_num))

def validate_primitives():
    bl_cat, bl_cat_chk = db.run_sql('SELECT COUNT(bl_category_id), COUNT(DISTINCT bl_category_id) FROM bl_categories;', one=True)
    if bl_cat != bl_cat_chk:
        syt.log_error("Count of categories is not unique in the bl_categories table [Total: {} |Distinct: {}]".format(bl_cat, bl_cat_chk))
    else:
        syt.log_info("    {} unique categories ".format(bl_cat))
    price_type, price_type_chk = db.run_sql('SELECT COUNT(price_type), COUNT(DISTINCT price_type) FROM price_types;', one=True)
    if price_type != price_type_chk:
        syt.log_error("Count of price types is not unique in the price_types table [Total: {} |Distinct: {}]".format(price_type, price_type_chk))
    else:
        syt.log_info("    {} unique price_types ".format(price_type))
    color_id, color_id_check = db.run_sql('SELECT COUNT(bl_color_id), COUNT(DISTINCT bl_color_id) FROM colors;', one=True)
    if color_id != color_id_check:
        syt.log_error("Count of bl color ids is not unique in the colors table [Total: {} |Distinct: {}]".format(color_id, color_id_check))
    else:
        syt.log_info("    {} unique bl color ids ".format(color_id))

def validate_all():
    syt.log_info("Validating database")
    validate_primitives()
    validate_sets_table()
    validate_parts_tables()

def validate_menu():

    options = (
        ("Integrity Check", integrity_check),
        ("Validate All", validate_all),
        ("Validate Parts Tables", validate_parts_tables),
        ("Validate Sets Table", validate_sets_table),
        ("Validate Primatives Tables", validate_primitives)
    )
    syt.Menu(name="- Check Database -", choices=options).run()

if __name__ == "__main__":
    validate_menu()