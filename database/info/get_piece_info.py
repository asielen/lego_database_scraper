# Internal
import database as db
import system as syt
if __name__ == "__main__": syt.setup_logger()


# Todo: 20140908 Add _type
def get_color_id(color_num, colors=None, type='bl'):
    """

    @param color_num:
    @param type: bl, re, ol, ld, lg
    @param colors:
    @return:
    """
    color_id = 9999
    color_num = syt.int_null(color_num)
    if colors is not None:
        try:
            color_id = colors[color_num]
        except:
            pass
    return color_id


def get_bl_piece_ids(bl_design_num=None):
    """
    @param bl_design_num: the number used by bricklink for pieces
    @return: the primary key for a piece in the database or if bl_design_num is none, it returns a list of ids and bl
    """

    if bl_design_num is None:
        element_id = db.run_sql('SELECT id, bricklink_id FROM parts')
    else:
        element_id = db.run_sql('SELECT id FROM parts WHERE bricklink_id=?', (bl_design_num,), one=True)

    return element_id


def get_re_piece_id(re_design_num=None):
    """
    @param re_design_num: the number used by bricklink for pieces
    @return: the primary key for a piece in the database
    """
    if re_design_num is None:
        element_id = db.run_sql('SELECT id, rebrickable_id FROM parts')
    else:
        element_id = db.run_sql('SELECT id FROM parts WHERE rebrickable_id=?', (re_design_num,), one=True)
    return element_id


def get_num_sets_for_part_design(bl_design_num=None):
    """

    @param bl_design_num: The bl design number or None if you want a list of all
    @return: design list of all the designs with the number of sets they are in
    based off bricklink inventories
    """

    designs = None
    if bl_design_num is None:
        designs = db.run_sql("SELECT parts.bricklink_id, COUNT(bl_inventories.set_id) AS number_of_sets FROM parts "
                             "JOIN bl_inventories ON parts.id = bl_inventories.piece_id "
                             "GROUP BY parts.bricklink_id;")
    else:
        designs = db.run_sql("SELECT parts.bricklink_id, COUNT(bl_inventories.set_id) AS number_of_sets FROM parts "
                             "JOIN bl_inventories ON parts.id = bl_inventories.piece_id "
                             "WHERE parts.bricklink_id=?;", (bl_design_num,), one=True)

    return designs


def get_years_available(bl_design_num=None):
    """

    @param bl_design_num: the design id used by bricklink
    @return: the first and last year a design was used in a _set calculated by bl inventories
    """
    years = None
    if bl_design_num is None:
        years = db.run_sql(
            "SELECT MIN(sets.year_released) AS first_year, MAX(sets.year_released) AS last_year FROM parts "
            "JOIN bl_inventories ON parts.id = bl_inventories.piece_id "
            "JOIN sets ON bl_inventories.set_id = sets.id "
            "GROUP BY parts.bricklink_id;")

    else:
        years = db.run_sql(
            "SELECT MIN(sets.year_released) AS first_year, MAX(sets.year_released) AS last_year FROM parts "
            "JOIN bl_inventories ON parts.id = bl_inventories.piece_id "
            "JOIN sets ON bl_inventories.set_id = sets.id "
            "WHERE parts.bricklink_id=?;", (bl_design_num,))

    return years


def get_avg_price_per_design(bl_design_num=None):
    """
        if a piece is 10 cents in one _set and 20 in another this returns 15
        This is also weighted for the number in a _set, so if one _set has 1000 at .10 and another has 100 at .5
        it will be closer to .10
    @param bl_design_num: the design id used by bricklink
    @return: taking the price per piece of a _set, this calculates the average price per piece of a piece; or if no
        bl_design_num is given it returns the values for all pieces by bl_design
    """

    avg_price = None
    if bl_design_num is None:
        avg_price = db.run_sql(
            "SELECT bricklink_id, average_weighted_price FROM parts AS P JOIN "
            "(SELECT bl_inventories.piece_id, SUM((sets.original_price_us / sets.get_piece_count) "
            "* bl_inventories.quantity) / SUM(bl_inventories.quantity) AS average_weighted_price "
            "FROM sets JOIN bl_inventories ON bl_inventories.set_id = sets.id "
            "WHERE sets.original_price_us IS NOT NULL GROUP BY bl_inventories.piece_id) AS R ON P.id=R.piece_id;")
        # This monstrosity gets the average price for every piece in the database by bl_num

    else:
        avg_price = db.run_sql(
            "SELECT average_weighted_price FROM parts AS P "
            "JOIN (SELECT bl_inventories.piece_id, SUM((sets.original_price_us / sets.get_piece_count) "
            "* bl_inventories.quantity) / SUM(bl_inventories.quantity) AS average_weighted_price "
            "FROM sets JOIN bl_inventories ON bl_inventories.set_id = sets.id "
            "WHERE sets.original_price_us IS NOT NULL GROUP BY bl_inventories.piece_id) "
            "AS R ON P.id=R.piece_id WHERE P.bricklink_id=?", (bl_design_num, ), one=True)
        # This beauty returns the average price for a single piece by bl_design num

    return avg_price


if __name__ == "__main__":

    def main_menu():
        """
        Main launch menu
        @return:
        """

        options = (
            ("Get Color ID", menu_get_color_id),
            ("Get RE Part ID", menu_get_re_piece_id),
            ("Get BL Part ID", menu_get_bl_piece_id),
            ("Get #sets / design", menu_get_num_sets_for_part_design),
            ("Get years available", menu_get_years_available),
            ("AVG price by design", menu_get_avg_price_per_design)
        )
        syt.Menu(name="– piece_info.py Testing –", choices=options).run()

    def menu_get_color_id():
        color = input("What color number?")
        print(get_color_id(color))

    def menu_get_bl_piece_id():
        part_num = syt.input_part_num()
        print(get_bl_piece_ids(part_num))
        syt.print4(get_bl_piece_ids())

    def menu_get_re_piece_id():
        part_num = syt.input_part_num()
        print(get_re_piece_id(part_num))
        syt.print4(get_re_piece_id())

    def menu_get_num_sets_for_part_design():
        part_num = syt.input_part_num()
        print(get_num_sets_for_part_design(part_num))
        syt.print4(get_num_sets_for_part_design())


    def menu_get_years_available():
        part_num = syt.input_part_num()
        print(get_years_available(part_num))
        syt.print4(get_years_available())


    def menu_get_avg_price_per_design():
        part_num = syt.input_part_num()
        print(get_avg_price_per_design(part_num))
        syt.print4(get_avg_price_per_design())


    if __name__ == "__main__":
        main_menu()