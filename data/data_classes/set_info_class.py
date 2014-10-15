__author__ = 'andrew.sielen'

import arrow

from database import info
import database as db
from system import base
from data import update_secondary
import navigation as menu
from system import logger
from system import calculate_inflation as inf


class SetInfo(object):
    """
    Used for an individual set
    """

    def __init__(self, set_info=None):
        """

        @param set_info: Can either be a string of the set_num or a list
        @return:
        """
        set_info_list = None
        s_num = None
        if set_info is not None:
            if isinstance(set_info, list) or isinstance(set_info, tuple):
                # If init with a list
                if len(set_info) == 27:
                    set_info_list = list(set_info)
                elif len(set_info) > 2 and isinstance(set_info[1], str):
                    # If the list is the wrong size, it still trys to find a set_num
                    s_num = base.expand_set_num(set_info[1])[2]
            else:
                if isinstance(set_info, str):
                    # If init with a string
                    s_num = base.expand_set_num(set_info)[2]

        if s_num is not None:
            # Todo: Cant add set with this function here because it causes a circular import
            set_info_list = info.get_set_info(set_info)  # , new=True)

        if set_info_list is None:
            self.set_info_list = [None] * 27  # New Empty Set
            if s_num is not None:
                self.set_info_list[1] = s_num
        else:
            self.set_info_list = set_info_list

    # ###
    # #Basic Properties
    # ##
    @property
    def db_id(self):
        """
        @return: the database id
        """
        return self.set_info_list[0]

    @property
    def set_num(self):
        """
        @return: the set num, set item num and set seq
        """
        return self.set_info_list[1]

    @set_num.setter
    def set_num(self, set_id):
        assert isinstance(set_id, str)
        self.set_info_list[3], self.set_info_list[4], self.set_info_list[1] = base.expand_set_num(set_id)

    @property
    def bo_id(self):
        """
        @return: The brickowl set id
        """
        return self.set_info_list[2]

    @bo_id.setter
    def bo_id(self, value):
        assert isinstance(value, str) or value is None
        self.set_info_list[2] = value

    @property
    def name(self):
        """
        @return: return the set name
        """
        return self.set_info_list[5]

    @name.setter
    def name(self, name):
        assert isinstance(name, str)
        self.set_info_list[5] = name

    @property
    def theme(self):
        """
        @return: return the set theme
        """
        return self.set_info_list[6]

    @theme.setter
    def theme(self, value):
        assert isinstance(value, str) or value is None
        self.set_info_list[6] = value

    @property
    def subtheme(self):
        """
        @return: return the set subtheme
        """
        return self.set_info_list[7]

    @subtheme.setter
    def subtheme(self, value):
        assert isinstance(value, str) or value is None
        self.set_info_list[7] = value

    @property
    def piece_count(self):
        """
        @return: return the set piece count
        """
        return self.set_info_list[8]

    @piece_count.setter
    def piece_count(self, value):
        assert isinstance(value, int) or value is None
        self.set_info_list[8] = value

    @property
    def figures(self):
        """
        @return: return the set figures count
        """
        return self.set_info_list[9]

    @figures.setter
    def figures(self, value):
        assert isinstance(value, int) or value is None
        self.set_info_list[9] = value

    @property
    def weight(self):
        """
        @return: return the set weight
        """
        return self.set_info_list[10]

    @weight.setter
    def weight(self, value):
        assert isinstance(value, float) or value is None
        self.set_info_list[10] = value

    @property
    def year_released(self):
        return self.set_info_list[11]

    @year_released.setter
    def year_released(self, value):
        assert isinstance(value, int) or value is None
        self.set_info_list[11] = value

    @property
    def ts_date_released_us(self):
        return self.set_info_list[12]

    @ts_date_released_us.setter
    def ts_date_released_us(self, value):
        assert isinstance(value, int) or value is None
        self.set_info_list[12] = value

    @property
    def date_released_us(self):
        return base.get_date(self.set_info_list[12])

    @date_released_us.setter
    def date_released_us(self, value):
        """ @param value: In the format YYYY-MM-DD"""
        assert isinstance(value, str) or value is None
        self.set_info_list[12] = base.get_timestamp(value)

    @property
    def ts_date_ended_us(self):
        return self.set_info_list[13]

    @ts_date_ended_us.setter
    def ts_date_ended_us(self, value):
        assert isinstance(value, int) or value is None
        self.set_info_list[13] = value

    @property
    def date_ended_us(self):
        return base.get_date(self.set_info_list[13])

    @date_ended_us.setter
    def date_ended_us(self, value):
        """ @param value: In the format YYYY-MM-DD"""
        assert isinstance(value, str) or value is None
        self.set_info_list[13] = base.get_timestamp(value)

    @property
    def ts_date_released_uk(self):
        return self.set_info_list[14]

    @ts_date_released_uk.setter
    def ts_date_released_uk(self, value):
        assert isinstance(value, int) or value is None
        self.set_info_list[14] = value

    @property
    def date_released_uk(self):
        return base.get_date(self.set_info_list[14])

    @date_released_uk.setter
    def date_released_uk(self, value):
        """ @param value: In the format YYYY-MM-DD"""
        assert isinstance(value, str) or value is None
        self.set_info_list[14] = base.get_timestamp(value)

    @property
    def ts_date_ended_uk(self):
        return self.set_info_list[15]

    @ts_date_ended_uk.setter
    def ts_date_ended_uk(self, value):
        assert isinstance(value, int) or value is None
        self.set_info_list[15] = value

    @property
    def date_ended_uk(self):
        return base.get_date(self.set_info_list[15])

    @date_ended_uk.setter
    def date_ended_uk(self, value):
        """ @param value: In the format YYYY-MM-DD"""
        assert isinstance(value, str) or value is None
        self.set_info_list[15] = base.get_timestamp(value)

    @property
    def original_price_us(self):
        return self.set_info_list[16]

    @original_price_us.setter
    def original_price_us(self, value):
        assert isinstance(value, float) or value is None
        self.set_info_list[16] = value

    @property
    def original_price_uk(self):
        return self.set_info_list[17]

    @original_price_uk.setter
    def original_price_uk(self, value):
        assert isinstance(value, float) or value is None
        self.set_info_list[17] = value

    @property
    def age_low(self):
        return self.set_info_list[18]

    @age_low.setter
    def age_low(self, value):
        assert isinstance(value, int) or value is None
        self.set_info_list[18] = value

    @property
    def age_high(self):
        return self.set_info_list[19]

    @age_high.setter
    def age_high(self, value):
        assert isinstance(value, int) or value is None
        self.set_info_list[19] = value

    @property
    def box_size(self):
        return self.set_info_list[20]

    @box_size.setter
    def box_size(self, value):
        assert isinstance(value, str) or value is None
        self.set_info_list[20] = value
        self.__set_box_volume()

    def __set_box_volume(self):
        if self.box_size is not None:
            dims = [int(x) for x in self.box_size.split(',')]
            assert len(dims) == 3
            self.set_info_list[21] = dims[0] * dims[1] * dims[2]

    @property
    def box_volume(self):
        """No setter because it relies on box_size"""
        return self.set_info_list[21]

    @property
    def ts_last_updated(self):
        return self.set_info_list[22]

    @ts_last_updated.setter
    def ts_last_updated(self, value):
        assert isinstance(value, int) or value is None
        self.set_info_list[22] = value

    @property
    def last_updated(self):
        return base.get_date(self.set_info_list[22])

    @last_updated.setter
    def last_updated(self, value):
        """ @param value: In the format YYYY-MM-DD"""
        assert isinstance(value, str) or value is None
        self.set_info_list[22] = base.get_timestamp(value)

    @property
    def ts_last_inv_updated_bo(self):
        return self.set_info_list[23]

    @ts_last_inv_updated_bo.setter
    def ts_last_inv_updated_bo(self, value):
        assert isinstance(value, int) or value is None
        self.set_info_list[23] = value

    @property
    def last_inv_updated_bo(self):
        return base.get_date(self.set_info_list[23])

    @last_inv_updated_bo.setter
    def last_inv_updated_bo(self, value):
        """ @param value: In the format YYYY-MM-DD"""
        assert isinstance(value, str) or value is None
        self.set_info_list[23] = base.get_timestamp(value)

    @property
    def ts_last_inv_updated_bl(self):
        return self.set_info_list[24]

    @ts_last_inv_updated_bl.setter
    def ts_last_inv_updated_bl(self, value):
        assert isinstance(value, int) or value is None
        self.set_info_list[24] = value

    @property
    def last_inv_updated_bl(self):
        return base.get_date(self.set_info_list[24])

    @last_inv_updated_bl.setter
    def last_inv_updated_bl(self, value):
        """ @param value: In the format YYYY-MM-DD"""
        assert isinstance(value, str) or value is None
        self.set_info_list[24] = base.get_timestamp(value)

    @property
    def ts_last_inv_updated_re(self):
        return self.set_info_list[25]

    @ts_last_inv_updated_re.setter
    def ts_last_inv_updated_re(self, value):
        assert isinstance(value, int) or value is None
        self.set_info_list[25] = value

    @property
    def last_inv_updated_re(self):
        return base.get_date(self.set_info_list[25])

    @last_inv_updated_re.setter
    def last_inv_updated_re(self, value):
        """ @param value: In the format YYYY-MM-DD"""
        assert isinstance(value, str) or value is None
        self.set_info_list[25] = base.get_timestamp(value)

    @property
    def ts_last_daily_update(self):
        return self.set_info_list[26]

    @ts_last_daily_update.setter
    def ts_last_daily_update(self, value):
        assert isinstance(value, int) or value is None
        self.set_info_list[26] = value

    @property
    def last_daily_update(self):
        return base.get_date(self.set_info_list[26])

    @last_daily_update.setter
    def last_daily_update(self, value):
        """ @param value: In the format YYYY-MM-DD"""
        assert isinstance(value, str) or value is None
        self.set_info_list[26] = base.get_timestamp(value)

    ####
    ## Calculated Properties
    ####

    ##Price per Piece
    @property
    def ppp(self):
        if self.original_price_us is None or self.piece_count is None:
            return self.__missing_data()
        if self.piece_count is not None and self.piece_count > 0:
            return self.original_price_us / self.piece_count

    @property
    def ppp_uk(self):
        if self.original_price_uk is None or self.piece_count is None:
            return self.__missing_data()
        if self.piece_count is not None and self.piece_count > 0:
            return self.original_price_uk / self.piece_count

    ##Price per Gram
    @property
    def ppg(self):
        if self.original_price_us is None or self.weight is None:
            return self.__missing_data()
        if self.weight is not None and self.weight > 0:
            return self.original_price_us / self.weight

    @property
    def ppg_uk(self):
        if self.original_price_uk is None or self.weight is None:
            return self.__missing_data()
        if self.weight is not None and self.weight > 0:
            return self.original_price_uk / self.weight

    ####
    ##Calculated data
    ###
    def get_price(self, year=None):
        """Only works for US right now, only have US inflation rates"""
        if self.original_price_us is None:
            return self.__missing_data()
        if year is None or year == self.year_released:
            return self.original_price_us
        else:
            price_inflated = (inf.get_inflation_rate(self.year_released,
                                                     year) * self.original_price_us) + self.original_price_us
            return price_inflated


    def get_calc_piece_count(self):
        return info.get_piece_count(self.set_num, 'bricklink')

    def get_calc_unique_pieces(self):
        return info.get_unique_piece_count(self.set_num)

    def get_calc_weight(self):
        return info.get_set_weight(self.set_num, 'bricklink')

    def get_ppp_adj(self, year=None, calc=False):

        piece_count = self.piece_count
        if calc is True:
            piece_count = self.get_calc_piece_count()

        if piece_count is None or self.original_price_us is None:
            return self.__missing_data()

        return self.get_price(year) / piece_count

    def get_ppg_adj(self, year=None, calc=False):
        weight = self.weight
        if calc is True:
            weight = self.get_calc_weight()

        if weight is None or self.original_price_us is None:
            return self.__missing_data()

        return self.get_price(year) / weight

    def get_price_history(self):
        return info.get_historic_prices(set_id=self.db_id)

    def get_historic_price_trends(self, select_filter=None, type="standard", price="standard", date=None,
                                  inflation=None):
        """
        @param select_filter: List:
                            [select statement, where statement, group?] See the end of this doc for examples
        @param type: Options:
                            standard - actual numbers (overrides all others)
                            relative - percent change from beginning date
                            delta - price change *day over day*
        @param price: Options:
                                standard - compare price against historic prices
                            These can only be used with relative and delta [type]
                                original_us - compare price against us original
                                original_uk - compare price against uk original
        @param date: Options:
                            a date to start on
                            start - list prices with start date as the focus
                            end - list prices with end date as the focus
        @param inflation: Options:
                            a year to get inflation based on
                            None - no changes

        All this is done in the lists and not with sql
        @return:
             {data:{year:price,year:price},settings:{price_type:"",type:"",price:"",date:"",inflation:""}}
        """
        if isinstance(select_filter, list) and len(select_filter) >= 2:
            sql_query = self._build_historic_data_sql(*select_filter)
        else:
            return self.get_price_history()

        working_data = self.sql(sql_query)

        base_date = None
        base_price = None
        if type != "standard":
            if date is not None:
                if date is "start":
                    base_date = self.date_released_us
                elif date is "end":
                    base_date = self.date_ended_us
                else:
                    base_date = arrow.get(date)
        if price != "standard":
            if price == "original_us":
                base_price = self.original_price_us
            elif price == "original_uk":
                base_price = self.original_price_uk

        return working_data

    def _build_historic_data_sql(self, select_=None, where_=None, group=True):
        """Takes what we got in the starter filter (either a complete filter string or a dict of filter options
            and returns a built out sql statement
        """
        h_select = "SELECT sets.set_num, historic_prices.record_date"
        if select_ is not None:
            h_select += ", " + select_
        h_joins = " FROM historic_prices JOIN sets ON (sets.id=historic_prices.set_id) JOIN price_types ON (price_types.id=historic_prices.price_type)"
        h_filter = " WHERE sets.set_num='{}'".format(self.set_num)
        if where_ is not None:
            h_filter += " and " + where_
        if group:
            h_filter += " GROUP BY historic_prices.record_date"
        h_end = ";"
        h_sql = h_select + h_joins + h_filter + h_end
        return h_sql






    def get_rating_history(self):
        return info.get_historic_data(set_id=self.db_id)

    ####
    ##House keeping
    ###
    def sql(self, sql_statement):
        """Not safe to have publicly exposed, but very handy for my own personal project"""
        return db.run_sql(sql_statement)

    def push_updates_to_db(self):
        """Push Updates to the database"""
        update_secondary.add_set_data_to_database(self.set_info_list)

    def push(self):
        self.push_updates_to_db()

    def update_from_db(self):
        """Wipe out changes and update with what the database shows"""
        self.set_info_list = info.get_set_info(self.set_num)

    def pull(self):
        self.update_from_db()

    def update_from_web(self):
        """Get set data from the web"""
        update_secondary.add_set_to_database(self.set_num)

    def __repr__(self):
        """The representation of the class"""
        return "{} | {}".format(self.set_num, self.name)

    def __str__(self):
        return "{} | {}".format(self.set_num, self.name)

    def __len__(self):
        return len(self.set_info_list)

    def __getitem__(self, item):
        if item < self.__len__():
            return self.set_info_list[item]

    def __bool__(self):
        if self.set_num is None or self.name is None:
            return False
        return True

    def __missing_data(self):
        return None

    # For testing
    def test_base_info(self):
        base_text_string = "\n#### Set Info Class - Test Base Info\n"
        base_text_string += "Database ID: {0}\n".format(self.db_id)
        base_text_string += "Set: {} | {}\n".format(self.set_num, self.name)
        base_text_string += "Theme: {} - {}\n".format(self.theme, self.subtheme)
        base_text_string += "Ages: {} to {}\n".format(self.age_low, self.age_high)
        base_text_string += "Released US: {} - From {} to {}\n".format(self.year_released, self.date_released_us,
                                                                       self.date_ended_us)
        base_text_string += "Released UK: {} - From {} to {}\n".format(self.year_released, self.date_released_uk,
                                                                       self.date_ended_uk)
        base_text_string += "Pieces/Figures: {} / {}\n".format(self.piece_count, self.figures)
        base_text_string += "Weight: {}\n".format(self.weight)
        base_text_string += "Price: {} USD / {} GBP\n".format(self.original_price_us, self.original_price_uk)
        base_text_string += "Box Size: {} - Box Volume {}\n".format(self.box_size, self.box_volume)
        base_text_string += "Last Updated: {}\n".format(self.last_updated)
        base_text_string += "Inventory Last Updated: BL {} / RE {}\n".format(self.last_inv_updated_bl,
                                                                             self.last_inv_updated_re)
        base_text_string += "Daily Last Updated: {}\n".format(self.last_daily_update)
        return base_text_string

    def test_basic_calcs(self):
        base_text_string = "#### Set Info Class - Test Basic Calcs\n"
        base_text_string += "### Database ID {0}\n".format(self.db_id)
        base_text_string += "Set: {} | {}\n".format(self.set_num, self.name)
        base_text_string += "PPP: {} | PPP UK: {}\n".format(self.ppp, self.ppp_uk)
        base_text_string += "PPG: {} | PPG UK: {}\n".format(self.ppg, self.ppg_uk)
        return base_text_string

    def test_inflation(self):
        if self.year_released is None:
            inf_year = 5
        else:
            inf_year = self.year_released + 5
        base_text_string = "#### Set Info Class - Test Inflation Calcs {} -> {}\n".format(self.year_released, inf_year)
        base_text_string += "### Database ID {0}\n".format(self.db_id)
        base_text_string += "Set: {} | {}\n".format(self.set_num, self.name)
        base_text_string += "Price: {} | Adjusted: {}\n".format(self.get_price(), self.get_price(inf_year))
        base_text_string += "PPP: {} | Adjusted: {}\n".format(self.get_ppp_adj(), self.get_ppp_adj(inf_year))
        base_text_string += "PPG: {} | Adjusted: {}\n".format(self.get_ppg_adj(), self.get_ppg_adj(inf_year))
        return base_text_string

    def test_sql_data(self):
        base_text_string = "#### Set Info Class - Test SQL Data\n"
        base_text_string += "### Database ID {0}\n".format(self.db_id)
        base_text_string += "Set: {} | {}\n".format(self.set_num, self.name)
        base_text_string += "Piece Count: {} | Calc {} | Unique: {}\n".format(self.piece_count,
                                                                              self.get_calc_piece_count(),
                                                                              self.get_calc_unique_pieces())
        base_text_string += "Weight: {} | Calc {}\n".format(self.weight, self.get_calc_weight())
        base_text_string += "PPP Count Adj {}\n".format(self.get_ppp_adj(calc=True))
        base_text_string += "PPG Count Adj {}\n".format(self.get_ppg_adj(calc=True))
        return base_text_string

    def test_historic(self):
        return self.get_price_history(), self.get_rating_history()


