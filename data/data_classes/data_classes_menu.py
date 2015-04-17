# Internal
from data.data_classes import SetInfo, HistoricPriceAnalyser
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
    set_num = SetInfo.input_set_num()
    test_set = SetInfo(set_num)


def si_menu_create_set_lst():
    global test_set
    set_num = SetInfo.input_set_num()
    set_info_list = SetInfo.get_set_info(set_num) #This is probably a stupid thing to test
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
    print(test_set.debug_dump_basic_calcs())


def si_menu_test_inflation():
    global test_set
    while not bool(test_set):
        si_menu_create_set_db()
    print(test_set.debug_dump_inflation())


def si_menu_test_date_range():
    global test_set
    while not bool(test_set):
        si_menu_create_set_db()
    print(test_set.get_relative_end_date_range())


def si_menu_test_sql_data():
    global test_set
    while not bool(test_set):
        si_menu_create_set_db()
    print(test_set.debug_dump_sql_data())


def si_menu_test_historic():
    global test_set
    while not bool(test_set):
        si_menu_create_set_db()
    price_history = test_set.debug_dump_historic()
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
    test_set.make_set_report()


def hpa_menu():
    """
    Main launch menu
    @return:
    """
    # logger.critical("Set Info testing")
    HistoricPriceAnalyser.create()
    #
    # def menu_text():
    # text = "- HPA Settings -\n"
    #     if test_HPA is not None:
    #         text += "Set Num = {}\n".format(test_HPA.si.set_num)
    #         text += "Base Date = {}\n".format(syt.get_date(test_HPA._base_date))
    #         text += "Base Price = {}\n".format(test_HPA._base_price)
    #         text += "Type = {}\n".format(test_HPA._type)
    #         # if test_HPA._inf_year is not None:
    #         text += "Inflation = {}\n".format(test_HPA._inf_year)
    #     return text
    #
    # options = (
    #     ("Test Historic", hpa_menu_create),
    #     ("Set Inflation Year", hpa_menu_inflation),
    #     ("Set Report Type", hpa_menu_report_type),
    #     ("Set Date Price", hpa_menu_date_price),
    #     ("Reset", hpa_menu_clear),
    #     ("Run", hpa_menu_get),
    #     ("Full Test", hpa_menu_test),
    # )
    #
    # syt.Menu(name=menu_text, choices=options).run()


def hpa_menu_create():
    """
    The point is to test the ability of the historic price analyzer
    @return:
    """
    global test_HPA
    test_HPA = HistoricPriceAnalyser.create()
    return test_HPA


def hpa_menu_inflation():
    if test_HPA is None:
        hpa_menu_create()
    inf_year = input("Enter Inflation Year: ")
    test_HPA.set_inflation_year(syt.int_null(inf_year))


def hpa_menu_report_type():
    if test_HPA is None:
        hpa_menu_create()
    rtype = input("""Enter Report Type 0-4: \n
    STANDARD = 0
    RELATIVE = 1
    RELATIVE_DAY = 2
    DELTA = 3
    DELTA_DAY = 4\n-->: """)
    test_HPA.set_report_type(syt.int_zero(rtype))


def hpa_menu_date_price():
    if test_HPA is None:
        hpa_menu_create()
    rprice = input("Enter Comparison Price OR original: ")
    rprice = syt.float_null(rprice)
    rdate = input("Enter Comparison Date YYYY-MM-DD OR start or end: ")
    test_HPA.set_base_price_date(price=rprice, date=rdate)


def hpa_menu_get():
    if test_HPA is None:
        hpa_menu_create()
    result = test_HPA.run().items()
    syt.print4(result, 10)


def hpa_menu_clear():
    if test_HPA is None:
        hpa_menu_create()
    test_HPA.clear()


def hpa_menu_test():
    if test_HPA is None:
        hpa_menu_create()
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




