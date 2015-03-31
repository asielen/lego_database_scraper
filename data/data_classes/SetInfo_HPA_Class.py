# External
import copy
import collections
import random

import arrow





# Internal
# from data import update_secondary
import database.database_support as db
import system as syt


class SetInfo(object):
    """
    Used to query an individual set information
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
                # If setup with a list
                if len(set_info) == 27:
                    set_info_list = list(set_info)
                elif len(set_info) > 2 and isinstance(set_info[1], str):
                    # If the list is the wrong size, it still trys to find a set_num
                    s_num = SetInfo.expand_set_num(set_info[1])[2]
            else:
                if isinstance(set_info, str):
                    # If setup with a string
                    s_num = SetInfo.expand_set_num(set_info)[2]

        if s_num is not None:
            # Todo: Cant add set with this function here because it causes a circular import
            set_info_list = SetInfo.get_set_info(set_info)  # , new=True)

        if set_info_list is None:
            self.set_info_list = [None] * 27  # New Empty Set
            if s_num is not None:
                self.set_info_list[1] = s_num
        else:
            self.set_info_list = set_info_list

    @staticmethod
    def get_set_info(set_num, new=False):
        """
        @param set_num:
        @return: the id column num of the set in the database
        """

        set_info_raw = db.run_sql('SELECT * FROM sets WHERE set_num=?', (set_num.lower(),), one=True)

        # Circular import
        # if set_id_raw is None and new is True: #If there is no data, try to add it
        # add_set_to_database(set_num)
        # set_id_raw = get_set_info(set_num)

        return set_info_raw

    @staticmethod
    def get_set_id(set_num=None):
        """
        @param set_num:
        @return: the id column num of the set in the database, or a list of all set ids with set num if no set num is provided
        """
        if set_num is None:
            set_id_raw = db.run_sql('SELECT set_num, id FROM sets')
        else:
            set_id_raw = db.run_sql('SELECT id FROM sets WHERE set_num=?', (set_num.lower(),), one=True)
            # if set_id_raw is not None:
            # set_id_raw = set_id_raw[0]

        return set_id_raw

    @staticmethod
    def get_random():
        """

        @return: Get a random set from the database (for testing)
        """
        set_list = db.run_sql('SELECT set_num FROM sets')
        return random.choice(set_list)[0]

    @staticmethod
    def input_set_num(type=0):
        """
        @param type: 0 or 1
        @return: if type == 1 xxxx, y, xxxx-y
        @return: else return xxxx-y
        """
        set_num = input("What set num? ")
        if set_num == "rand":
            set_num = SetInfo.get_random()
            print("Random Set: {}".format(set_num))
        if type == 1:
            return SetInfo.expand_set_num(set_num)
        else:
            return SetInfo.expand_set_num(set_num)[2]

    @staticmethod
    def expand_set_num(set_id):
        """

        @param set_id: in standard format xxxx-yy
        @return: xxxx, yy, xxxx-yy
        """

        set_id = set_id.lower()
        try:
            if ' or ' in set_id:
                set_id = set_id.split(' or ')[0]
            set_list = set_id.split("-")
            if len(set_list) > 2: return (None, None, set_id)
            set_num = set_list[0]
            set_seq = set_list[1]
        except:
            set_num = set_id
            set_seq = '1'
        return set_num, set_seq, set_num + '-' + set_seq

    # ###
    # # Basic Properties
    # ###
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
        self.set_info_list[3], self.set_info_list[4], self.set_info_list[1] = SetInfo.expand_set_num(set_id)

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
        @return: return the set get_figures count
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
        return syt.get_date(self.set_info_list[12])

    @date_released_us.setter
    def date_released_us(self, value):
        """ @param value: In the format YYYY-MM-DD"""
        assert isinstance(value, str) or value is None
        self.set_info_list[12] = syt.get_timestamp(value)

    @property
    def ts_date_ended_us(self):
        return self.set_info_list[13]

    @ts_date_ended_us.setter
    def ts_date_ended_us(self, value):
        assert isinstance(value, int) or value is None
        self.set_info_list[13] = value

    @property
    def date_ended_us(self):
        return syt.get_date(self.set_info_list[13])

    @date_ended_us.setter
    def date_ended_us(self, value):
        """ @param value: In the format YYYY-MM-DD"""
        assert isinstance(value, str) or value is None
        self.set_info_list[13] = syt.get_timestamp(value)

    @property
    def ts_date_released_uk(self):
        return self.set_info_list[14]

    @ts_date_released_uk.setter
    def ts_date_released_uk(self, value):
        assert isinstance(value, int) or value is None
        self.set_info_list[14] = value

    @property
    def date_released_uk(self):
        return syt.get_date(self.set_info_list[14])

    @date_released_uk.setter
    def date_released_uk(self, value):
        """ @param value: In the format YYYY-MM-DD"""
        assert isinstance(value, str) or value is None
        self.set_info_list[14] = syt.get_timestamp(value)

    @property
    def ts_date_ended_uk(self):
        return self.set_info_list[15]

    @ts_date_ended_uk.setter
    def ts_date_ended_uk(self, value):
        assert isinstance(value, int) or value is None
        self.set_info_list[15] = value

    @property
    def date_ended_uk(self):
        return syt.get_date(self.set_info_list[15])

    @date_ended_uk.setter
    def date_ended_uk(self, value):
        """ @param value: In the format YYYY-MM-DD"""
        assert isinstance(value, str) or value is None
        self.set_info_list[15] = syt.get_timestamp(value)

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
        return syt.get_date(self.set_info_list[22])

    @last_updated.setter
    def last_updated(self, value):
        """ @param value: In the format YYYY-MM-DD"""
        assert isinstance(value, str) or value is None
        self.set_info_list[22] = syt.get_timestamp(value)

    @property
    def ts_last_inv_updated_bo(self):
        return self.set_info_list[23]

    @ts_last_inv_updated_bo.setter
    def ts_last_inv_updated_bo(self, value):
        assert isinstance(value, int) or value is None
        self.set_info_list[23] = value

    @property
    def last_inv_updated_bo(self):
        return syt.get_date(self.set_info_list[23])

    @last_inv_updated_bo.setter
    def last_inv_updated_bo(self, value):
        """ @param value: In the format YYYY-MM-DD"""
        assert isinstance(value, str) or value is None
        self.set_info_list[23] = syt.get_timestamp(value)

    @property
    def ts_last_inv_updated_bl(self):
        return self.set_info_list[24]

    @ts_last_inv_updated_bl.setter
    def ts_last_inv_updated_bl(self, value):
        assert isinstance(value, int) or value is None
        self.set_info_list[24] = value

    @property
    def last_inv_updated_bl(self):
        return syt.get_date(self.set_info_list[24])

    @last_inv_updated_bl.setter
    def last_inv_updated_bl(self, value):
        """ @param value: In the format YYYY-MM-DD"""
        assert isinstance(value, str) or value is None
        self.set_info_list[24] = syt.get_timestamp(value)

    @property
    def ts_last_inv_updated_re(self):
        return self.set_info_list[25]

    @ts_last_inv_updated_re.setter
    def ts_last_inv_updated_re(self, value):
        assert isinstance(value, int) or value is None
        self.set_info_list[25] = value

    @property
    def last_inv_updated_re(self):
        return syt.get_date(self.set_info_list[25])

    @last_inv_updated_re.setter
    def last_inv_updated_re(self, value):
        """ @param value: In the format YYYY-MM-DD"""
        assert isinstance(value, str) or value is None
        self.set_info_list[25] = syt.get_timestamp(value)

    @property
    def ts_last_daily_update(self):
        return self.set_info_list[26]

    @ts_last_daily_update.setter
    def ts_last_daily_update(self, value):
        assert isinstance(value, int) or value is None
        self.set_info_list[26] = value

    @property
    def last_daily_update(self):
        return syt.get_date(self.set_info_list[26])

    @last_daily_update.setter
    def last_daily_update(self, value):
        """ @param value: In the format YYYY-MM-DD"""
        assert isinstance(value, str) or value is None
        self.set_info_list[26] = syt.get_timestamp(value)

    # ###
    # # Calculated Properties
    # ###

    # Price per Piece
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

    # Price per Gram
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
            price_inflated = (syt.get_inflation_rate(self.year_released,
                                                     year) * self.original_price_us) + self.original_price_us
            return price_inflated


    def get_calc_piece_count(self):
        """
        Returns the piece count of a set by either getting it straight from the piece count column or by
        calculating it based on inventory

        @return: the number of pieces
        """

        count = db.run_sql("SELECT SUM(bl_inventories.quantity) FROM bl_inventories "
                           " WHERE bl_inventories.set_id=?;", (self.db_id,), one=True)
        return count

    def get_calc_unique_pieces(self):
        """
        Returns the unique piece count of a set by calculating it based on inventory
        """
        # TODO: Make this work with rebrickable inventories
        count = db.run_sql("SELECT COUNT(bl_inventories.quantity) FROM bl_inventories JOIN parts"
                           " ON bl_inventories.piece_id = parts.id"
                           " WHERE bl_inventories.set_id=?;", (self.db_id,), one=True)
        return count

    def get_calc_weight(self):
        """
        Returns the weight of a set by either getting it straight from the set weight column or by
        calculating it based on inventory
        """
        # TODO: Make sure piece weight is being imported correctly
        weight = db.run_sql("SELECT SUM(bl_inventories.quantity * parts.weight) FROM bl_inventories JOIN parts"
                                " ON bl_inventories.piece_id = parts.id"
                                " WHERE bl_inventories.set_id=?;", (self.db_id,), one=True)
        return weight

    def get_avg_piece_weight(self, calc=False):
        if calc is False:
            if self.weight is None or self.piece_count is None or self.piece_count == 0:
                return None
            else:
                return self.weight / self.piece_count
        else:
            calc_weight = self.get_calc_weight()
            calc_piece_count = self.get_calc_piece_count()
            if calc_weight is None or calc_piece_count is None or calc_piece_count == 0:
                return None
            else:
                return self.get_calc_weight() / self.get_calc_piece_count()

    def get_unique_piece_ratio(self):
        unique_pieces = self.get_calc_unique_pieces()
        calc_pieces = self.get_calc_piece_count()
        if unique_pieces is None or calc_pieces is None or calc_pieces == 0:
            return None
        else:
            return self.get_calc_unique_pieces() / self.get_calc_piece_count()

    def get_ppp_adj(self, year=None, calc=False):

        piece_count = self.piece_count
        if calc is True:
            piece_count = self.get_calc_piece_count()

        if piece_count is None or self.original_price_us is None or piece_count == 0:
            return self.__missing_data()

        return self.get_price(year) / piece_count

    def get_ppg_adj(self, year=None, calc=False):
        weight = self.weight
        if calc is True:
            weight = self.get_calc_weight()

        if weight is None or self.original_price_us is None or weight == 0:
            return self.__missing_data()

        return self.get_price(year) / weight


    def _get_rating_history(self, desc=None, select_filter=None):
        self.rating_history = HistoricPriceAnalyser(si=self, desc=desc, select_filter=select_filter, rating=True)
        return self.rating_history

    def get_rating_history_all(self):
        rating_types = ("want", "own", "rating")
        rating_dict = {}
        date_list = None
        for r in rating_types:
            rating_dict[r] = self.get_rating_history(rating_type=r)
            if date_list is None:
                date_list = [n for n in rating_dict[r].working_data]
        return rating_dict, date_list

    def get_rating_history(self, rating_type=""):
        """
        @param rating_type: ("want","own","rating")
        @return:
        """
        if rating_type == "":
            return None
        select_filter = "bs_ratings.{}".format(rating_type)
        where_filter = None
        return self._get_rating_history(desc=filter, select_filter=[select_filter, where_filter, True])

    def _get_price_history(self, desc=None, select_filter=None):
        self.price_history = HistoricPriceAnalyser(si=self, desc=desc, select_filter=select_filter)
        return self.price_history

    def get_price_history_all(self):
        price_types = ("historic_new", "historic_used", "current_new", "current_used")
        fields = ("avg", "lots", "max", "min", "qty", "qty_avg", "piece_avg")
        price_dict = {}
        date_list = None
        for p in price_types:
            for f in fields:
                price_dict["{}.{}".format(p, f)] = self.get_price_history(price_type=p, field=f)
                if date_list is None:
                    date_list = [n for n in price_dict["{}.{}".format(p, f)].working_data]
        return price_dict, date_list

    def get_price_history(self, price_type="", field=""):
        """
        @param price_type: = ("historic_new", "historic_used", "current_new", "current_used")
        @param field: avg / lots / max / min / qty / qty_avg / piece_avg
        @return:
        """
        if price_type == "" or field == "":
            return None
        select_filter = "historic_prices.{}".format(field)
        where_filter = "price_types.price_type = '{}'".format(price_type)
        return self._get_price_history(desc=filter, select_filter=[select_filter, where_filter, False])

    def get_relative_date(self, date, reference_date=None):
        """
        Gets the distance from date to reference date

        @param date: the date to compare
        @param reference_date: the date 0
        @return:
        """
        if syt.check_if_the_same_day(date, reference_date):
            return 0
        else:
            return syt.get_days_between(date, reference_date)


    def get_relative_end_date(self, date):
        """
        Return the position of date to the comparison date (end date in this case)
        @param date:
        @return:
        Simply date - end-date = relative date
        """
        if date is None or self.date_ended_us is None: return None
        dif_date = arrow.get(date) - arrow.get(self.date_ended_us)
        return dif_date.days


    def get_relative_end_date_range(self):
        """
        6/30/14 = 1372550400 # The first possible date in the db
        @return:
        """
        d1 = self.get_date_min(type="end")
        if d1 is not None:
            d1 = -d1
        d2 = self.get_date_max(type="end")
        return d1, d2

    def get_relative_start_date_range(self):
        """
        6/30/14 = 1372550400 # The first possible date in the db
        @return:
        """
        d1 = self.get_date_min(type="start")
        if d1 is not None:
            d1 = -d1
        d2 = self.get_date_max(type="start")
        return d1, d2

    def get_abs_date_range(self):
        """
        The actual start and end dates
        @return:
        """
        d1 = self.get_date_min(type="abs")
        d2 = self.get_date_max(type="abs")
        return d1, d2

    def get_date_min(self, type="end"):
        """

        @param type: start or end
        @return: The number of values it has before the [type] date
        6/30/14 = 1372550400 # The first possible date in the db
        """
        comp_date = self.date_ended_us
        if type == "start":
            comp_date = self.date_released_us
        elif type == "abs":
            return arrow.get(1372550400)
        if comp_date is None: return None
        date_min = arrow.get(comp_date) - arrow.get(1372550400)
        return date_min.days

    def get_date_max(self, type="end"):
        """

        @param type: start or end
        @return: The number of values it has after the [type] date
        6/30/14 = 1372550400 # The first possible date in the db
        """
        comp_date = self.date_ended_us
        if type == "start":
            comp_date = self.date_released_us
        elif type == "abs":
            return arrow.get()
        if comp_date is None: return None
        date_max = arrow.now('US/Pacific') - arrow.get(1372550400)
        date_max = date_max.days
        return date_max - self.get_date_min(type)

    ####
    ##House keeping
    ###
    def sql(self, sql_statement):
        """Not safe to have publicly exposed, but very handy for my own personal project"""
        return db.run_sql(sql_statement)

    # def push_updates_to_db(self):
    #     """Push Updates to the database"""
    #     update_secondary.add_set_data_to_database(self.set_info_list)
    #
    # def push(self):
    #     self.push_updates_to_db()
    #
    # def update_from_db(self):
    #     """Wipe out changes and update with what the database shows"""
    #     self.set_info_list = info.get_set_info(self.set_num)
    #
    # def pull(self):
    #     self.update_from_db()
    #
    # def update_from_web(self):
    #     """Get set data from the web"""
    #     update_secondary.add_set_to_database(self.set_num)

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

    def set_dump(self):
        """
        "id, set_num, set_name, set_theme, get_piece_count, get_figures, set_weight, year_released, date_released_us, date_ended_us,
        date_released_uk, date_ended_uk, original_price_us, original_price_uk, age_low, age_high, box_size, box_volume,
        last_updated, last_inv_updated_bl, last_inv_updated_re, last_daily_update, BASE CALC, get_ppp, ppp_uk, get_ppg, ppg_uk,
        avg_piece_weight,INFLATION, price_inf, ppp_inf, ppg_inf, CALC PIECE/WEIGHT, calc_piece_count, calc_unique_piece_count,
        calc_unique_to_total_piece_count, calc_weight, calc_avg_piece_weight, CALC INFLATION, calc_ppp_inf, calc_ppg_inf\n"
        """
        test_string = ""
        test_string += "{},".format(self.db_id)
        test_string += "{},".format(syt.csv_replace_comma(self.set_num))
        test_string += "{},".format(syt.csv_replace_comma(self.name))
        test_string += "{},".format(syt.csv_replace_comma(self.theme))
        test_string += "{},".format(self.piece_count)
        test_string += "{},".format(self.figures)
        test_string += "{},".format(self.weight)
        test_string += "{},".format(self.year_released)
        test_string += "{},".format(self.date_released_us)
        test_string += "{},".format(self.date_ended_us)
        test_string += "{},".format(self.date_released_uk)
        test_string += "{},".format(self.date_ended_uk)
        test_string += "{},".format(self.original_price_us)
        test_string += "{},".format(self.original_price_uk)
        test_string += "{},".format(self.age_low)
        test_string += "{},".format(self.age_high)
        test_string += "{},".format(syt.csv_replace_comma(self.box_size))
        test_string += "{},".format(self.box_volume)
        test_string += "{},".format(self.last_updated)
        test_string += "{},".format(self.last_inv_updated_bl)
        test_string += "{},".format(self.last_inv_updated_re)
        test_string += "{},".format(self.last_daily_update)
        test_string += "BASE CALC,"
        test_string += "{},".format(self.ppp)
        test_string += "{},".format(self.ppp_uk)
        test_string += "{},".format(self.ppg)
        test_string += "{},".format(self.ppg_uk)
        test_string += "{},".format("WP")  #self.get_avg_piece_weight())
        test_string += "INFLATION,"
        test_string += "{},".format(self.get_price(year=2014))
        test_string += "{},".format(self.get_ppp_adj(year=2014))
        test_string += "{},".format(self.get_ppg_adj(year=2014))
        test_string += "CALC PIECE/WEIGHT,"
        test_string += "{},".format(self.get_calc_piece_count())
        test_string += "{},".format(self.get_calc_unique_pieces())
        test_string += "{},".format("UT")  #self.get_unique_piece_ratio())
        test_string += "{},".format(self.get_calc_weight())
        test_string += "{},".format("WCP")  #self.get_avg_piece_weight(calc=True))
        test_string += "CALC INFLATION,"
        test_string += "{},".format(self.get_ppp_adj(year=2014, calc=True))
        test_string += "{},".format(self.get_ppg_adj(year=2014, calc=True))
        test_string += "\n"
        return test_string

    def set_report(self):
        """
        "id, set_num, set_name, set_theme, get_piece_count, get_figures, set_weight, year_released, date_released_us, date_ended_us,
        date_released_uk, date_ended_uk, original_price_us, original_price_uk, age_low, age_high, box_size, box_volume,
        last_updated, last_inv_updated_bl, last_inv_updated_re, last_daily_update, BASE CALC, get_ppp, ppp_uk, get_ppg, ppg_uk,
        avg_piece_weight,INFLATION, price_inf, ppp_inf, ppg_inf, CALC PIECE/WEIGHT, calc_piece_count, calc_unique_piece_count,
        calc_unique_to_total_piece_count, calc_weight, calc_avg_piece_weight, CALC INFLATION, calc_ppp_inf, calc_ppg_inf\n"
        """
        syt.log_info("Building CSV")
        csv_string = ""
        csv_string += "Set Report, {}, {},\n".format(syt.csv_replace_comma(self.set_num),
                                                     syt.csv_replace_comma(self.name))
        csv_string += "Database ID, {},\n".format(self.db_id)
        csv_string += "\n"
        csv_string += "Basic Info,\n"
        csv_string += "Set Num, {},\n".format(syt.csv_replace_comma(self.set_num))
        csv_string += "Set Name, {},\n".format(syt.csv_replace_comma(self.name))
        csv_string += "Theme, {},\n".format(syt.csv_replace_comma(self.theme))
        csv_string += "Piece Count, {},\n".format(self.piece_count)
        csv_string += "Figures, {},\n".format(self.figures)
        csv_string += "Set Weight, {},\n".format(self.weight)
        csv_string += "Year Released, {},\n".format(self.year_released)
        csv_string += "US Availability, {}, {}, {},Days,\n".format(self.date_released_us, self.date_ended_us,
                                                                   syt.get_days_between(self.date_ended_us,
                                                                                        self.date_released_us))
        csv_string += "US Price, {},\n".format(self.original_price_us)
        csv_string += "UK Availability, {}, {}, {},Days,\n".format(self.date_released_uk, self.date_ended_uk,
                                                                   syt.get_days_between(self.date_ended_uk,
                                                                                        self.date_released_uk))
        csv_string += "UK Price, {},\n".format(self.original_price_uk)
        csv_string += "Age Range, {}, {},\n".format(self.age_low, self.age_high)
        csv_string += "Box Dimensions, {},\n".format(syt.csv_replace_comma(self.box_size))
        csv_string += "Box Volume, {},\n".format(self.box_volume)
        csv_string += "\n"
        csv_string += "Last Updated,\n"
        csv_string += "Last Inventory Updated BL, {},\n".format(self.last_inv_updated_bl)
        csv_string += "Last Inventory Updated BO, {},\n".format(self.last_inv_updated_bo)
        csv_string += "Last Inventory Updated RE, {},\n".format(self.last_inv_updated_re)
        csv_string += "Last Price Updated, {},\n".format(self.last_daily_update)
        csv_string += "\n"
        csv_string += "Calculated Date,\n"
        csv_string += "Calc Piece Count, {},\n".format(self.get_calc_piece_count())
        csv_string += "Calc Unique Pieces, {}, {},\n".format(self.get_calc_unique_pieces(), self.get_unique_piece_ratio())
        csv_string += "Calc Weight, {},\n".format(self.get_calc_weight())
        csv_string += "Price Adj for Inflation, {},\n".format(self.get_price(year=2014))
        csv_string += "Price per Piece, {}, {},\n".format(self.ppp, self.get_ppp_adj(calc=True))
        csv_string += "Price per Piece Adj for Inflation, {}, {},\n".format(self.get_ppp_adj(year=2015), self.get_ppp_adj(year=2015, calc=True))
        csv_string += "Price per Gram, {}, {},\n".format(self.ppg, self.get_ppg_adj(calc=True))
        csv_string += "Price per Gram Adj for Inflation, {}, {},\n".format(self.get_ppg_adj(year=2015), self.get_ppg_adj(year=2015, calc=True))
        csv_string += "\n"
        csv_string += "\n"
        csv_string += "Historic Data,,,,,,6 Month New Prices,,,,,,,,6 Month Used Prices,,,,,,,,Current New Prices,,,,,,,,Current Used Prices,\n"
        csv_string += "Note,Date,Want,Own,Rating,,6 Month New - Lots,6 Month New - QTY,6 Month New - MIN,6 Month New - MAX,6 Month New - AVG,6 Month New - QTY AVG,6 Month New - Piece AVG,,6 Month Used - Lots,6 Month Used - QTY,6 Month Used - MIN,6 Month Used - MAX,6 Month Used - AVG,6 Month Used - QTY AVG,6 Month Used - Piece AVG,,Current New - Lots,Current New - QTY,Current New - MIN,Current New - MAX,Current New - AVG,Current New - QTY AVG,Current New - Piece AVG,,Current Used - Lots,Current Used - QTY,Current Used - MIN,Current Used - MAX,Current Used - AVG,Current Used - QTY AVG,Current Used - Piece AVG,\n"
        syt.log_info("Getting Historic Prices")
        hpd, date_list = self.get_price_history_all()
        hrd, _ = self.get_rating_history_all()
        date_list = sorted(date_list)

        for date in date_list:
            note = ""
            if syt.check_if_the_same_day(date, self.date_released_us):
                note = "Released-US"
            elif syt.check_if_the_same_day(date, self.date_ended_us):
                note = "Ended-US"
            # Notes
            csv_string += "{},{},".format(note, syt.get_date(date))
            # Ratings (Want own rating)
            csv_string += "{},{},{},,".format(hrd["want"].working_data[date], hrd["own"].working_data[date],
                                              hrd["rating"].working_data[date])
            # Historic New
            csv_string += "{},{},{},{},{},{},{},,".format(hpd["historic_new.lots"].working_data[date],
                                                          hpd["historic_new.qty"].working_data[date],
                                                          hpd["historic_new.min"].working_data[date],
                                                          hpd["historic_new.max"].working_data[date],
                                                          hpd["historic_new.avg"].working_data[date],
                                                          hpd["historic_new.qty_avg"].working_data[date],
                                                          hpd["historic_new.piece_avg"].working_data[date])
            # Historic Used
            csv_string += "{},{},{},{},{},{},{},,".format(hpd["historic_used.lots"].working_data[date],
                                                          hpd["historic_used.qty"].working_data[date],
                                                          hpd["historic_used.min"].working_data[date],
                                                          hpd["historic_used.max"].working_data[date],
                                                          hpd["historic_used.avg"].working_data[date],
                                                          hpd["historic_used.qty_avg"].working_data[date],
                                                          hpd["historic_used.qty_avg"].working_data[date])
            # Current New
            csv_string += "{},{},{},{},{},{},{},,".format(hpd["current_new.lots"].working_data[date],
                                                          hpd["current_new.qty"].working_data[date],
                                                          hpd["current_new.min"].working_data[date],
                                                          hpd["current_new.max"].working_data[date],
                                                          hpd["current_new.avg"].working_data[date],
                                                          hpd["current_new.qty_avg"].working_data[date],
                                                          hpd["current_new.qty_avg"].working_data[date])
            # Current Used
            csv_string += "{},{},{},{},{},{},{},\n".format(hpd["current_used.lots"].working_data[date],
                                                           hpd["current_used.qty"].working_data[date],
                                                           hpd["current_used.min"].working_data[date],
                                                           hpd["current_used.max"].working_data[date],
                                                           hpd["current_used.avg"].working_data[date],
                                                           hpd["current_used.qty_avg"].working_data[date],
                                                           hpd["current_used.qty_avg"].working_data[date])
        syt.log_info('Building: {}-{}-set-report.csv'.format(syt.get_timestamp(), self.set_num))
        with open('{}-{}-set-report.csv'.format(syt.get_timestamp(), self.set_num), "w") as f:
            f.write(csv_string)


    # For Quick output
    def debug_dump_all(self):
        dump_string = self.debug_dump_base_info()
        dump_string += self.debug_dump_basic_calcs()
        dump_string += self.debug_dump_inflation()
        dump_string += self.debug_dump_sql_data()
        return dump_string

    def debug_dump_base_info(self):
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

    def debug_dump_basic_calcs(self):
        base_text_string = "#### Set Info Class - Test Basic Calcs\n"
        base_text_string += "### Database ID {0}\n".format(self.db_id)
        base_text_string += "Set: {} | {}\n".format(self.set_num, self.name)
        base_text_string += "PPP: {} | PPP UK: {}\n".format(self.ppp, self.ppp_uk)
        base_text_string += "PPG: {} | PPG UK: {}\n".format(self.ppg, self.ppg_uk)
        return base_text_string

    def debug_dump_inflation(self):
        if self.year_released is not None:
            inf_year = min(self.year_released + 10, 2015)
        else:
            inf_year = 2015

        base_text_string = "#### Set Info Class - Test Inflation Calcs {} -> {}\n".format(self.year_released, inf_year)
        base_text_string += "### Database ID {0}\n".format(self.db_id)
        base_text_string += "Set: {} | {}\n".format(self.set_num, self.name)
        base_text_string += "Price: {} | Adjusted: {}\n".format(self.get_price(), self.get_price(inf_year))
        base_text_string += "PPP: {} | Adjusted: {}\n".format(self.get_ppp_adj(), self.get_ppp_adj(inf_year))
        base_text_string += "PPG: {} | Adjusted: {}\n".format(self.get_ppg_adj(), self.get_ppg_adj(inf_year))
        return base_text_string

    def debug_dump_sql_data(self):
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

    def debug_dump_historic(self):
        return self.get_price_history_all(), self.get_rating_history_all()


class HistoricPriceAnalyser(object):
    """
        This class basically acts as a pre-made sql query. In essence it just stores a sql string that is modified for
            whatever report you need.

        @NOTE: it only works on one price type at a time.@ - But it can do aggregate prices/ratings
    """
    # Price types
    STANDARD = 0
    RELATIVE = 1
    RELATIVE_DAY = 2
    DELTA = 3
    DELTA_DAY = 4

    # Relative to
    R_NOT_RELATIVE = 0
    R_RETAIL_PRICE = 1
    R_START_PRICE = R_START_DATE = 2
    R_END_PRICE = R_END_DATE = 3

    def __init__(self, si=None, desc=None, select_filter=None, rating=False):

        """
            @param desc: A short description of the filter
            @param select_filter: List:
                [select statement, where statement, group?] See the end of this doc for examples
                - This can also be in a dictionary format or None and it will prompt to make it
                NOTE, filters have to return a list in the format [(date,price),(date,price)] (Only one price type at a time)
        """
        self.si = si  # the parent set. If none is provided, it doesn't create one until it is needed
        self.rating = rating  # If this is true, we are working with ratings not prices, so options like relative pricing is ignored


        # The following two if statements create a list that can be used by _build_report_data_sql to make the sql text
        if select_filter is None:
            # If no select filter is provided, ask to make one
            select_filter = HistoricPriceAnalyser.build_filter(True)
            print(select_filter)
        if isinstance(select_filter, dict):
            select_filter = HistoricPriceAnalyser.make_filter(select_filter)
        # Make the sql filter
        sql_query = None
        if isinstance(select_filter, list) and len(select_filter) >= 2:
            sql_query = self._build_report_data_sql(*select_filter)
        else:
            sql_query = self._build_report_data_sql()
        self.sql_query = sql_query
        self.select_filter = select_filter
        sql_result = self.sql(sql_query)
        if sql_result is not None and len(sql_result):
            clean_dict = False
            while clean_dict is False:
                base_dict = syt.list_to_dict(self._process_date_price_list(sql_result))
                sql_result = self.sql(sql_query)
                if "rerun" not in base_dict: clean_dict = True

            # Store the results of the original query so we can restore it later
            self.original_data = syt.OrderedDictV2(sorted(base_dict.items(), key=lambda t: t[0]))
            #   Store the sql so we can work it later, or rebuild it if needed
            self.sql_query = sql_query
            # Same as clear - but needs to be defined in __init__ (set the working data = to the original data)
            self.clear()
            # self.working_data = copy.deepcopy(self.original_data)
            #
            # # Working_data_format:
            # self.base_date = None #min(self.original_data.keys())  # The earliest date
            # self.base_price = None #self.original_data[self.base_date]  # The price at the earliest date
            # self.type = self.STANDARD
            # self.inf_year = None
        else:
            raise SyntaxError("Invalid HPA Formation")

        if desc is not None:
            self.desc = desc
        else:
            self.desc = self.sql_query


    def __bool__(self):
        return bool(self.si)

    def _process_date_price_list(self, dp_list):
        """
        Takes a list of dates and get_prices and fills in the missing dates and extrapolates the get_prices
        @param dp_list: In this format [(date,price),(date,price))]
        @return:
        """
        dp_list.sort(key=lambda x: x[0])  # Sort the list by date
        dp_list_to_add = []  # date, price combos that need to be added
        DAY = 86400  # (60 * 60 * 24)  # Number of seconds in a day: 86400

        # If the list is longer than this, it returned a query with too many get_prices, only one at a time.
        #       May consider expanding this to multiple types at a time
        assert len(dp_list[0]) == 2
        for idx, dp in enumerate(dp_list):
            if idx == 0:
                continue
            days_between = abs(syt.get_days_between(dp_list[idx][0], dp_list[idx - 1][0]))
            if days_between == 1:
                continue
            elif days_between == 0:
                syt.log_error("Days between two dates is zero.")
                syt.log.error("  {}  –   {}".format(arrow.get(dp_list[idx][0]).date(), arrow.get(dp_list[idx - 1][0]).date()))
                delete_sql = self.convert_select_to_delete(dp_list[idx][0])
                print("sql string: " + delete_sql)
                delete_dup = input("Delete the duplicate date? (y/n) ")
                if delete_dup is "y":
                    db.run_sql(delete_sql)
                    return [["rerun", None]]
                else:
                    raise ZeroDivisionError
            else:
                current_price = dp_list[idx][1]
                previous_price = dp_list[idx - 1][1]
                increment = 0
                # If the start and end prices are None, make the inbetween prices None
                # print(days_between)
                price_is_none = False
                if current_price is None and previous_price is None:
                    price_is_none = True

                    #   If a previous price exists but a current price doesn't, then guess prices
                    #   If a current price exists but a previous price doesn't, don't guess if more than 35 days
                elif current_price is None:
                    pass  # current price isn't used so no need to do anything since increment will still be zero
                elif previous_price is None:
                    if days_between > 35:
                        price_is_none = True
                        print("None")
                    else:
                        previous_price = current_price

                else:
                    #Get the number of days between (price delta)
                    increment = round((syt.float_zero(current_price) - syt.float_zero(previous_price)) / days_between,
                                      ndigits=2)

                for n in range(1, days_between):
                    if price_is_none is False:
                        dp_list_to_add.append([arrow.get(dp_list[idx - 1][0]).replace(days=+n).timestamp,
                                               round((syt.float_zero(previous_price) + (increment * n)), ndigits=2)])
                    else:
                        dp_list_to_add.append([arrow.get(dp_list[idx - 1][0]).replace(days=+n).timestamp, None])

        dp_list.extend(dp_list_to_add)
        return dp_list

    @property
    def dates(self):
        return self.working_data.keys()

    def convert_select_to_delete(self, record_date):
        """
        Create a sql string to use to delete based on the select string
        @param record_date:
        @return:
        """
        del_sql = " WHERE record_date={} AND set_id in (SELECT id from sets WHERE set_num='{}')".format(record_date,
                                                                                                        self.si.set_num)
        if 'bs_ratings' in self.select_filter[0]:
            del_sql = "DELETE FROM bs_ratings" + del_sql + ";"
        else:
            del_sql = "DELETE FROM historic_prices" + del_sql
            if self.select_filter[1] is not None:
                del_sql += " AND price_type in (SELECT id from price_types WHERE {});".format(self.select_filter[1])
        return del_sql


    def set_options(self, report_type=STANDARD, base_price=None, base_date=None, inf_year=None):
        """
        Set the report options all in one place
        @param report_type: in:
            STANDARD = 0
            RELATIVE = 1
            RELATIVE_DAY = 2
            DELTA = 3
            DELTA_DAY = 4
        @param base_price: in
            R_NOT_RELATIVE = 0
            R_RETAIL_PRICE = 1
            R_START_PRICE = 2
            R_END_PRICE = 3
            price value
        @param base_date:
            R_NOT_RELATIVE = 0
            R_START_DATE = 2
            R_END_DATE = 3
            date value  <- in any date format
        @param inf_year: Year string
        @return: None
        """
        # if options_dict:
        # report_type = options_dict["report_type"]
        #     base_price = options_dict["base_price"]
        #     base_date = options_dict["base_date"]
        #     inf_year = options_dict["inf_year"]
        if inf_year is not None:
            self.set_inflation_year(inf_year)
        if report_type is not None:
            self.set_report_type(report_type)
        if base_price is not None:
            self.set_base_price(price=base_price)
        if base_date is not None:
            self.set_base_date(date=base_date)
        return self

    def set_inflation_year(self, year=None):
        """
        @param year: If none provided, it is set to None
        @return:
        """
        self.inf_year = None
        if isinstance(year, int):
            if 1950 <= year <= arrow.get().year:
                self.inf_year = year

    def set_report_type(self, rtype=None):
        """
        @param rtype: Options:
            standard - actual numbers (overrides all others)
            relative - percent change from start date
            relative_day - percent change from previous day (does not take into account start price)
            delta - price change from start date
            delta_day - price change *day over day*  (does not take into account start price)
        """
        self.type = self.STANDARD
        if rtype in (self.STANDARD, self.RELATIVE, self.RELATIVE_DAY, self.DELTA, self.DELTA_DAY):
            if rtype != self.type:
                self.type = rtype

    def set_base_price(self, price=None, region="us"):
        """
        Sets the price to do all the calculations from. if none then calculations are done against the retail price
        - This has no effect in a standard report, only has effect in relative and delta reports (not day over day reports though)

        @param price: Options:
                R_NOT_RELATIVE = 0 compare price against historic get_prices (influenced by base date)
            These can only be used with relative and delta [type]
                R_RETAIL_PRICE = 1 compare price against us/uk original
                R_START_PRICE = 2
                R_END_PRICE = 3
                price value
        @param region: Options:
                us or uk
        @return:
        """

        if price is None or price == "" or price == self.R_NOT_RELATIVE:
            self.base_price = None

        elif price == self.R_RETAIL_PRICE:
            if region == "uk":
                self.base_price = self.si.original_price_uk
            else:
                self.base_price = self.si.original_price_us
        elif price == self.R_START_PRICE:
            self.base_price = self._get_price_from_date(self.base_date)
        elif price == self.R_END_PRICE:
            self.base_price = self._get_price_from_date(self.base_date)
        else:
            self.price = syt.int_zero(price)

    def set_base_date(self, date=None, region="us"):
        """


        price affects how the prices are calculated
        date affects how the prices line up (where t0 is)

        @param date: Options:
                a date to start on (in format YYYY-MM-DD)
                R_START_DATE = 2 list get_prices with start date as the focus
                R_END_DATE = 3 list get_prices with end date as the focus
                R_NOT_RELATIVE = 0 = None
        @param region: Options:
                us or uk
        """
        # If no date, then we are not shifting the dates at all
        if date is None or date == "" or date == self.R_NOT_RELATIVE:
            self.base_date = None  # Date is not relative

        #   Set the compare date as the start date (or the earlist date)
        elif date == self.R_START_DATE:
            if region == "uk":
                self.base_date = self.si.ts_date_released_uk
            else:
                self.base_date = self.si.ts_date_released_us

            if self.base_date is None or self.base_date == "":
                self.base_date = max(self.original_data.keys())

        #   Set the compare date as the end date
        elif date == self.R_END_DATE:
            if region == "uk":
                self.base_date = self.si.ts_date_ended_uk
            else:
                self.base_date = self.si.ts_date_ended_us
            if self.base_date is None or self.base_date == "":
                self.base_date = None
        else:
            self.base_date = syt.get_timestamp(date)
            self.base_price = self._get_price_from_date(self.base_date)

    def set_base_price_date(self, price=None, date=None, region="us"):
        self.set_base_price(price=price, region=region)
        self.set_base_date(date=date, region=region)

    def clear(self):
        """
        Reverts the working data back to the original state
        @return:
        """
        self.working_data = copy.deepcopy(self.original_data)
        self.base_date = None
        self.base_price = None
        self.type = self.STANDARD
        self.inf_year = None

    def _process_prices(self):
        """

        This updates (calculates the prices) the working_data dict with the new parameters
        This does not modify the dates, that is done in

        STANDARD = 0
        RELATIVE = 1  - %percent change from start date
        RELATIVE_DAY = 2 - %percent change from previous day (does not take into account start price)
        DELTA = 3 - price change from start date
        DELTA_DAY = 4 - price change *day over day*  (does not take into account start price)

        Uses these variables:
        self.type - see above
        self.base_date
        self.base_price
        self.inf_year
        @return:
        """
        new_dict = collections.defaultdict()
        if self.type == self.STANDARD:
            return self.working_data  # standard type no change, Todo, should this clear?

        # Delta simply means the difference from the base price
        elif self.type == self.DELTA:
            for db in self.working_data:
                new_dict[db] = syt.float_zero(self.working_data[db]) - syt.float_zero(self.base_price)

        # Delta simply means the %difference from the base price
        elif self.type == self.RELATIVE:
            for db in self.working_data:
                try:
                    new_dict[db] = (syt.float_zero(self.working_data[db]) / syt.float_zero(self.base_price)) - 1
                except ZeroDivisionError:
                    new_dict[db] = 0

        #   Delta day simply means the difference from the day before, base price doesn't matter
        elif self.type == self.DELTA_DAY:
            for idx, db in enumerate(self.working_data.keys()):
                if idx == 0:
                    new_dict[db] = 0
                    continue
                else:
                    previous_value = self.working_data.previous_key(db)
                    new_dict[db] = syt.float_zero(self.working_data[db]) - syt.float_zero(
                        self.working_data[previous_value])

        #   Delta day simply means the %difference from the day before, base price doesn't matter
        elif self.type == self.RELATIVE_DAY:
            for idx, db in enumerate(self.working_data.keys()):
                if idx == 0:
                    new_dict[db] = 0
                    continue
                else:
                    previous_value = self.working_data.previous_key(db)
                    try:
                        new_dict[db] = round(
                            (syt.float_zero(self.working_data[db]) / self.working_data[previous_value]) - 1, 6)
                    except ZeroDivisionError:
                        new_dict[db] = None
        self.working_data = syt.OrderedDictV2(sorted(new_dict.items(), key=lambda t: t[0]))

        if self.inf_year is not None:
            self.working_data = syt.adj_dict_for_inf(self.working_data, self.inf_year)

        return self.working_data

    def _process_dates(self):
        """
            Take self.base_date and return the working_data with the adjusted dates
        @return:
        """
        if self.base_date is not None:
            self.working_data = syt.OrderedDictV2({self.si.get_relative_date(d, self.base_date): self.working_data[d]
                                                   for d in self.working_data})
        return self.working_data

    def _get_price_from_date(self, date=None):
        """

        @param date: in format YYYY-MM-DD
        @return:
        """
        if date is None: return None
        compare_ts = date  # syt.get_timestamp(date)
        closest_price_date = syt.get_closest_list(compare_ts, self.working_data.keys())
        self.base_date = date
        return self.working_data[closest_price_date]

    def _build_report_data_sql(self, select_=None, where_=None, group=True):
        """Takes what we got in the starter filter (either a complete filter string or a dict of filter options
            and returns a built out sql statement
        """
        h_select = "SELECT historic_prices.record_date"
        if select_ is not None:
            h_select += ", " + select_
        else:
            syt.log_error("Missing filter text")
            return None
            # h_select = "SELECT historic_prices.record_date, price_types.price_type, historic_prices.lots, historic_prices.qty, historic_prices.min, historic_prices.max, historic_prices.avg, historic_prices.qty_avg, historic_prices.piece_avg"
        h_joins = " FROM historic_prices JOIN sets ON (sets.id=historic_prices.set_id) JOIN price_types ON (price_types.id=historic_prices.price_type) JOIN bs_ratings ON (bs_ratings.set_id=historic_prices.set_id AND bs_ratings.record_date=historic_prices.record_date)"
        h_filter = " WHERE sets.set_num='{}'".format(self.si.set_num)
        if where_ is not None:
            h_filter += " AND " + where_
        if group:
            h_filter += " GROUP BY historic_prices.record_date"
        h_end = ";"
        h_sql = h_select + h_joins + h_filter + h_end
        return h_sql

    def sql(self, sql_statement):
        """Not safe to have publicly exposed, but very handy for my own personal project"""
        return db.run_sql(sql_statement)



    def get_set_descs(self, type="dict"):
        """
        Gets basic information for every set in the HPA, basically a nice to have
        @param type:
        @return:
        """
        if type == "list":
            return [self.si.set_num, self.si.theme, self.si.year_released, self.si.original_price_us,
                    self.si.date_released_us, self.si.date_ended_us]
        else:
            return {"set_num": self.si.set_num, "theme": self.si.theme, "date_release": self.si.date_released_us,
                    "original_price": self.si.original_price_us, "base_date": syt.get_date(self.base_date),
                    "base_date_ts": self.base_date, "inflation_year": self.inf_year, "base_price": self.base_price,
                    "report_type": self.type, "records": len(self.working_data)}

    def prepare_report(self):
        """
        Setup the working list based on the current settings (type, inf etc)
        @return:
        """
        self._process_prices()
        self._process_dates()
        return self

    def run_report(self, prepare=True):
        """
        Run the report based on current settings and return two lists that can be turned into csv filed
        @return:
        """
        if prepare: self.prepare_report()
        set_descs = self.get_set_descs(type="list")
        set_prices = self.working_data
        return set_prices, set_descs


    def test_eval_reports(self):
        """
        Returns two lists that can be turned into csv files

        Set List
        Set_num, theme, year_released, original_price, start_date, end_date

        Price List
        set_num, date(price), date(price), date(price), date(price)
        @return:
        set_descs = [["SET_NUM", "THEME", "YEAR_RELEASED", "ORIGINAL_PRICE", "DATE_START", "DATE_END"]]
        """
        set_descs = self.get_set_descs(type="list")
        self.clear()
        set_prices = self.run_all_test(report_types=[1])  # By date will start with the date ended

        return set_prices, set_descs

    def run_all_test(self, report_types=None):
        self.working_data = copy.deepcopy(self.original_data)
        results_dict = collections.defaultdict()
        in_progress = []

        range_types = report_types
        if range_types is None:
            range_types = (self.STANDARD, self.RELATIVE, self.RELATIVE_DAY, self.DELTA, self.DELTA_DAY)

        for n in range_types:
            self.set_options(report_type=n, base_price=self.R_RETAIL_PRICE, base_date=self.R_END_DATE, inf_year=2015)
            self.prepare_report()
            in_progress.append(self.run_report())

        for n in in_progress[0]:
            next_row = []
            for m in range(len(in_progress)):
                next_row.append(in_progress[m][n])
                results_dict[syt.get_ts_day(n)] = next_row

        return results_dict

    ##
    # Static Methods
    ##
    @staticmethod
    def build_report_type():
        """
        -Report Type
            STANDARD = 0
            RELATIVE = 1
            RELATIVE_DAY = 2
            DELTA = 3
            DELTA_DAY = 4
        -Inflation Date
        -Relative Date: (set_base_price_date) - start, end
        -Relative Price: start, end, retail

        @return:
        """

        def _get_report_type(type_text):
            """
            STANDARD = 0
            RELATIVE = 1
            RELATIVE_DAY = 2
            DELTA = 3
            DELTA_DAY = 4
            """
            report_types = {
                "Standard": HistoricPriceAnalyser.STANDARD,
                "Relative": HistoricPriceAnalyser.RELATIVE,
                "Relative Day": HistoricPriceAnalyser.RELATIVE_DAY,
                "Delta": HistoricPriceAnalyser.DELTA,
                "Delta Day": HistoricPriceAnalyser.DELTA_DAY
            }
            return report_types[type_text]

        options = (
            "Standard",
            "Relative",
            "Relative Day",
            "Delta",
            "Delta Day"
        )
        report_type = syt.Menu('- Choose Report Type -', choices=options, function=_get_report_type, type=syt.Menu.LOAD).run()

        def _get_base_price(type_text):
            """
            # Relative to
            R_NOT_RELATIVE = 0
            R_RETAIL_PRICE = 1
            R_START_PRICE = R_START_DATE = 2
            R_END_PRICE = R_END_DATE = 3
            """
            report_types = {
                "None": HistoricPriceAnalyser.R_NOT_RELATIVE,
                "Retail": HistoricPriceAnalyser.R_RETAIL_PRICE,
                "Start Price": HistoricPriceAnalyser.R_START_PRICE,
                "End Price": HistoricPriceAnalyser.R_END_PRICE
            }
            if type_text == "Custom":
                price = input("What custom price would you like to compare to? ")
                return price
            else:
                return report_types[type_text]

        options = (
            "None",
            "Retail",
            "Start Price",
            "End Price",
            "Custom"
        )
        base_price = syt.Menu('- Choose Base Price -', choices=options, function=_get_base_price, type=syt.Menu.LOAD).run()

        def _get_base_date(type_text):
            """
            # Relative to
            R_NOT_RELATIVE = 0
            R_RETAIL_PRICE = 1
            R_START_PRICE = R_START_DATE = 2
            R_END_PRICE = R_END_DATE = 3
            """
            report_types = {
                "None": HistoricPriceAnalyser.R_NOT_RELATIVE,
                "Start Date": HistoricPriceAnalyser.R_START_DATE,
                "End Date": HistoricPriceAnalyser.R_END_Date
            }
            if type_text == "Custom":
                date = input("What custom date would you like to compare to? (yyyy-mm-dd) ")
                return date
            else:
                return report_types[type_text]

        options = (
            "None",
            "Retail",
            "Start Price",
            "End Price",
            "Custom"
        )
        base_date = syt.Menu('- Choose Base Date -', choices=options, function=_get_base_date, type=syt.Menu.LOAD).run()

        inf_year = input("What year do you want to use for inflation (blank for none)? ")
        if inf_year == "":
            inf_year = None

        return report_type, base_price, base_date, inf_year


    @staticmethod
    def build_filter():
        """
        Through a set of menus, this creates the select string for a HPA class
        @return:
        """
        hpa_list = ""

        def hpa_build_rating():
            qstring = ["", None, True]
            options = ["Want", "Own", "Rating", "Want+Own", "Want-Own"]
            choice = syt.Menu("- Create HPA Query Rating -", choices=options, type="return", drop_down=True,
                              quit_tag="Done").run()

            if choice == "Want":
                qstring[0] = "bs_ratings.want"
            elif choice == "Own":
                qstring[0] = "bs_ratings.own"
            elif choice == "Rating":
                qstring[0] = "bs_ratings.rating"
            elif choice == "Want+Own":
                qstring[0] = "(bs_ratings.want + bs_ratings.own)"
            elif choice == "Want-Own":
                qstring[0] = "(bs_ratings.want - bs_ratings.own)"
            else:
                qstring = None

            return qstring

        def hpa_build_price():


            price_types = ["historic_new", "historic_used", "current_new", "current_used"]
            fields = ["avg", "lots", "max", "min", "qty", "qty_avg", "piece_avg"]
            group_functions = ["AVG", "MIN", "MAX", "SUM"]  # For price types
            aggregate_functions = ["AVG", "SUM", "DIFFERENCE"]  # For fields
            c_price_types = []
            c_fields = []
            c_group_function = None
            c_aggregate_function = None

            c_price_types = syt.MultiChoiceMenu(price_types)
            if len(c_price_types) > 1:
                c_group_function = syt.Menu("- Choose group function -", choices=group_functions, drop_down=True,
                                            type=syt.Menu.RETURN).run()
            c_fields = syt.MultiChoiceMenu(fields)
            if len(c_fields) > 1:
                c_aggregate_function = syt.Menu("- Choose aggregate function -", choices=aggregate_functions,
                                                drop_down=True, type=syt.Menu.RETURN).run()

            return {"price_type": c_price_types, "field": c_fields,
                    "group_function": c_group_function, "aggregate_function": c_aggregate_function}


        options = [("Rating", hpa_build_rating),
                   ("Price", hpa_build_price)]
        hpa_list = syt.Menu("- Create HPA Query -", choices=options, drop_down=True).run()
        if hpa_list == 0: hpa_list = None

        return hpa_list

    @staticmethod
    def make_filter(filter_dict=None):
        """
            #For making sql from a dictionary in this format:
            # {'price_types':[], 'fields':[], 'group_function':"", 'aggregate_function':""}
        @param dic:
        @return: a list in the standard format to build a filter sql string
        """
        if isinstance(filter_dict, list):
            return filter_dict

        if len(filter_dict['field']) == 0 and len(filter_dict['price_type']) == 0:
            return None

        sql_string = []

        # validate dict
        if len(filter_dict['field']) > 1 and filter_dict['aggregate_function'] == None:
            raise SyntaxError
        elif len(filter_dict['price_type']) > 1 and filter_dict['group_function'] == None:
            raise SyntaxError

        # Build select string
        aggregate_lookup = {"AVG": "+", "SUM": "+", "DIFFERENCE": "-"}
        select_string = "("
        for idx, field in enumerate(filter_dict['field']):
            if idx > 0:
                select_string += aggregate_lookup[filter_dict['aggregate_function']]
            select_string += "historic_prices.{}".format(field)
        select_string += ")"
        if filter_dict['aggregate_function'] == "AVG":
            select_string += "/{}".format(len(filter_dict['field']) * len(filter_dict['price_type']))

        if filter_dict['group_function'] != None:
            select_string = "{}({})".format(filter_dict['group_function'], select_string)


        #Build Where string
        where_string = "("
        for idx, price_type in enumerate(filter_dict['price_type']):
            if idx > 0:
                where_string += " OR "
            where_string += 'price_types.price_type="{}"'.format(price_type)
        where_string += " )"

        #Add group by true/false
        group_by = False
        if len(filter_dict['price_type']) > 1:
            group_by = True

        return [select_string, where_string, group_by]