# Internal
from data.data_classes import SetInfo, HistoricPriceAnalyser
from database import info
import navigation as menu
import system as syt
if __name__ == "__main__": syt.setup_logger()


if __name__ == "__main__":
    test_HPA = None
    test_set = SetInfo()

    def main_menu():
        options = {}

        options['1'] = "Test SetInfo Class", si_menu
        options['2'] = "Test Historic Price Data Class", hpa_menu
        options['9'] = "Quit", menu.quit

        while True:
            result = menu.options_menu(options)
            if result is 'kill':
                exit()

    def si_menu():

        """
        Main launch menu
        @return:
        """
        syt.log_critical("Set Info testing")

        options = {}

        options['1'] = "Create Set from DB", si_menu_create_set_db
        options['2'] = "Create Set from List", si_menu_create_set_lst
        options['3'] = "Test Base Info", si_menu_get_base_info
        options['4'] = "Test Basic Calcs", si_menu_get_basic_calcs
        options['5'] = "Test Inflation", si_menu_test_inflation
        options['6'] = "Test SQL Data", si_menu_test_sql_data
        options['7'] = "Test Historic", si_menu_test_historic
        options['8'] = "Test all Output", si_menu_test_all_output
        #options['S'] = "Test SQL Historic", menu_test_sql_historic
        options['D'] = "Get Date Min", si_menu_test_date_range
        options['C'] = "GET CSV DUMP", si_menu_text_csv_dump
        options['9'] = "Quit", menu.quit

        while True:
            print("Current Set: {}".format(test_set.set_num))
            result = menu.options_menu(options)
            if result is 'kill':
                exit()

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
        price_history, rating_history = test_set.test_historic()
        print("Price History")
        syt.print4(price_history)
        print("Rating History")
        syt.print4(rating_history)

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
        print(test_set.set_dump())

    # def menu_test_sql_historic():
    #     global test_set
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

        options = {}

        options['1'] = "Test Historic", hpa_menu_test_historic
        options['2'] = "Set Inflation Year", hpa_menu_inflation
        options['3'] = "Set Report Type", hpa_menu_report_type
        options['4'] = "Set Date Price", hpa_menu_date_price
        options['5'] = "Reset", hpa_menu_clear
        options['5'] = "Run", hpa_menu_get
        options['6'] = "Full Test", hpa_menu_test
        options['9'] = "Quit", menu.quit

        while True:
            if test_HPA is not None:
                print("Settings")
                print("Base Date = {}".format(syt.get_date(test_HPA.base_date)))
                print("Base Price = {}".format(test_HPA.base_price))
                print("Type = {}".format(test_HPA.type))
                # if test_HPA.inf_year is not None:
                print("Inflation = {}".format(test_HPA.inf_year))
            result = menu.options_menu(options)
            if result is 'kill':
                exit()

    def hpa_menu_test_historic():
        global test_HPA

        set_num = syt.input_set_num()
        test_set = SetInfo(set_num)

        test_HPA = HistoricPriceAnalyser(si=test_set, select_filter=["AVG(historic_prices.piece_avg)",
                                                                     "(price_types.price_type='historic_new' OR "
                                                                     "price_types.price_type='historic_used')", True])


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
        # if bool(test_HPA) is False:
        # print("invalid set num")
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
    main_menu()




