# External
import collections


# Internal
import database as db
from data.data_classes.SetInfo_HPA_Class import HistoricPriceAnalyser, SetInfo
import navigation as menu
import system as syt


class SetCollection(object):
    """
        This stores a list of sets, but it also stores the filter list to get that list of text
        This makes it easier to do mass things to it because we can then do it just in sql instead
        of loops
    """

    def __init__(self, set_list=None, filter_text=None):
        """
        @param set_list: List of set_nums
        @param filter_text: Filter Text e.g. "year_released = 2014, theme = city
        @return:
        """

        set_filters = ""
        if set_list is not None and isinstance(set_list, list):
            set_filters = _set_filter_creator(set_list)
        if filter_text is not None:
            set_filters = "(" + filter_text + ")" + set_filters

        # set_data = _set_info_creator(self._run_query(filter_text=set_filters))
        self.set_data_lookups = {"calc_piece_count": None, "calc_unique_piece_count": None, "calc_weight": None,
                                 "calc_inf_price": None}

        self.set_info_list = None  # set_data  # The actual SetInfo class objects
        self.filter_text = set_filters  # The filter used to reconstruct the collection
        self.recent_query = []
        self.recent_query.append(self._query_builder(
            filter_text=set_filters))  # To track the history of filters, may come in handy? time will tell

    def _run_query(self, base_text=None, filter_text=None, one=False):
        query = self._query_builder(base_text, filter_text)
        self.recent_query.insert(0, query)
        return db.run_sql(query, one=one)

    def _query_builder(self, base_text=None, filter_text=None):
        if base_text is None:
            base_text = 'SELECT * FROM sets'
        if filter_text is None:
            return base_text + " WHERE " + self.filter_text + ";"
        else:
            return base_text + " WHERE " + self.filter_text + " " + filter_text + ";"

    def sql(self, base_text=None, filter_text=None):
        """Not safe to have publicly exposed, but very handy for my own personal project"""
        query_text = self._query_builder(base_text=base_text, filter_text=filter_text)
        return db.run_sql(query_text)

    # #
    # Basic Info
    # #
    @property
    def num_sets(self):
        """ Number of sets in the collection """
        return self.__len__()

    def __len__(self):
        """number of sets in the collection"""
        return len(self.set_info_list)

    def date_range(self):
        """The date range of the collection """
        # Todo: Add month and region
        max_date = None
        min_date = None
        max_date = self._run_query(base_text="SELECT MAX(year_released) FROM sets", one=True)
        min_date = self._run_query(base_text="SELECT MIN(year_released) FROM sets", one=True)
        return min_date, max_date

    def themes(self, subtheme=False, coverage=False):
        """List of all the themes in the collection, when coverage is true, it returns the num of sets that have this field"""
        # Todo: add subtheme
        theme_list = self._run_query(base_text="SELECT DISTINCT theme FROM sets")
        if coverage:
            return theme_list, len(theme_list)
        return theme_list

    def set_nums(self):
        """List of all set nums"""
        nums_list = self._run_query(base_text="SELECT set_num FROM sets", filter_text=None)
        nums_list = [n[0] for n in nums_list]
        return nums_list

    def _get_num_value(self, field="", type=None):
        """
        Used for any of the fields on a set record that could contain a value that is worth summing counting etc
        """
        result = None
        if field is None: return None
        if type is "total":
            result = self._run_query(base_text="SELECT SUM({}) FROM sets".format(field))
        elif type is "average":
            result = self._run_query(base_text="SELECT AVG({}) FROM sets".format(field))
        else:
            result_list = self._run_query(base_text="SELECT set_num, {} FROM sets".format(field))
            result = syt.list_to_dict(result_list)
        return result

    def unique_piece_count(self):
        if self.set_data_lookups["calc_unique_piece_count"] is not None:
            return self.set_data_lookups["calc_unique_piece_count"]
        query = ("SELECT set_num, unique_pieces FROM sets AS S JOIN (SELECT bl_inventories.set_id, "
                 "COUNT(bl_inventories.quantity) AS unique_pieces FROM bl_inventories "
                 "JOIN parts ON bl_inventories.piece_id = parts.id",
                 "GROUP BY bl_inventories.set_id) AS U ON S.id = U.set_id")
        self.set_data_lookups["calc_unique_piece_count"] = self._run_query(query[0], query[1])
        return self.set_data_lookups["calc_unique_piece_count"]

    def piece_count(self, type=None, calc=False):
        if calc:
            query = None
            if self.set_data_lookups["calc_piece_count"] is not None and type is None:
                return self.set_data_lookups["calc_piece_count"]
            if calc:
                query = (
                    "SELECT set_num, SUM(bl_inventories.quantity) FROM bl_inventories JOIN sets ON (bl_inventories.set_id=sets.id)",
                    "GROUP BY sets.set_num")
            if type == "total":
                query = (
                    "SELECT SUM(bl_inventories.quantity) FROM bl_inventories JOIN sets ON (bl_inventories.set_id=sets.id)",
                    None)
            elif type == "average":
                query = (
                    "SELECT AVG(bl_inventories.quantity) FROM bl_inventories JOIN sets ON (bl_inventories.set_id=sets.id)",
                    None)
            if type is None:
                self.set_data_lookups["calc_piece_count"] = self._run_query(query[0], query[1])
            return self._run_query(query[0], query[1])
        else:
            return self._get_num_value(field="piece_count", type=type)

    def prices(self, type=None, year=None):
        """
        @param type; either None, average, or total
        @param year; If this is a number it will adjust all the prices for that years inflation
        @return:
        """
        # Todo, year
        return self._get_num_value(field="original_price_us", type=type)

    def weights(self, type=None, calc=False):
        if calc:
            if self.set_data_lookups["calc_weight"] is not None:
                return self.set_data_lookups["calc_weight"]
            query = (
                "SELECT sets.set_num, SUM(bl_inventories.quantity * parts.weight) FROM bl_inventories JOIN parts ON bl_inventories.piece_id = parts.id JOIN sets ON bl_inventories.set_id = sets.id",
                "GROUP BY sets.set_num")
            if type == "total":
                query = (
                    "SELECT SUM(bl_inventories.quantity * parts.weight) FROM bl_inventories JOIN parts ON bl_inventories.piece_id = parts.id",
                    None)
            elif type == "average":
                query = (
                    "SELECT AVG(bl_inventories.quantity * parts.weight) FROM bl_inventories JOIN parts ON bl_inventories.piece_id = parts.id",
                    None)
            if type is None:
                self.set_data_lookups["calc_weight"] = self._run_query(query[0], query[1])
            return self._run_query(query[0], query[1])
        else:
            return self._get_num_value(field="set_weight", type=type)

    def figures(self, type=None):
        return self._get_num_value(field="figures", type=type)

    def age_range(self, type=None):
        age_result = {"low": None, "high": None}
        if type is "dist":
            age_result["low"] = self._run_query(base_text="SELECT age_low, COUNT(age_low) FROM sets",
                                                filter_text="GROUP BY age_low")
            age_result["high"] = self._run_query(base_text="SELECT age_high, COUNT(age_high) FROM sets",
                                                 filter_text="GROUP BY age_high")
        else:
            age_result["low"] = self._run_query(base_text="SELECT MIN(age_low) FROM sets", one=True)
            age_result["high"] = self._run_query(base_text="SELECT MAX(age_high) FROM sets", one=True)
        return age_result

    # #
    # Calculated Data
    ##
    def ppp(self, type=None):
        pass

    def ppg(self, type=None):
        pass

    def unique_piece_count(self, type=None):
        pass

    ##
    #CSV DUMP
    ##
    # @profile
    def csv_dump(self):
        csv_dump_string = ""
        csv_dump_string += "id, set_num, set_name, set_theme, piece_count, figures, set_weight, year_released, date_released_us, date_ended_us, " \
                           "date_released_uk, date_ended_uk, original_price_us, original_price_uk, age_low, age_high, box_size, box_volume, " \
                           "last_updated, last_inv_updated_bl, last_inv_updated_re, last_daily_update, BASE CALC, ppp, ppp_uk, ppg, ppg_uk, " \
                           "avg_piece_weight,INFLATION, price_inf, ppp_inf, ppg_inf, CALC PIECE/WEIGHT, calc_piece_count, calc_unique_piece_count, " \
                           "calc_unique_to_total_piece_count, calc_weight, calc_avg_piece_weight, CALC INFLATION, calc_ppp_inf, calc_ppg_inf\n"
        timer = syt.process_timer("BUILDING CSV")
        sets = self.set_nums()
        total_sets = len(sets)
        timer.log_time(1, total_sets)
        current_set_count = 0
        for snum in sets:
            tSetInfo = SetInfo(snum)
            csv_dump_string += tSetInfo.set_dump()
            current_set_count += 1
            if current_set_count >= 50:
                timer.log_time(current_set_count, total_sets - (timer.tasks_completed + current_set_count))
                current_set_count = 0
        timer.end()
        return csv_dump_string

    ##
    # Advanced Data
    ##
    def historic_price_trends(self, type="standard", price="standard", date="", inflation=None):
        """

        """
        historic_data_sets = collections.defaultdict()
        sfilter = ["AVG(historic_prices.qty_avg)",
                   "(price_types.price_type='historic_new' OR price_types.price_type='historic_used')",
                   True]  #Third option (Group) needs to be true if getting multiple values
        for snum in self.set_nums():
            print("Getting snum {}".format(snum))
            tHPA = HistoricPriceAnalyser(si=SetInfo(snum), select_filter=sfilter)
            tHPA.set_base_price_date(date="end")
            historic_data_sets[snum] = tHPA.run_all([0, 1], by_date=True)

        print("Check")
        return historic_data_sets


    def historic_price_report(self):
        """
        Get all prices for sets between (filter text "(year_released BETWEEN 2008 AND 2014)") Relative to their end date
            Day 0 is the end date, days before are negative, days after are positive
            Values for prices are in percent change from original
            Prices are the average of new and used historic qty avg prices
        """
        historic_price_sets = collections.defaultdict()
        historic_set_defs = collections.defaultdict()
        sfilter = ["AVG(historic_prices.qty_avg)",
                   "(price_types.price_type='historic_used')",
                   True]  #Third option (Group) needs to be true if getting multiple values
        date_list = []
        date_range = [0, 0]
        for snum in self.set_nums():
            print("Getting snum {}".format(snum))
            tHPA = HistoricPriceAnalyser(si=SetInfo(snum), select_filter=sfilter)
            tdate_range = tHPA.si.get_relative_end_date_range()
            if tdate_range[
                0] is None:  #If there is no starting date, there is nothing to compare to, don't really need to check end date also
                continue
            if tdate_range[0] is not None and tdate_range[0] < date_range[0]:
                date_range[0] = tdate_range[0]
            if tdate_range[1] is not None and tdate_range[1] > date_range[1]:
                date_range[1] = tdate_range[1]
            historic_price_sets[snum], historic_set_defs[snum] = tHPA.eval_re
            port()

        date_list.sort()
        price_csv = "SET_NUM"
        print("Building Price CSV")
        for dte in range(date_range[0], date_range[1]):
            price_csv += ",{}".format(dte)  #syt.get_date(dte))
        price_csv += "\n"

        for st in historic_price_sets:
            if len(historic_price_sets[st]) < 2:
                continue
            price_csv += "{}".format(st)
            for dte in range(date_range[0], date_range[1]):
                if dte in historic_price_sets[st]:
                    if isinstance(historic_price_sets[st][dte], list):
                        price_csv += ",{}".format(historic_price_sets[st][dte][0])
                    else:
                        price_csv += ",{}".format(historic_price_sets[st][dte])
                else:
                    price_csv += ", "
            price_csv += "\n"
        print("Building Set DEF CSV")

        set_csv = "SET_NUM, THEME, YEAR_RELEASED, ORIGINAL_PRICE, START_DATE, END_DATE\n"
        for st in historic_set_defs:
            set_csv += syt.list2string(historic_set_defs[st])
            set_csv += "\n"

        with open('{}-price-data.csv'.format(syt.get_timestamp()), "w") as f:
            f.write(price_csv)

        with open('{}-price-set-data.csv'.format(syt.get_timestamp()), "w") as f:
            f.write(set_csv)


    def historic_data_trends(self):
        pass


