# External
import sqlite3 as lite

# Internal
import data.bricklink.bricklink_api as blapi
import data.rebrickable.rebrickable_api as reapi
import data.update_primitives as update_p
import database as db
import system as syt
if __name__ == "__main__": syt.setup_logger()

#
# Primitive: {these initiate the database from nothing}
# * init_colors()
# @ Download colors
# * init_parts()
# @ Download parts from Bricklink
# @ Download parts from Rebrickable
# * init_price_types()
# @ Internal, no need to download
# * init_bl_categories()
#         @ Download categories from Bricklink


def init_colors(update=0):
    """
    Download and add colors to the database
    @return:
    """
    update_p.update_colors(update=update)


def init_parts():
    """
    Pull parts from bulk downloads on bricklink and rebrickable
    @return:
    """
    blapi.init_parts()
    blapi.init_minifigs()
    reapi.update_parts()


def init_price_types():
    """
    Create price_types table
    @return:
    """
    syt.log_info("$$$ Updating Price Types")
    price_types = (('current_new',), ('current_used',), ('historic_new',), ('historic_used',))
    con = lite.connect(db.database)

    with con:
        con.execute(
            "DELETE FROM price_types")  #This is okay because there are only 4 and they are always in the same order
        con.executemany("INSERT OR IGNORE INTO price_types(price_type) VALUES (?)", price_types)
    syt.log_info("%%% Price Types Updated")


def init_bl_categories():
    """
    Download and add bl_categories to the database
    @return:
    """
    blapi.init_categories()


def run_primitives():
    init_colors()
    init_price_types()
    init_bl_categories()
    init_parts()


if __name__ == "__main__":

    def main_menu():
        """
        Main launch menu
        @return:
        """
        syt.log_critical("Primitives testing")
        options = (
            ("Initiate Colors", menu_init_colors),
            ("Initiate Parts", menu_init_parts),
            ("Initiate Pricetypes", menu_init_price_types),
            ("Initiate BL Categories", menu_init_bl_categories)
        )

        syt.Menu(name="– Primitives testing –", choices=options, quit_tag="Exit").run()


    def menu_init_colors():
        init_colors()


    def menu_init_parts():
        init_parts()


    def menu_init_price_types():
        init_price_types()

    def menu_init_bl_categories():
        init_bl_categories()

    if __name__ == "__main__":
        main_menu()