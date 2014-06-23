__author__ = 'andrew.sielen'

# other modules

from data.update_database.add_parts_database import add_parts_to_database
from data.rebrickable.rebrickable_api import rebrickable_api as reapi
from data.bricklink.bricklink_api.bricklink_update_database import get_bl_piece_id
import data.update_database as update
import database.info as info
import system.base_methods as LBEF


def update_parts():
    """
    Pull all parts from the database and update them it in the database.
        this doesn't add them directly from the list, it first sees if the part is in the database, if it isn't add it
        from a bricklink scrape
    @return:
    """
    part_list = [x[0] for x in reapi.pull_all_pieces()]  # ['piece_id', 'descr', 'category')
    part_list.pop(0)  # Remove the header
    add_parts_to_database(part_list, type="re")
    # Todo: need to create a scraper for rebrickable piece num information


def update_sets(check_update=1):
    """
    Pulls the list of sets from rebrickable and then looks up all their data on bricklink and brickset
    @return:
    """

    set_list = reapi.pull_set_catalog()
    update.add_sets_to_database(set_list, update=check_update)


def update_set_inventories():
    """
    Insert and update all set inventories
    @return:
    """
    parts = info.read_re_parts()
    set_inv = info.read_re_invs()
    colors_dict = info.read_re_colors()
    parts_to_insert = []
    set_inventories = reapi.pull_all_set_parts()
    for row in set_inventories:
        if row[0] == 'set_id': continue
        if row[0] in set_inv:
            continue  # already in the database todo: check last update
        row[0] = get_bl_piece_id(row[0], add=True)
        row[1] = parts[row[1]]
        row[2] = int(row[2])
        row[3] = colors_dict[row[3]]
        del row[-1]
        parts_to_insert.append(row)
    LBEF.print4(parts_to_insert)


if __name__ == "__main__":
    import navigation.menu as menu

    def main_menu():
        """
        Main launch menu
        @return:
        """

        logger.info("RUNNING: Rebrickable API testing")
        options = {}

        options['1'] = "Update Parts", menu_update_parts
        options['2'] = "Update Sets", menu_update_sets
        options['3'] = "Update Set Inventories", menu_update_set_inventories
        options['9'] = "Quit", menu.quit

        while True:
            result = menu.options_menu(options)
            if result is 'kill':
                exit()


    def menu_update_parts():
        update_parts()


    def menu_update_sets():
        update_sets()


    def menu_update_set_inventories():
        update_set_inventories()

    if __name__ == "__main__":
        main_menu()