def _set_filter_creator(set_lists):
    """
    Take a list of set lists and return a filter statement:  " OR set_num=xxx-xx OR ..."
    @param set_lists:
    @return:
    """
    set_num_filter = ""
    for s in set_lists:
        cset_num = _validate_set_list(s, allow_set_nums=True)
        if cset_num:
            set_num_filter += " OR sets.set_num = {}".format(cset_num)
        cset_num = None
    return set_num_filter


def _set_info_creator(set_list):
    """

    @param set_list: Take a list of set lists and return SetInfo objects
    @return:
    """
    SetInfo_list = []
    for s in set_list:
        SetInfo_list.append(SetInfo(s))
    return SetInfo_list


def _validate_set_list(set_list, allow_set_nums=False):
    if len(set_list) == 27 and isinstance(set_list[1], str):
        return set_list[1]
    elif allow_set_nums is True and isinstance(set_list, str):
        return set_list
    return False


if __name__ == "__main__":
    test_SC = None


    def main_menu():

        options = {}

        options['1'] = "Create Set Collection", menu_createSC
        options['2'] = "Get Historic", menu_test_historic
        options['3'] = "Get all Set Data", menu_data_dump
        options['9'] = "Quit", menu.quit

        while True:
            result = menu.options_menu(options)
            if result is 'kill':
                exit()

    def menu_createSC():
        global test_SC
        filter_text = "(year_released BETWEEN 2008 AND 2015)"
        test_SC = SetCollection(filter_text=filter_text)

    def menu_test_historic():
        global test_SC
        filter_text = "(year_released BETWEEN 1980 AND 2015) AND ((piece_count >=25) OR (original_price_us >=4)) AND year_released IS NOT NULL AND set_name IS NOT NULL"
        test_SC = SetCollection(filter_text=filter_text)
        historic_data_sets = test_SC.historic_price_report()
        syt.print4(historic_data_sets.items(), 20)

    def menu_get_historic_prices():
        global test_SC
        filter_text = "(year_released BETWEEN 2008 AND 2015)"
        test_SC = SetCollection(filter_text=filter_text)

    def menu_data_dump():
        global test_SC
        filter_text = "(year_released BETWEEN 1980 AND 2015) AND ((piece_count >=25) OR (original_price_us >=4)) AND year_released IS NOT NULL AND set_name IS NOT NULL"
        test_SC = SetCollection(filter_text=filter_text)
        csv_dump_text = test_SC.csv_dump()
        with open('{}-set-collection-dump.csv'.format(syt.get_timestamp()), "w") as f:
            f.write(csv_dump_text)

    main_menu()
