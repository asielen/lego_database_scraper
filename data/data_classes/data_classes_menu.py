# Internal
from data.data_classes import SetInfo, HistoricPriceAnalyser
from database import info
import system as syt

if __name__ == "__main__": syt.setup_logger()

test_HPA = None
test_set = SetInfo()


def main_menu():
    options = (
        ("Test SetInfo Class", si_menu),
        ("Test Historic Price Data Class", hpa_menu),
    )

    syt.Menu(name="- Data Class Tests -", choices=options).run()


def si_menu():
    """
    Main launch menu
    @return:
    """
    syt.log_critical("Set Info testing")

    def menu_text():
        text = "Current Set: {}".format(test_set.set_num)
        return text

    options = (
        ("Create Set from DB", si_menu_create_set_db),
        ("Create Set from List", si_menu_create_set_lst),
        ("Test Base Info", si_menu_get_base_info),
        ("Test Basic Calcs", si_menu_get_basic_calcs),
        ("Test Inflation", si_menu_test_inflation),
        ("Test SQL Data", si_menu_test_sql_data),
        ("Test Historic", si_menu_test_historic),
        ("Test all Output", si_menu_test_all_output),
        ("Get Date Min", si_menu_test_date_range),
        ("Set Report", si_menu_text_csv_dump),
    )

    syt.Menu(name=menu_text, choices=options).run()


def si_menu_create_set_db():
    global test_set
    set_num = syt.input_set_num()
    test_set = SetInfo(set_num)


def si_menu_create_set_lst():
    global test_set
    set_num = syt.input_set_num()
    set_info_list = info.get_set_info(set_num)
    test_set = SetInfo(set_info_list)


def si_menu_get_base_info():
    global test_set
    while not bool(test_set):
        si_menu_create_set_db()
    print(test_set)


def si_menu_get_basic_calcs():
    global test_set
    while not bool(test_set):
        si_menu_create_set_db()
    print(test_set.test_basic_calcs())


def si_menu_test_inflation():
    global test_set
    while not bool(test_set):
        si_menu_create_set_db()
    print(test_set.test_inflation())


def si_menu_test_date_range():
    global test_set
    while not bool(test_set):
        si_menu_create_set_db()
    print(test_set.get_relative_end_date_range())


def si_menu_test_sql_data():
    global test_set
    while not bool(test_set):
        si_menu_create_set_db()
    print(test_set.test_sql_data())


def si_menu_test_historic():
    global test_set
    while not bool(test_set):
        si_menu_create_set_db()
    price_history = test_set.test_historic()
    print("Price History")
    syt.print4(price_history)
    # print("Rating History")
    # syt.print4(rating_history)


def si_menu_test_all_output():
    global test_set
    while not bool(test_set):
        si_menu_create_set_db()
    si_menu_get_base_info()
    si_menu_get_basic_calcs()
    si_menu_test_inflation()
    si_menu_test_sql_data()
    si_menu_test_historic()


def si_menu_text_csv_dump():
    global test_set
    while not bool(test_set):
        si_menu_create_set_db()
    test_set.set_report()


# def menu_test_sql_historic():
# global test_set
#     while not bool(test_set):
#         menu_create_set_db()
#     c_result = test_set.get_historic_price_trends()
#     syt.print4(c_result, 5)
#     c_result = test_set.get_historic_price_trends(
#         select_filter=["(historic_prices.min+historic_prices.max)/2", None, False])
#     syt.print4(c_result, 5)
#     c_result = test_set.get_historic_price_trends(select_filter=["(historic_prices.min+historic_prices.max)",
#                                                                  "(price_types.price_type='historic_used' OR price_types.price_type='historic_new')",
#                                                                  False])
#     syt.print4(c_result, 5)
#     c_result = test_set.get_historic_price_trends(select_filter=["SUM(historic_prices.min+historic_prices.max)",
#                                                                  "(price_types.price_type='historic_used' OR price_types.price_type='historic_new')",
#                                                                  True])
#     syt.print4(c_result, 5)

def hpa_menu():
    """
    Main launch menu
    @return:
    """
    # logger.critical("Set Info testing")

    def menu_text():
        text = "- HPA Settings -\n"
        if test_HPA is not None:
            text += "Set Num = {}\n".format(test_HPA.si.set_num)
            text += "Base Date = {}\n".format(syt.get_date(test_HPA.base_date))
            text += "Base Price = {}\n".format(test_HPA.base_price)
            text += "Type = {}\n".format(test_HPA.type)
            # if test_HPA.inf_year is not None:
            text += "Inflation = {}\n".format(test_HPA.inf_year)
        return text

    options = (
        ("Test Historic", hpa_menu_test_historic),
        ("Set Inflation Year", hpa_menu_inflation),
        ("Set Report Type", hpa_menu_report_type),
        ("Set Date Price", hpa_menu_date_price),
        ("Reset", hpa_menu_clear),
        ("Run", hpa_menu_get),
        ("Full Test", hpa_menu_test),
    )

    syt.Menu(name=menu_text, choices=options).run()


