__author__ = 'andrew.sielen'

import collections
import copy

import arrow

import database as db
from system import base
import navigation as menu
from data.data_classes import SetInfo


class OrderedDictV2(collections.OrderedDict):
    def next_key(self, key):
        next = self._OrderedDict__map[key].next
        if next is self._OrderedDict__root:
            raise ValueError("{!r} is the last key".format(key))
        return next.key

    def previous_key(self, key):
        previous = self._OrderedDict__map[key].prev
        return previous.key

    def first_key(self):
        for key in self: return key
        raise ValueError("OrderedDict() is empty")


class HistoricPriceAnalyser(object):
    STANDARD = 0
    RELATIVE = 1
    RELATIVE_DAY = 2
    DELTA = 3
    DELTA_DAY = 4


    def __init__(self, si=None, select_filter=None):

        """
            @param select_filter: List:
                [select statement, where statement, group?] See the end of this doc for examples
        """
        self.si = si  # the parent set
        sql_query = None
        if isinstance(select_filter, list) and len(select_filter) >= 2:
            sql_query = self._build_historic_data_sql(*select_filter)

        sql_result = self.sql(sql_query)
        if sql_result is not None and len(sql_result):
            base_dict = base.list_to_dict(self._process_date_price_list(sql_result))
            self.original_data = OrderedDictV2(sorted(base_dict.items(), key=lambda t: t[0]))
            # for rebuilding data
            self.sql_query = sql_query
            # Same as clear - but needs to be defined in __init__
            self.working_data = copy.deepcopy(self.original_data)
            #Working_data_format:
            #
            self.base_date = min(self.original_data.keys())  #), key=self.original_data.get)
            self.base_price = self.original_data[self.base_date]
            self.type = self.STANDARD
            self.inf_year = None
        else:
            raise SyntaxError("Invalid HPA Formation")


    def __bool__(self):
        return bool(self.si)

    @property
    def dates(self):
        return self.working_data.keys()

    def _process_date_price_list(self, dp_list):
        """
        Takes a list of dates and prices and fills in the missing dates and extrapolates the prices
        @param dp_list: In this format [(date,price),(date,price))]
        @return:
        """
        dp_list.sort(key=lambda x: x[0])  # Sort the list by date
        dp_list_to_add = []  # date, price combos that need to be added
        DAY = (60 * 60 * 24)  # NUmber of seconds in a day
        for idx, dp in enumerate(dp_list):
            if idx == 0:
                continue
            days_between = abs(base.get_days_between(dp_list[idx][0], dp_list[idx - 1][0]))
            if days_between == 1:
                continue
            else:
                increment = round(
                    (base.float_zero(dp_list[idx][1]) - base.float_zero(dp_list[idx - 1][1])) / days_between, ndigits=2)
                for n in range(1, days_between):
                    # next_date = arrow.get(arrow.get(dp_list[idx-1][0]).replace(days=+n).timestamp).format("YYYY-MM-DD")
                    dp_list_to_add.append([arrow.get(dp_list[idx - 1][0]).replace(days=+n).timestamp,
                                           round((base.float_zero(dp_list[idx - 1][1]) + (increment * n)), ndigits=2)])
        dp_list.extend(dp_list_to_add)
        return dp_list


    def set_inflation_year(self, year=None):
        """
        @param year:
        @param clear: revert back to working data
        @return:
        """
        self.inf_year = None
        if isinstance(year, int):
            if 1950 <= year <= arrow.get().year:
                self.inf_year = year


    def set_report_type(self, rtype=None):
        """
        @param type: Options:
            standard - actual numbers (overrides all others)
            relative - percent change from start date
            relative_day - percent change from previous day (does not take into account start price)
            delta - price change from start date
            delta_day - price change *day over day*  (does not take into account start price)
        """
        if rtype in (self.STANDARD, self.RELATIVE, self.RELATIVE_DAY, self.DELTA, self.DELTA_DAY):
            if rtype != self.type:
                self.type = rtype


    def set_base_price_date(self, price=None, date=None, region="us"):
        """
        @param price: Options:
                standard - compare price against historic prices (influenced by base date)
            These can only be used with relative and delta [type]
                original - compare price against us original
                original - compare price against uk original
        @param date: Options:
                a date to start on (in format YYYY-MM-DD)
                start - list prices with start date as the focus
                end - list prices with end date as the focus
        @param region: Options:
                us or uk
        """
        if date is None or date == "":
            self.base_date = None
            if price == "original":
                if region == "uk":
                    self.base_price = self.si.original_price_uk
                else:
                    self.base_price = self.si.original_price_us
            else:
                self.base_price = None
        elif date == "start":
            if region == "uk":
                self.base_date = self.si.ts_date_released_uk
            else:
                self.base_date = self.si.ts_date_released_us

            if self.base_date is None or self.base_date == "":
                self.base_date = max(self.original_data.keys())
            self.base_price = self._get_price_from_date(self.base_date)
        elif date == "end":
            if region == "uk":
                self.base_date = self.si.ts_date_ended_uk
            else:
                self.base_date = self.si.ts_date_ended_us
            if self.base_date is None or self.base_date == "":
                self.base_date = None
            else:
                self.base_price = self._get_price_from_date(self.base_date)
        else:
            self.base_date = base.get_timestamp(date)
            self.base_price = self._get_price_from_date(self.base_date)

            # if self.base_date is None:
            # self.base_date = min(self.original_data.keys())
            # if self.base_price is None:
            #     self.base_price = max(self.original_data.keys())


    def run(self, by_date=False, clear=True):
        """

        @param clear: Default is to re-run from base. Can also set to False to rerun from existing
        @return:
        Default values
        self.base_date = min(self.original_data, key=self.original_data.get)
        self.base_price = self.original_data[self.base_date]
        self.type = self.STANDARD
        self.inf_year = None
        """
        if clear: self.working_data = copy.deepcopy(self.original_data)
        if isinstance(self.inf_year, int):
            self.working_data = base.adj_dict_for_inf(self.working_data, self.inf_year)
        self._process_change_list()
        return self.get(by_date)


    def run_all(self, types=None, by_date=False):
        self.working_data = copy.deepcopy(self.original_data)
        results_dict = collections.defaultdict()
        in_progress = []
        range_types = range(0, 5)
        if isinstance(types, list):
            range_types = types
        for n in range_types:
            self.set_report_type(n)
            self.set_base_price_date(date="end")
            self.set_base_price_date(price="original")
            self._process_change_list()
            in_progress.append(self.get(by_date))

        for n in in_progress[0]:
            next_row = []
            for m in range(len(in_progress)):
                next_row.append(in_progress[m][n])
            if by_date is True:
                results_dict[n] = next_row
            else:
                results_dict[base.get_ts_day(n)] = next_row
                # Note this returns a list not just a value, if you have one value (one price) you need to pull it out later

        return results_dict


    def _process_change_list(self):
        """
         STANDARD = 0
        RELATIVE = 1
        RELATIVE_DAY = 2
        DELTA = 3
        DELTA_DAY = 4
        relative - percent change from start date
        relative_day - percent change from previous day (does not take into account start price)
        delta - price change from start date
        delta_day - price change *day over day*  (does not take into account start price)
        @param type:
        @return:
        """
        new_dict = collections.defaultdict()
        if self.type == 0:
            return self.working_data  # standard type no change
        elif self.type == self.DELTA:
            for db in self.working_data:
                new_dict[db] = base.float_zero(self.working_data[db]) - base.float_zero(self.base_price)
        elif self.type == self.RELATIVE:
            for db in self.working_data:
                try:
                    new_dict[db] = (base.float_zero(self.working_data[db]) / base.float_zero(self.base_price)) - 1
                except ZeroDivisionError:
                    new_dict[db] = 0
        elif self.type == self.DELTA_DAY:
            for idx, db in enumerate(self.working_data.keys()):
                if idx == 0:
                    new_dict[db] = 0
                    continue
                else:
                    previous_value = self.working_data.previous_key(db)
                    new_dict[db] = base.float_zero(self.working_data[db]) - base.float_zero(
                        self.working_data[previous_value])
        elif self.type == self.RELATIVE_DAY:
            for idx, db in enumerate(self.working_data.keys()):
                if idx == 0:
                    new_dict[db] = 0
                    continue
                else:
                    previous_value = self.working_data.previous_key(db)
                    try:
                        new_dict[db] = round(
                            (base.float_zero(self.working_data[db]) / self.working_data[previous_value]) - 1, 6)
                    except ZeroDivisionError:
                        new_dict[db] = None
        self.working_data = OrderedDictV2(sorted(new_dict.items(), key=lambda t: t[0]))
        return self.working_data


    def clear(self):
        self.working_data = copy.deepcopy(self.original_data)
        self.base_date = min(self.original_data.keys())
        self.base_price = self.original_data[self.base_date]
        self.type = self.STANDARD
        self.inf_year = None

    def get_def(self, type="dict"):
        if type == "list":
            return [self.si.set_num, self.si.theme, self.si.year_released, self.si.original_price_us,
                    self.si.date_released_us, self.si.date_ended_us]
        else:
            return {"set_num": self.si.set_num, "theme": self.si.theme, "date_release": self.si.date_released_us,
                    "original_price": self.si.original_price_us, "base_date": base.get_date(self.base_date),
                    "base_date_ts": self.base_date, "inflation_year": self.inf_year, "base_price": self.base_price,
                    "report_type": self.type, "records": len(self.working_data)}


    def get(self, by_date=False):
        if by_date:
            raw_dict = OrderedDictV2({self.si.get_relative_end_date(d): self.working_data[d] for d in
                                      self.working_data})  # if d >= self.base_date})
            # return_dict = OrderedDictV2()
            # dates = sorted(raw_dict.keys())
            # for i, dte in enumerate(dates):
            # return_dict[i] = raw_dict[dte]
            return raw_dict
        else:
            return self.working_data

    def _get_price_from_date(self, date=None):
        """

        @param date: in format YYYY-MM-DD
        @return:
        """
        if date is None: return None
        compare_ts = date  # base.get_timestamp(date)
        closest_price_date = base.get_closest_list(compare_ts, self.working_data.keys())
        self.base_date = date
        return self.working_data[closest_price_date]

    def _build_historic_data_sql(self, select_=None, where_=None, group=True):
        """Takes what we got in the starter filter (either a complete filter string or a dict of filter options
            and returns a built out sql statement
        """
        h_select = "SELECT historic_prices.record_date"
        if select_ is not None:
            h_select += ", " + select_
        h_joins = " FROM historic_prices JOIN sets ON (sets.id=historic_prices.set_id) JOIN price_types ON (price_types.id=historic_prices.price_type)"
        h_filter = " WHERE sets.set_num='{}'".format(self.si.set_num)
        if where_ is not None:
            h_filter += " and " + where_
        if group:
            h_filter += " GROUP BY historic_prices.record_date"
        h_end = ";"
        h_sql = h_select + h_joins + h_filter + h_end
        return h_sql

    def sql(self, sql_statement):
        """Not safe to have publicly exposed, but very handy for my own personal project"""
        return db.run_sql(sql_statement)

    def eval_report(self):
        """
        Returns two lists that can be turned into csv files

        Set List
        Set_num, theme, year_released, original_price, start_date, end_date

        Price List
        set_num, date(price), date(price), date(price), date(price)
        @param year_start:
        @param year_end:
        @return:
        """
        set_prices = []
        # set_defs = [["SET_NUM", "THEME", "YEAR_RELEASED", "ORIGINAL_PRICE", "DATE_START", "DATE_END"]]
        set_defs = self.get_def(type="list")
        self.clear()
        set_prices = self.run_all(types=[1], by_date=True)  #By date will start with the date ended

        return set_prices, set_defs


