__author__ = 'andrew.sielen'

import database as db
from data.data_classes.SetInfo_class import SetInfo
from system import base


class SetCollection(object):
    """
        This stores a list of sets, but it also stores the filter list to get that list of text
        This makes it easier to do mass things to it because we can then do it just in sql instead
        of loops
    """

    def __init__(self, set_list=None, filter_text=None):
        """
        @param set_list: List of set_nums
        @param filter: Filter Text e.g. "year_released = 2014, theme = city
        @return:
        """

        set_filters = ""
        if set_list is not None and isinstance(set_list, list):
            set_filters = _set_filter_creator(set_list)
        if filter_text is not None:
            set_filters = "(" + filter_text + ")" + set_filters

        # set_data = _set_info_creator(self._run_query(filter_text=set_filters))

        self.set_info_list = None  # set_data  # The actual SetInfo class objects
        self.filter_text = set_filters  # The filter used to reconstruct the collection
        self.recent_query = []
        self.recent_query.append(self._query_builder(
            filter_text=set_filters))  # To track the history of filters, may come in handy? time will tell

    def _run_query(self, base_text=None, filter_text=None, one=False):
        query = self._query_builder(base_text, filter_text)
        self.recent_query.insert(0, query)  # Todo, this should add to the front so we can keep is to a limited history
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
        nums_list = self._run_query(base_text="SELECT set_num FROM sets", filter_text=self.filter_text)
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
            result = base.list_to_dict(result_list)
        return result

    def piece_count(self, type=None, calc=False):
        if calc:
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

    ##
    # Calculated Data
    ##
    def ppp(self, type=None):
        pass

    def ppg(self, type=None):
        pass

    def unique_piece_count(self, type=None):
        pass

    ##
    # Advanced Data
    ##
    def historic_price_trends(self, type="standard", price="standard", date="", inflation=None):
        """
        @param type: Options:
                            standard - actual numbers
                            relative - percent change
                            delta - price change
        @param type: Options:
                                standard - compare price against historic prices
                            These can only be used with relative and delta [type]
                                original_us - compare price against us original
                                original_uk - compare price against uk original
        @param date: Options:
                            a date to start on
                            release date - list prices with start date as the focus
                            end date - list prices with end date as the focus
        @param inflation: Options:
                            a year to get inflation based on
                            None - no changes

        All this is done in the lists and not with sql
        """

        # First make SetInfos for each set if they don't exists
        self.set_info_list = _set_info_creator(self._run_query(filter_text=self.filter_text))
        for s in self.set_info_list:
            pass
        pass

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
