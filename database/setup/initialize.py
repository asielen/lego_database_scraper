# External
import sqlite3 as lite

# Internal
import database as db
import system as syt
if __name__ == "__main__": syt.setup_logger()



def create_database():
    """
    Simply creates the framework of the database
    @return:
    """
    _initiate_database()


def _initiate_database():
    syt.log_info("$$$ Creating Database")
    con = lite.connect(db.database)
    with con:
        # ### Brick Link Info Tables
        con.execute("CREATE TABLE IF NOT EXISTS bl_categories(id INTEGER PRIMARY KEY,"
                    "bl_category_id INTEGER, "
                    "bl_category_name TEXT);")

        con.execute("CREATE TABLE IF NOT EXISTS price_types(id INTEGER PRIMARY KEY,"
                    "price_type TEXT);")
        con.execute("CREATE UNIQUE INDEX IF NOT EXISTS price_type_idx ON price_types(price_type)")



        # ### Build pieces table
        con.execute("CREATE TABLE IF NOT EXISTS parts(id INTEGER PRIMARY KEY, "
                    "bricklink_id TEXT, "
                    "brickowl_id TEXT ,"
                    "rebrickable_id TEXT, "
                    "lego_id TEXT, "  # probably not known for most, or at least it could be the same as the bl_id
                    "design_name TEXT, "
                    "weight REAL, "
                    "bl_category INTEGER,"
                    "bl_type TEXT, "  # P for part, M for minifig - may implement others
                    "FOREIGN KEY (bl_category) REFERENCES bl_categories(id));")
        con.execute("CREATE UNIQUE INDEX IF NOT EXISTS bo_num_idx ON parts(brickowl_id)")
        con.execute("CREATE UNIQUE INDEX IF NOT EXISTS bl_num_idx ON parts(bricklink_id)")
        con.execute("CREATE UNIQUE INDEX IF NOT EXISTS re_num_idx ON parts(rebrickable_id)")


        # For alternate part ids
        con.execute("CREATE TABLE IF NOT EXISTS part_alternates(id INTEGER PRIMARY KEY,"
                    "part_id INTEGER,"
                    "alternate_id TEXT,"
                    "FOREIGN KEY (part_id) REFERENCES parts(id));")
        con.execute("CREATE UNIQUE INDEX IF NOT EXISTS alt_id_idx ON part_alternates(alternate_id)")

        con.execute("CREATE TABLE IF NOT EXISTS colors(id INTEGER PRIMARY KEY,"
                    "bl_color_id INTEGER, "
                    "re_color_id INTEGER, "
                    "bo_color_id INTEGER, "
                    "ldraw_color_id INTEGER, "
                    "lego_color_id INTEGER, "
                    "bl_color_name TEXT, "
                    "lego_color_name TEXT, "
                    "hex_value TEXT);")

        con.execute("CREATE TABLE IF NOT EXISTS part_color_codes(id INTEGER PRIMARY KEY,"
                    "part_id INTEGER, "
                    "color_id INTEGER, "
                    "element_color_code TEXT,"
                    "FOREIGN KEY (part_id) REFERENCES parts(id),"
                    "FOREIGN KEY (color_id) REFERENCES colors(id));")
        con.execute("CREATE UNIQUE INDEX IF NOT EXISTS part_num_idx ON part_color_codes(element_color_code)")



        # ### Build sets table
        con.execute("CREATE TABLE IF NOT EXISTS sets(id INTEGER PRIMARY KEY,"
                    "set_num TEXT,"
                    "bo_set_num TEXT,"
                    "item_num TEXT,"
                    "item_seq TEXT,"
                    "set_name TEXT,"
                    "theme TEXT,"
                    "subtheme TEXT,"
                    "piece_count INTEGER,"
                    "figures INTEGER,"
                    "set_weight REAL,"
                    "year_released INTEGER,"
                    "date_released_us INTEGER,"
                    "date_ended_us INTEGER,"
                    "date_released_uk INTEGER,"
                    "date_ended_uk INTEGER,"
                    "original_price_us REAL,"
                    "original_price_uk REAL,"
                    "age_low INTEGER,"
                    "age_high INTEGER,"
                    "box_size TEXT,"
                    "box_volume REAL,"
                    "last_updated INTEGER,"
                    "last_inv_updated_bo INTEGER,"
                    "last_inv_updated_bl INTEGER,"
                    "last_inv_updated_re INTEGER,"
                    "last_price_updated INTEGER);")
        con.execute("CREATE UNIQUE INDEX IF NOT EXISTS set_num_idx ON sets(set_num)")
        con.execute("CREATE INDEX IF NOT EXISTS set_name_idx ON sets(set_name)")



        # ### Build inventories table
        con.execute("CREATE TABLE IF NOT EXISTS re_inventories(id INTEGER PRIMARY KEY,"
                    "set_id INTEGER,"
                    "piece_id INTEGER,"
                    "color_id INTEGER,"
                    "quantity INTEGER,"
                    "FOREIGN KEY (set_id) REFERENCES sets(id), "
                    "FOREIGN KEY (piece_id) REFERENCES parts(id), "
                    "FOREIGN KEY (color_id) REFERENCES colors(id));")

        con.execute("CREATE TABLE IF NOT EXISTS bl_inventories(id INTEGER PRIMARY KEY,"
                    "set_id INTEGER,"
                    "piece_id INTEGER,"
                    "color_id INTEGER,"
                    "quantity INTEGER,"
                    "FOREIGN KEY (set_id) REFERENCES sets(id),"
                    "FOREIGN KEY (piece_id) REFERENCES parts(id), "
                    "FOREIGN KEY (color_id) REFERENCES colors(id));")

        con.execute("CREATE TABLE IF NOT EXISTS bo_inventories(id INTEGER PRIMARY KEY,"
                    "set_id INTEGER,"
                    "piece_id INTEGER,"
                    "color_id INTEGER,"
                    "quantity INTEGER,"
                    "FOREIGN KEY (set_id) REFERENCES sets(id),"
                    "FOREIGN KEY (piece_id) REFERENCES parts(id), "
                    "FOREIGN KEY (color_id) REFERENCES colors(id));")



        # Build historic_prices table
        con.execute("CREATE TABLE IF NOT EXISTS historic_prices(id INTEGER PRIMARY KEY,"
                    "set_id INTEGER,"
                    "record_date INTEGER,"
                    "price_type INTEGER,"  # 1,2,3,4 current_new, current_used, historic_new, historic_used
                    "avg REAL,"
                    "lots REAL,"
                    "max REAL,"
                    "min REAL,"
                    "qty REAL,"
                    "qty_avg REAL,"
                    "piece_avg REAL,"
                    "FOREIGN KEY (set_id) REFERENCES sets(id),"
                    "FOREIGN KEY (price_type) REFERENCES price_types(id));")
        con.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS price_type_date_idx ON historic_prices(set_id, price_type, record_date)")

        con.execute("CREATE TABLE IF NOT EXISTS bs_ratings(id INTEGER PRIMARY KEY,"
                    "set_id INTEGER,"
                    "want INTEGER,"
                    "own INTEGER,"
                    "rating INTEGER,"
                    "record_date INTEGER,"
                    "FOREIGN KEY (set_id) REFERENCES sets(id));")
        con.execute("CREATE UNIQUE INDEX IF NOT EXISTS rating_type_date_idx ON bs_ratings(set_id, record_date)")
        syt.log_info("%%% Database Created")