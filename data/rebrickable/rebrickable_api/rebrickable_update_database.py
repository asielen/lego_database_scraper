__author__ = 'andrew.sielen'

# other modules

from data.update_database.add_parts_database import add_parts_to_database
from data.rebrickable.rebrickable_api import rebrickable_api as reapi
import data.update_database as update


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


def update_sets():
    """
    Pulls the list of sets from rebrickable and then looks up all their data on bricklink and brickset
    @return:
    """

    set_list = reapi.pull_set_catalog()
    update.add_sets_to_database(set_list)