if __name__ == "__main__":
    test_HPA = None


    def main_menu():
        """
        Main launch menu
        @return:
        """
        # logger.critical("Set Info testing")

        options = {}

        options['1'] = "Test Historic", menu_test_historic
        options['2'] = "Set Inflation Year", menu_inflation
        options['3'] = "Set Report Type", menu_report_type
        options['4'] = "Set Date Price", menu_date_price
        options['5'] = "Reset", menu_clear
        options['5'] = "Run", menu_get
        options['6'] = "Full Test", menu_test
        options['9'] = "Quit", menu.quit

        while True:
            if test_HPA is not None:
                print("Settings")
                print("Base Date = {}".format(base.get_date(test_HPA.base_date)))
                print("Base Price = {}".format(test_HPA.base_price))
                print("Type = {}".format(test_HPA.type))
                # if test_HPA.inf_year is not None:
                print("Inflation = {}".format(test_HPA.inf_year))
            result = menu.options_menu(options)
            if result is 'kill':
                exit()

    def menu_test_historic():
        global test_HPA

        set_num = base.input_set_num()
        test_set = SetInfo(set_num)

        test_HPA = HistoricPriceAnalyser(si=test_set, select_filter=["AVG(historic_prices.piece_avg)",
                                                                     "(price_types.price_type='historic_new' OR "
                                                                     "price_types.price_type='historic_used')", True])


    def menu_inflation():
        if test_HPA is None:
            menu_test_historic()
        inf_year = input("Enter Inflation Year: ")
        test_HPA.set_inflation_year(base.int_null(inf_year))

    def menu_report_type():
        if test_HPA is None:
            menu_test_historic()
        rtype = input("""Enter Report Type 0-4: \n
        STANDARD = 0
        RELATIVE = 1
        RELATIVE_DAY = 2
        DELTA = 3
        DELTA_DAY = 4\n-->: """)
        test_HPA.set_report_type(base.int_zero(rtype))

    def menu_date_price():
        if test_HPA is None:
            menu_test_historic()
        rprice = input("Enter Comparison Price OR original: ")
        rprice = base.float_null(rprice)
        rdate = input("Enter Comparison Date YYYY-MM-DD OR start or end: ")
        test_HPA.set_base_price_date(price=rprice, date=rdate)

    def menu_get():
        if test_HPA is None:
            menu_test_historic()
        result = test_HPA.run().items()
        base.print4(result, 10)

    def menu_clear():
        if test_HPA is None:
            menu_test_historic()
        test_HPA.clear()

    def menu_test():
        if test_HPA is None:
            menu_test_historic()
        # if bool(test_HPA) is False:
        # print("invalid set num")
        test_HPA.set_report_type(0)
        test_HPA.set_inflation_year(2014)
        test_HPA.set_base_price_date(price="original")
        result = test_HPA.run_all([0, 1])
        base.print4(test_HPA.get_def().items(), 20)
        base.print4(result.items(), 10)
        try:
            test_HPA.clear()

            test_HPA.set_inflation_year(2014)
            test_HPA.set_base_price_date(date="end")
            result = test_HPA.run_all([0, 1], by_date=True)
            base.print4(test_HPA.get_def().items(), 20)
            base.print4(result.items(), 10)
        except AssertionError:
            print("No End Date")

    main_menu()

    #
    # def get_historic_price_trends(self, select_filter=None, type="standard", price="standard", date=None,
    # inflation=None):
    # """
    #     @param select_filter: List:
    #                         [select statement, where statement, group?] See the end of this doc for examples
    #
    #     @param inflation: Options:
    #                         a year to get inflation based on
    #                         None - no changes
    #
    #     All this is done in the lists and not with sql
    #     @return:
    #          {data:{year:price,year:price},settings:{price_type:"",type:"",price:"",date:"",inflation:""}}
    #     """
    #     if isinstance(select_filter, list) and len(select_filter) >= 2:
    #         sql_query = self._build_historic_data_sql(*select_filter)
    #     else:
    #         return self.get_price_history()
    #
    #     working_data = self.sql(sql_query)
    #
    #     base_date = None
    #     base_price = None
    #     if type != "standard":
    #         if date is not None:
    #             if date is "start":
    #                 base_date = self.date_released_us
    #             elif date is "end":
    #                 base_date = self.date_ended_us
    #             else:
    #                 base_date = arrow.get(date)
    #     if price != "standard":
    #         if price == "original_us":
    #             base_price = self.original_price_us
    #         elif price == "original_uk":
    #             base_price = self.original_price_uk
    #
    #     return working_data




    # Historic SQL Exmples
    # BASE
    # SELECT sets.set_num, historic_prices.record_date, price_types.price_type,
    # historic_prices.lots, historic_prices.qty, historic_prices.min, historic_prices.max,
    # historic_prices.avg, historic_prices.qty_avg, historic_prices.piece_avg
    # FROM historic_prices
    # JOIN sets ON (sets.id=historic_prices.set_id)
    #   JOIN price_types ON (price_types.id=historic_prices.price_type)
    # WHERE sets.set_num='10501-1';
    #
    # AVERAGE 2+ fields
    # SELECT sets.set_num, historic_prices.record_date, price_types.price_type, (historic_prices.min+historic_prices.max)/2 # The 2 needs to be flexible
    # FROM historic_prices
    #   JOIN sets ON (sets.id=historic_prices.set_id)
    #   JOIN price_types ON (price_types.id=historic_prices.price_type)
    # WHERE sets.set_num='10501-1';
    #
    # SUM
    # SELECT sets.set_num, historic_prices.record_date, price_types.price_type, (historic_prices.min+historic_prices.max) # Same thing, no division
    # FROM historic_prices
    #   JOIN sets ON (sets.id=historic_prices.set_id)
    #   JOIN price_types ON (price_types.id=historic_prices.price_type)
    # WHERE sets.set_num='10501-1';
    #
    # COMBINE PRICE TYPES - AVERAGE THEM
    # SELECT sets.set_num, historic_prices.record_date, price_types.price_type, AVG(historic_prices.min+historic_prices.max)
    # FROM historic_prices
    #   JOIN sets ON (sets.id=historic_prices.set_id)
    #   JOIN price_types ON (price_types.id=historic_prices.price_type)
    # WHERE sets.set_num='10501-1' and (price_types.price_type='historic_used' OR price_types.price_type='historic_new')
    # GROUP BY historic_prices.record_date;
    #
    # COMBINE PRICE TYPES - SUM THEM (ALSO CAN DO MIN AND MAX)
    # SELECT sets.set_num, historic_prices.record_date, price_types.price_type, SUM(historic_prices.min+historic_prices.max)
    # FROM historic_prices
    #   JOIN sets ON (sets.id=historic_prices.set_id)
    #   JOIN price_types ON (price_types.id=historic_prices.price_type)
    # WHERE sets.set_num='10501-1' and (price_types.price_type='historic_used' OR price_types.price_type='historic_new')
    # GROUP BY historic_prices.record_date;