
# Internal
import data.bricklink.bricklink_api as blapi
import data.rebrickable.rebrickable_api as reapi
import data.update_primitives as update_p
import database as db
import system as syt
if __name__ == "__main__": syt.setup_logger()

#
# Primitive: {these initiate the database from nothing}
# * init_colors()  SAFE
# @ Download colors
# * init_parts()  SAFE
# @ Download parts from Bricklink
# @ Download parts from Rebrickable
# * init_price_types() SAFE
# @ Internal, no need to download
# * init_bl_categories() SAFE
# @ Download categories from Bricklink


def init_colors(update=False):
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

    db.run_batch_sql("INSERT OR IGNORE INTO price_types(price_type) VALUES (?)", price_types)
    syt.log_info("%%% Price Types Updated")

def init_theme_categories():
    """
    Update  theme_categories
        –  NEEDS to have a 'theme_categories.csv' file in  the  system_files  folder
    @return:
    """
    syt.log_info("$$$ Initializing Theme Categories")
    theme_categories = (('Action Figures',), ('Educational',), ('Large Bricks',), ('Licensed',), ('Miscellaneous',), ('Standard',), ('Technic',))
    db.run_batch_sql("INSERT OR IGNORE INTO theme_categories(theme_category) VALUES (?)", theme_categories)
    syt.log_info("$$$ Theme Categories Initialized")

    syt.log_info("$$$ Mapping Theme Categories")
    theme_category_map = syt.list_to_dict(db.run_sql('SELECT theme_category, id FROM theme_categories'))
    theme_category_map_file = syt.make_project_path("/system_files/theme_categories.csv")
    print(theme_category_map_file)
    theme_to_category_list = []
    with open(theme_category_map_file) as csvfile:
        for row in csvfile:
            row_list = row.strip().split(",")
            if row_list[0] == 'Theme':
                continue
            else:
                theme_to_category_list.append((row_list[0], theme_category_map[row_list[1]]))
    db.run_batch_sql("INSERT OR IGNORE INTO themes('theme', 'theme_category_id') VALUES (?,?)", theme_to_category_list)
    syt.log_info("$$$ Done Mapping Theme Categories")


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
    init_theme_categories()
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
            ("Initiate BL Categories", menu_init_bl_categories),
            ("Initiate Theme Categories", menu_init_theme_categories)
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

    def menu_init_theme_categories():
        init_theme_categories()

    if __name__ == "__main__":
        main_menu()