def hpa_menu_test_historic():
    """
    The point is to test the ability of the historic price analyzer
    @return:
    """
    global test_HPA

    set_num = syt.input_set_num()
    test_set = SetInfo(set_num)
    test_HPA = HistoricPriceAnalyser(si=test_set, select_filter=HistoricPriceAnalyser.build_filter())


# Now a static method in the HPA class
# def hpa_builder():
# """
#     Through a set of menus, this creates the select string for a HPA class
#     @return:
#     """
#     hpa_string = ""
#
#     def hpa_build_rating():
#         qstring = ["",None,True]
#         options = ["Want","Own","Rating","Want+Own","Want-Own"]
#         choice = syt.Menu("- Create HPA Query Rating -", choices=options, type="return", quit=False, drop_down=True).choice
#
#         if choice == "Want":
#             qstring[0] = "bs_ratings.want"
#         elif choice == "Own":
#             qstring[0] = "bs_ratings.own"
#         elif choice == "Rating":
#             qstring[0] = "bs_ratings.rating"
#         elif choice == "Want+Own":
#             qstring[0] = "(bs_ratings.want + bs_ratings.own)"
#         elif choice == "Want-Own":
#             qstring[0] = "(bs_ratings.want - bs_ratings.own)"
#
#         return qstring
#
#     def hpa_build_price():
#
#
#         price_types = ["historic_new", "historic_used", "current_new", "current_used"]
#         fields = ["avg", "lots", "max", "min", "qty", "qty_avg", "piece_avg"]
#         group_functions = ["AVG","MIN","MAX","SUM"] # For price types
#         aggregate_functions = ["AVG","SUM","DIFFERENCE"] # For fields
#         c_price_types = []
#         c_fields = []
#         c_group_function = None
#         c_aggregate_function = None
#
#         c_price_types = syt.MultiChoiceMenu(price_types)
#         if len(c_price_types)>1:
#             c_group_function = syt.Menu("- Choose group function -", choices=group_functions, drop_down=True, type=syt.Menu.RETURN).choice
#         c_fields = syt.MultiChoiceMenu(fields)
#         if len(c_fields)>1:
#             c_aggregate_function = syt.Menu("- Choose aggregate function -", choices=aggregate_functions, drop_down=True, type=syt.Menu.RETURN).choice
#
#
#         return {"price_type": c_price_types, "field": c_fields,
#                 "group_function": c_group_function, "aggregate_function": c_aggregate_function}
#
#
#
#     options = [("Rating", hpa_build_rating),
#                ("Price", hpa_build_price)]
#     hpa_string = syt.Menu("- Create HPA Query -", choices=options, quit=False, drop_down=True).choice
#
#     return hpa_string



def hpa_menu_inflation():
    if test_HPA is None:
        hpa_menu_test_historic()
    inf_year = input("Enter Inflation Year: ")
    test_HPA.set_inflation_year(syt.int_null(inf_year))


def hpa_menu_report_type():
    if test_HPA is None:
        hpa_menu_test_historic()
    rtype = input("""Enter Report Type 0-4: \n
    STANDARD = 0
    RELATIVE = 1
    RELATIVE_DAY = 2
    DELTA = 3
    DELTA_DAY = 4\n-->: """)
    test_HPA.set_report_type(syt.int_zero(rtype))


def hpa_menu_date_price():
    if test_HPA is None:
        hpa_menu_test_historic()
    rprice = input("Enter Comparison Price OR original: ")
    rprice = syt.float_null(rprice)
    rdate = input("Enter Comparison Date YYYY-MM-DD OR start or end: ")
    test_HPA.set_base_price_date(price=rprice, date=rdate)


def hpa_menu_get():
    if test_HPA is None:
        hpa_menu_test_historic()
    result = test_HPA.run().items()
    syt.print4(result, 10)


def hpa_menu_clear():
    if test_HPA is None:
        hpa_menu_test_historic()
    test_HPA.clear()


def hpa_menu_test():
    if test_HPA is None:
        hpa_menu_test_historic()
    test_HPA.set_report_type(0)
    test_HPA.set_inflation_year(2014)
    test_HPA.set_base_price_date(price="original")
    result = test_HPA.run_all([0, 1])
    syt.print4(test_HPA.get_def().items(), 20)
    syt.print4(result.items(), 10)
    try:
        test_HPA.clear()

        test_HPA.set_inflation_year(2014)
        test_HPA.set_base_price_date(date="end")
        result = test_HPA.run_all([0, 1], by_date=True)
        syt.print4(test_HPA.get_def().items(), 20)
        syt.print4(result.items(), 10)
    except AssertionError:
        print("No End Date")


if __name__ == "__main__":
    main_menu()




