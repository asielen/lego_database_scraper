__author__ = 'andrew.sielen'

import database
import system as syt
if __name__ == "__main__": syt.setup_logger()


"""
Standalone file, to fix various database issues I have come across
"""

def fix_no_unique_key_in_bl_categories():
    """
    A unique key wasn't originally setup for bl_categories
    So, first, comb through the parts table and update all the bl_ids with the proper ones
    2) Rebuild the bl_categories table with the proper index
    3) Rebuild the parts table with the proper foreign key
    @return:
    """
    # Step 1
    # Remove bad ids from parts database by finding the correct ones and sqapping
    print("Distinct Parts: {}".format(database.run_sql('SELECT COUNT(DISTINCT bl_category) FROM parts;', one=True)))
    sql_bl_categories_fix = 'SELECT id, (SELECT MIN(bl.id) FROM bl_categories AS bl  WHERE bl_categories.bl_category_id=bl.bl_category_id GROUP BY bl.bl_category_id) AS new_id FROM bl_categories;'
    bl_categories_fix_lookup = syt.list_to_dict(database.run_sql(sql_bl_categories_fix))

    syt.log_info("Running cleanup loop")
    loop_count = 0
    for bad_value in bl_categories_fix_lookup:
        sql_update = 'UPDATE parts SET bl_category={} WHERE bl_category={};'.format(bl_categories_fix_lookup[bad_value], bad_value)
        database.run_sql(sql_update)
        loop_count += 1
        if loop_count % 642 == 0: #642 is the number of categories
            syt.log_info("Done cleanup loop {}".format(loop_count))
    syt.log_info("Done with cleanup loop")

    print("Distinct Parts: {}".format(database.run_sql('SELECT COUNT(DISTINCT bl_category) FROM parts;', one=True)))
    # Delete the offending lines in the bl_categories table (all ids>642)
    syt.log_info("Deleting duplicate bl_category records")
    sql_delete = 'DELETE FROM bl_categories WHERE id>642;'
    database.run_sql(sql_delete)
    syt.log_info("Done deleting duplicate bl_category records")




if __name__ == "__main__":
    fix_no_unique_key_in_bl_categories()