if __name__ == "__main__":
    test_set = SetInfo()

    def main_menu():
        """
        Main launch menu
        @return:
        """
        logger.critical("Set Info testing")

        options = {}

        options['1'] = "Create Set from DB", menu_create_set_db
        options['2'] = "Create Set from List", menu_create_set_lst
        options['3'] = "Test Base Info", menu_get_base_info
        options['4'] = "Test Basic Calcs", menu_get_basic_calcs
        options['5'] = "Test Inflation", menu_test_inflation
        options['6'] = "Test SQL Data", menu_test_sql_data
        options['7'] = "Test Historic", menu_test_historic
        options['8'] = "Test all Output", menu_test_all_output
        options['S'] = "Test SQL Historic", menu_test_sql_historic
        options['9'] = "Quit", menu.quit

        while True:
            print("Current Set: {}".format(test_set.set_num))
            result = menu.options_menu(options)
            if result is 'kill':
                exit()


    def menu_create_set_db():
        global test_set
        set_num = base.input_set_num()
        test_set = SetInfo(set_num)

    def menu_create_set_lst():
        global test_set
        set_num = base.input_set_num()
        set_info_list = info.get_set_info(set_num)
        test_set = SetInfo(set_info_list)

    def menu_get_base_info():
        global test_set
        while not bool(test_set):
            menu_create_set_db()
        print(test_set)

    def menu_get_basic_calcs():
        global test_set
        while not bool(test_set):
            menu_create_set_db()
        print(test_set.test_basic_calcs())

    def menu_test_inflation():
        global test_set
        while not bool(test_set):
            menu_create_set_db()
        print(test_set.test_inflation())

    def menu_test_sql_data():
        global test_set
        while not bool(test_set):
            menu_create_set_db()
        print(test_set.test_sql_data())

    def menu_test_historic():
        global test_set
        while not bool(test_set):
            menu_create_set_db()
        price_history, rating_history = test_set.test_historic()
        print("Price History")
        base.print4(price_history)
        print("Rating History")
        base.print4(rating_history)

    def menu_test_all_output():
        global test_set
        while not bool(test_set):
            menu_create_set_db()
        menu_get_base_info()
        menu_get_basic_calcs()
        menu_test_inflation()
        menu_test_sql_data()
        menu_test_historic()

    def menu_test_sql_historic():
        global test_set
        while not bool(test_set):
            menu_create_set_db()
        c_result = test_set.get_historic_price_trends()
        base.print4(c_result, 5)
        c_result = test_set.get_historic_price_trends(
            select_filter=["(historic_prices.min+historic_prices.max)/2", None, False])
        base.print4(c_result, 5)
        c_result = test_set.get_historic_price_trends(select_filter=["(historic_prices.min+historic_prices.max)",
                                                                     "(price_types.price_type='historic_used' OR price_types.price_type='historic_new')",
                                                                     False])
        base.print4(c_result, 5)
        c_result = test_set.get_historic_price_trends(select_filter=["SUM(historic_prices.min+historic_prices.max)",
                                                                     "(price_types.price_type='historic_used' OR price_types.price_type='historic_new')",
                                                                     True])
        base.print4(c_result, 5)


    if __name__ == "__main__":
        main_menu()


# Historic SQL Exmples
# BASE
# SELECT sets.set_num, historic_prices.record_date, price_types.price_type,
# historic_prices.lots, historic_prices.qty, historic_prices.min, historic_prices.max,
#   historic_prices.avg, historic_prices.qty_avg, historic_prices.piece_avg
# FROM historic_prices
#   JOIN sets ON (sets.id=historic_prices.set_id)
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
