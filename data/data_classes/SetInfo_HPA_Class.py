# External
import copy
import collections
import random
import os
import pickle

import arrow






# Internal
# from data import update_secondary
import database.database_support as db
import system as syt


class SetInfo(object):
    """
    Used to query an individual _set information
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
        @return: the id column num of the _set in the database
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
        @return: the id column num of the _set in the database, or a list of all _set ids with _set num if no _set num is provided
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

        @return: Get a random _set from the database (for testing)
        """
        set_list = db.run_sql('SELECT set_num FROM sets')
        return random.choice(set_list)[0]

    @staticmethod
    def input_set_num(type=0):
        """
        @param type: 0 or 1
        @return: if _type == 1 xxxx, y, xxxx-y
        @return: else return xxxx-y
        """
        set_num = input("What set num? ")
        if set_num == "rand" or set_num == "r":
            set_num = SetInfo.get_random()
            syt.log_info("Random Set: {}".format(set_num))
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
        @return: the _set num, _set item num and _set seq
        """
        return self.set_info_list[1]

    @set_num.setter
    def set_num(self, set_id):
        assert isinstance(set_id, str)
        self.set_info_list[3], self.set_info_list[4], self.set_info_list[1] = SetInfo.expand_set_num(set_id)

    @property
    def bo_id(self):
        """
        @return: The brickowl _set id
        """
        return self.set_info_list[2]

    @bo_id.setter
    def bo_id(self, value):
        assert isinstance(value, str) or value is None
        self.set_info_list[2] = value

    @property
    def name(self):
        """
        @return: return the _set name
        """
        return self.set_info_list[5]

    @name.setter
    def name(self, name):
        assert isinstance(name, str)
        self.set_info_list[5] = name

    @property
    def theme(self):
        """
        @return: return the _set theme
        """
        return self.set_info_list[6]

    @theme.setter
    def theme(self, value):
        assert isinstance(value, str) or value is None
        self.set_info_list[6] = value

    @property
    def subtheme(self):
        """
        @return: return the _set subtheme
        """
        return self.set_info_list[7]

    @subtheme.setter
    def subtheme(self, value):
        assert isinstance(value, str) or value is None
        self.set_info_list[7] = value

    @property
    def piece_count(self):
        """
        @return: return the _set piece count
        """
        return self.set_info_list[8]

    @piece_count.setter
    def piece_count(self, value):
        assert isinstance(value, int) or value is None
        self.set_info_list[8] = value

    @property
    def figures(self):
        """
        @return: return the _set get_figures count
        """
        return self.set_info_list[9]

    @figures.setter
    def figures(self, value):
        assert isinstance(value, int) or value is None
        self.set_info_list[9] = value

    @property
    def weight(self):
        """
        @return: return the _set weight
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
        Returns the piece count of a _set by either getting it straight from the piece count column or by
        calculating it based on inventory

        @return: the number of pieces
        """

        count = db.run_sql("SELECT SUM(bl_inventories.quantity) FROM bl_inventories "
                           " WHERE bl_inventories.set_id=?;", (self.db_id,), one=True)
        return count

    def get_calc_unique_pieces(self):
        """
        Returns the unique piece count of a _set by calculating it based on inventory
        """
        # TODO: Make this work with rebrickable inventories
        count = db.run_sql("SELECT COUNT(bl_inventories.quantity) FROM bl_inventories JOIN parts"
                           " ON bl_inventories.piece_id = parts.id"
                           " WHERE bl_inventories.set_id=?;", (self.db_id,), one=True)
        return count

    def get_calc_weight(self):
        """
        Returns the weight of a _set by either getting it straight from the _set weight column or by
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

    def get_rating_history_all(self):
        rating_types = ("want", "own", "rating")
        rating_dict = {}
        date_list = None
        for r in rating_types:
            rating_dict[r] = self.get_rating_history(rating_type=r)
            if date_list is None:
                date_list = rating_dict[r].dates
        return rating_dict, date_list

    def get_rating_history(self, rating_type=""):
        """
        @param rating_type: ("want","own","rating")
        @return:
        """
        if rating_type == "":
            return None
        if rating_type not in ('want', 'own', 'rating'):
            raise ValueError("{} is not a valid rating type".format(rating_type))
        select_filter = "bs_ratings.{}".format(rating_type)
        where_filter = None
        return self._get_rating_history(desc=filter, select_filter=[select_filter, where_filter, True])
    
    def _get_rating_history(self, desc=None, select_filter=None):
        self.rating_history = HistoricPriceAnalyser().create(select_filter=select_filter, si=self, rating=True, run=True)
        self.rating_history.desc = desc
        return self.rating_history


    def get_price_history_all(self):
        price_types = ("historic_new", "historic_used", "current_new", "current_used")
        fields = ("avg", "lots", "max", "min", "qty", "qty_avg", "piece_avg")
        price_dict = {}
        date_list = None
        for p in price_types:
            for f in fields:
                price_dict["{}.{}".format(p, f)] = self.get_price_history(price_type=p, field=f)
                if date_list is None:
                    date_list = price_dict["{}.{}".format(p, f)].dates
        return price_dict, date_list

    def get_price_history(self, price_type="", field=""):
        """
        @param price_type: = ("historic_new", "historic_used", "current_new", "current_used")
        @param field: avg / lots / max / min / qty / qty_avg / piece_avg
        @return:
        """
        if price_type == "" or field == "":
            return None
        if price_type not in ("historic_new", "historic_used", "current_new", "current_used"):
            raise ValueError("{} is not a valid price type".format(price_type))
        if field not in ("avg", "lots", "max", "min", "qty", "qty_avg", "piece_avg"):
            raise ValueError("{} is not a valid field type".format(field))
        
        select_filter = "historic_prices.{}".format(field)
        where_filter = "price_types.price_type = '{}'".format(price_type)
        return self._get_price_history(desc=filter, select_filter=[select_filter, where_filter, False])

    def _get_price_history(self, desc=None, select_filter=None):
        self.price_history = HistoricPriceAnalyser().create(select_filter=select_filter, si=self, run=True)
        self.price_history.desc = desc
        return self.price_history
    
    # Todo, this did the dame thing as a syt function so just using that
    # def get_relative_date(self, date, reference_date=None):
    # """
    #     Gets the distance from date to reference date
    #
    #     @param date: the date to compare
    #     @param reference_date: the date 0
    #     @return:
    #     """
    #     if syt.check_if_the_same_day(date, reference_date):
    #         return 0
    #     else:
    #         return syt.get_days_between(date, reference_date)


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
        @return: The number of values it has before the [_type] date
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
        @return: The number of values it has after the [_type] date
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
    # """Get _set data from the web"""
    #     update_secondary.add_set_to_database(self.set_num)

    def __repr__(self):
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

    def set_dump(self, inf_year=2015):
        """
        Used to create base reports in this format:
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
        test_string += "{},".format(self.get_avg_piece_weight())
        test_string += "INFLATION,"
        test_string += "{},".format(self.get_price(year=inf_year))
        test_string += "{},".format(self.get_ppp_adj(year=inf_year))
        test_string += "{},".format(self.get_ppg_adj(year=inf_year))
        test_string += "CALC PIECE/WEIGHT,"
        test_string += "{},".format(self.get_calc_piece_count())
        test_string += "{},".format(self.get_calc_unique_pieces())
        test_string += "{},".format(self.get_unique_piece_ratio())
        test_string += "{},".format(self.get_calc_weight())
        test_string += "{},".format(self.get_avg_piece_weight(calc=True))
        test_string += "CALC INFLATION,"
        test_string += "{},".format(self.get_ppp_adj(year=inf_year, calc=True))
        test_string += "{},".format(self.get_ppg_adj(year=inf_year, calc=True))
        test_string += "\n"
        return test_string

    def make_set_report(self):
        """
        Creates a csv file of a single _set's info

        """
        # Fields used:
        # "id, set_num, set_name, set_theme, get_piece_count, get_figures, set_weight, year_released, date_released_us, date_ended_us,
        # date_released_uk, date_ended_uk, original_price_us, original_price_uk, age_low, age_high, box_size, box_volume,
        # last_updated, last_inv_updated_bl, last_inv_updated_re, last_daily_update, BASE CALC, get_ppp, ppp_uk, get_ppg, ppg_uk,
        # avg_piece_weight,INFLATION, price_inf, ppp_inf, ppg_inf, CALC PIECE/WEIGHT, calc_piece_count, calc_unique_piece_count,
        # calc_unique_to_total_piece_count, calc_weight, calc_avg_piece_weight, CALC INFLATION, calc_ppp_inf, calc_ppg_inf\n"

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
            csv_string += "{},{},{},,".format(hrd["want"][date], hrd["own"][date],
                                              hrd["rating"][date])
            # Historic New
            csv_string += "{},{},{},{},{},{},{},,".format(hpd["historic_new.lots"][date],
                                                          hpd["historic_new.qty"][date],
                                                          hpd["historic_new.min"][date],
                                                          hpd["historic_new.max"][date],
                                                          hpd["historic_new.avg"][date],
                                                          hpd["historic_new.qty_avg"][date],
                                                          hpd["historic_new.piece_avg"][date])
            # Historic Used
            csv_string += "{},{},{},{},{},{},{},,".format(hpd["historic_used.lots"][date],
                                                          hpd["historic_used.qty"][date],
                                                          hpd["historic_used.min"][date],
                                                          hpd["historic_used.max"][date],
                                                          hpd["historic_used.avg"][date],
                                                          hpd["historic_used.qty_avg"][date],
                                                          hpd["historic_used.qty_avg"][date])
            # Current New
            csv_string += "{},{},{},{},{},{},{},,".format(hpd["current_new.lots"][date],
                                                          hpd["current_new.qty"][date],
                                                          hpd["current_new.min"][date],
                                                          hpd["current_new.max"][date],
                                                          hpd["current_new.avg"][date],
                                                          hpd["current_new.qty_avg"][date],
                                                          hpd["current_new.qty_avg"][date])
            # Current Used
            csv_string += "{},{},{},{},{},{},{},\n".format(hpd["current_used.lots"][date],
                                                           hpd["current_used.qty"][date],
                                                           hpd["current_used.min"][date],
                                                           hpd["current_used.max"][date],
                                                           hpd["current_used.avg"][date],
                                                           hpd["current_used.qty_avg"][date],
                                                           hpd["current_used.qty_avg"][date])
        syt.log_info('Building: {}-{}-_set-report.csv'.format(syt.get_timestamp(), self.set_num))
        file_path = syt.make_dir('resources/SetInfo_Reports/')
        with open(file_path+'{}-{}-_set-report.csv'.format(syt.get_timestamp(), self.set_num), "w") as f:
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
        This class basically acts as a pre-made _sql query. In essence it just stores a _sql string that is modified for
            whatever report you need.

        @NOTE: it only works on one price _type at a time.@ - But it can do aggregate prices/ratings
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

    def __init__(self):
        """
            Just to create the shell of the HPA, nothing is defined here except variable defs
        """
        self.name = None
        self.desc = None

        self._sql_query = None  # SQL Query Text, Todo: Not sure this is needed
        self._select_filter = None  # Used to build the SQL query
        self._rating = False  # True if the HPA is for ratings, false otherwise
        self._working_data = {}  # Current working data
        self._original_data = {}  # Original data, as a backup

        # Report Settings
        #This is used to hold the options until they are ready to be processed (need the set number)
        self._report_options = {"Base Date": None,
                                "Base Price": None,
                                "Type": self.STANDARD,
                                "Inflation Year": None}
        self._base_date = None  # The base date used as "date 0"
        self._base_price = None  # The base price that other prices are evaluated against
        self._type = self.STANDARD  # Evaluation _type
        self._inf_year = None  # Year dates are adjusted for

        self._si = None


    def __bool__(self):
        return bool(self._select_filter)

    def __str__(self):
        return self.name

    def __getitem__(self, item):
        if self._working_data:
            return self._working_data[item]
        else:
            raise AttributeError('Report has not been run yet')
    
    def about(self):
        syt.log_info("{}: {}".format(self.name, self.desc))
        syt.log_info("FILTER: ".format(self._select_filter))
        syt.log_info("REPORT OPTIONS: ".format(self._report_options))
        return self

    @property
    def si(self):
        return self._si

    @si.setter
    def si(self, st):
        if isinstance(st, SetInfo):
            self._si = st
        else:
            self._si = None

    @property
    def dates(self):
        if self._working_data:
            return self._working_data.keys()
        return None

    @staticmethod
    def create(hpa=None, select_filter=None, rating=False, set_options=None, si=None, run=False):
        """
        This can be used as the main 'event loop' when dealing with a report. It allows you to create/load/save an HPA
            Also, it returns an HPA, so if it is called from let's say, Set Collection, class. The _set collection class
            Can then manipulate it.
        @param select_filter:
        @param rating: True or False, is the HPA a _rating HPA
        @param hpa: Can pass through an HPA, to edit
        @return: The HPA
        """

        C_HPA = hpa

        if not isinstance(C_HPA, HistoricPriceAnalyser) and (select_filter is not None):
            # If a set_filter was included, then just build it without any input
            C_HPA = HistoricPriceAnalyser()

            if select_filter is not None:
                C_HPA.set_filter(select_filter, rating)
            if set_options is not None:
                C_HPA.set_options(**set_options)
            if si is not None:
                C_HPA._set(si)
            return C_HPA._create(run=run)

        def _new_hpa():
            return HistoricPriceAnalyser()

        # All of these options should return self
        options = (
            ("New HPA", _new_hpa),
            ("Load HPA", HistoricPriceAnalyser.load)
        )

        C_HPA = syt.Menu("- HPA Option -", options, quit_tag="Back", drop_down=True).run()

        if C_HPA in [None, 0]:
            return None
        return C_HPA._create()

    def _create(self, run=False):

        # All of these options should return self
        if run is True:
            self.run_report()
            return self
        options = (
            ("Change HPA Filter", self.build_filter),
            ("Change HPA Report Type", self.build_report_type),
            ("Test HPA", self.run_all_test),
            ("About HPA", self.about),  # Need this to give a better overview
            ("Save HPA", self.save)
        )

        def menu_title():
            title = "- HPA Option -"
            title += "\n : {}".format(self.name)
            title += "\n : {}".format(self.desc)
            title += "\n : {}".format(self.si)
            return title

        syt.Menu(menu_title, options, quit_tag="Done").run()

        return self

    ##
    # Setup HPA
    ##
    def build_filter(self):
        """
        Through a _set of menus, this creates the select string for a HPA class
        @return:
        """
        hpa_list = ""

        def hpa_build_rating():
            qstring = ["", None, True]
            options = ["Want", "Own", "Rating", "Want+Own", "Want-Own"]
            choice = syt.Menu("- Create HPA Query Rating -", choices=options, type="return", drop_down=True,
                              quit_tag="Back").run()

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

            return qstring, True


        def hpa_build_price():

            price_types = ["historic_new", "historic_used", "current_new", "current_used"]
            fields = ["avg", "lots", "max", "min", "qty", "qty_avg", "piece_avg"]
            group_functions = ["AVG", "MIN", "MAX", "SUM"]  # For price types
            aggregate_functions = ["AVG", "SUM", "DIFFERENCE"]  # For fields
            c_price_types = []
            c_fields = []
            c_group_function = None
            c_aggregate_function = None

            c_price_types = syt.MultiChoiceMenu("- Choose Price Type(s) -", price_types)
            if len(c_price_types) == 0:
                return None
            if len(c_price_types) > 1:
                c_group_function = syt.Menu("- Choose group function -", choices=group_functions, drop_down=True,
                                            type=syt.Menu.RETURN).run()
            c_fields = syt.MultiChoiceMenu("- Choose Price field(s) -", fields)
            if len(c_fields) == 0:
                return None
            if len(c_fields) > 1:
                c_aggregate_function = syt.Menu("- Choose aggregate function -", choices=aggregate_functions,
                                                drop_down=True, type=syt.Menu.RETURN).run()
            return {"price_type": c_price_types, "field": c_fields,
                    "group_function": c_group_function, "aggregate_function": c_aggregate_function}, False


        options = [("Rating", hpa_build_rating),
                   ("Price", hpa_build_price)]
        hpa_list, rating = syt.Menu("- Create HPA Query -", choices=options, drop_down=True).run()
        if hpa_list == 0:
            hpa_list = None
            rating = False
        try:
            self.set_filter(hpa_list, rating)
        except ValueError:
            syt.log_error("Filter not set")
            pass

        return self

    def set_filter(self, select_filter=None, rating=False):
        self._select_filter = select_filter
        self._rating = rating

        # Todo Can I wrap this into one so I don't have to do it twice?
        if isinstance(select_filter, dict):
            select_filter = self._make_filter(select_filter)
        self._select_filter = select_filter
        if not isinstance(select_filter, list) and len(select_filter) < 2:
            raise ValueError("Invalid Filter Formation")
        return self

    def build_report_type(self):
        """
        -Report Type
            STANDARD = 0
            RELATIVE = 1
            RELATIVE_DAY = 2
            DELTA = 3
            DELTA_DAY = 4
        -Inflation Date
        -Relative Date: (_set_base_price_date) - start, end
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
        report_type = syt.Menu('- Choose Report Type -', choices=options, function=_get_report_type, type=syt.Menu.LOAD,
                               drop_down=True).run()

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
        base_price = syt.Menu('- Choose Base Price -', choices=options, function=_get_base_price, type=syt.Menu.LOAD,
                              drop_down=True).run()

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
                "End Date": HistoricPriceAnalyser.R_END_DATE
            }
            if type_text == "Custom":
                date = input("What custom date would you like to compare to? (yyyy-mm-dd) ")
                return date
            else:
                return report_types[type_text]

        options = (
            "None",
            "Start Date",
            "End Date",
            "Custom"
        )
        base_date = syt.Menu('- Choose Base Date -', choices=options, function=_get_base_date, type=syt.Menu.LOAD,
                             drop_down=True).run()

        inf_year = input("What year do you want to use for inflation (blank for none)? ")
        if inf_year == "":
            inf_year = None

        try:
            self.set_options(report_type, base_price, base_date, inf_year)
        except ValueError:
            syt.log_error("Options not set")
            pass

        return self

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
        self._report_options["Base Date"] = base_date
        self._report_options["Type"] = report_type
        self._report_options["Base Price"] = base_price
        self._report_options["Inflation Year"] = inf_year

        return self

    def get_set(self):
        """
        Used to prompt for a _set
        @return:
        """
        self._set(SetInfo(SetInfo.input_set_num()))
        return self

    def _set(self, si):
        """
        @param si:
        @return:
        """
        if si is not None:
            self.si = si
        return self
  

    def _build_report_data_sql(self, select_=None, where_=None, group=True):
        """Takes what we got in the starter filter (either a complete filter string or a dict of filter options
            and returns a built out _sql statement
        """
        h_select = "SELECT historic_prices.record_date"
        if select_ is not None:
            h_select += ", " + select_
        else:
            syt.log_error("Missing filter text")
            return None
            # h_select = "SELECT historic_prices.record_date, price_types.price_type, historic_prices.lots, historic_prices.qty, historic_prices.min, historic_prices.max, historic_prices.avg, historic_prices.qty_avg, historic_prices.piece_avg"
        h_joins = " FROM historic_prices JOIN sets ON (sets.id=historic_prices.set_id) JOIN price_types ON (price_types.id=historic_prices.price_type) JOIN bs_ratings ON (bs_ratings.set_id=historic_prices.set_id AND bs_ratings.record_date=historic_prices.record_date)"
        h_filter = " WHERE sets.set_num='{}'".format(self._si.set_num)
        if where_ is not None:
            h_filter += " AND " + where_
        if group:
            h_filter += " GROUP BY historic_prices.record_date"
        h_end = ";"
        h_sql = h_select + h_joins + h_filter + h_end
        return h_sql

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
                delete_sql = self._convert_select_to_delete(dp_list[idx][0])
                syt.log_info("SQL string: " + delete_sql)
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
                        # print("None")
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

    def _convert_select_to_delete(self, record_date):
        """

        Create a _sql string to use to delete based on the select string
        @param record_date:
        @return:
        """
        # Todo, remove this function. It is only needed because of the stupid dupe date in the database

        del_sql = " WHERE record_date={}".format(record_date,
                                                 self._si.set_num)
        # del_sql = " WHERE record_date={} AND set_id in (SELECT id from sets WHERE set_num='{}')".format(record_date,
        #                                                                                                 self._si.set_num)
        if 'bs_ratings' in self._select_filter[0]:
            del_sql = "DELETE FROM bs_ratings" + del_sql + ";"
        else:
            del_sql = "DELETE FROM historic_prices" + del_sql
            # if self._select_filter[1] is not None:
            # del_sql += " AND price_type in (SELECT id from price_types WHERE {});".format(self._select_filter[1])
        return del_sql

    def _clear(self):
        """
        Reverts the working data back to the original state
        @return:
        """
        self._working_data = copy.deepcopy(self._original_data)
        self._base_date = None
        self._base_price = None
        self._type = self.STANDARD
        self._inf_year = None

    def _sql(self, sql_statement):
        """Not safe to have publicly exposed, but very handy for my own personal project"""
        return db.run_sql(sql_statement)

    ##
    # Prepare Reports
    ##
    def run_report(self, si=None):
        """
        Run the report based on current settings and return two lists that can be turned into csv filed
        @return:
        """
        # Make sure the right variables are filled out
        if si is not None: self.si = si

        # Prepare the report
        self.prepare_report()

        # Run the report
        set_descs = self.get_set_info()
        set_prices = self._working_data
        return set_prices, set_descs

    ##
    # Prepare HPA for reporting
    ##
    def prepare_report(self):
        """
        Setup the working list based on the current settings (_type, inf etc)
        @return:
        """
        self._validate()
        self._process_filter()
        self._process_report_type()
        self._process_prices()
        self._process_dates()
        return self

    # Report Type
    def _process_report_type(self):
        self._set_inflation_year(self._report_options["Inflation Year"])
        self._set_report_type(self._report_options["Type"])
        self._set_base_price(self._report_options["Base Price"])
        self._set_base_date(self._report_options["Base Date"])

    def _set_report_type(self, rtype=None):
        """
        @param rtype: Options:
            standard - actual numbers (overrides all others)
            relative - percent change from start date
            relative_day - percent change from previous day (does not take into account start price)
            delta - price change from start date
            delta_day - price change *day over day*  (does not take into account start price)
        """
        self._type = self.STANDARD
        if rtype in (self.STANDARD, self.RELATIVE, self.RELATIVE_DAY, self.DELTA, self.DELTA_DAY):
            if rtype != self._type:
                self._type = rtype

    def _set_base_price(self, price=None, region="us"):
        """
        Sets the price to do all the calculations from. if none then calculations are done against the retail price
        - This has no effect in a standard report, only has effect in relative and delta reports (not day over day reports though)

        @param price: Options:
                R_NOT_RELATIVE = 0 compare price against historic get_prices (influenced by base date)
            These can only be used with relative and delta [_type]
                R_RETAIL_PRICE = 1 compare price against us/uk original
                R_START_PRICE = 2
                R_END_PRICE = 3
                price value
        @param region: Options:
                us or uk
        @return:
        """

        if price is None or price == "" or price == self.R_NOT_RELATIVE:
            self._base_price = None

        elif price == self.R_RETAIL_PRICE:
            if region == "uk":
                self._base_price = self._si.original_price_uk
            else:
                self._base_price = self._si.original_price_us
        elif price == self.R_START_PRICE:
            self._base_price = self._get_price_from_date(self._base_date)
        elif price == self.R_END_PRICE:
            self._base_price = self._get_price_from_date(self._base_date)
        else:
            self.price = syt.int_zero(price)

        if self._base_price is None and not (self._report_options["Base Price"] == self.R_NOT_RELATIVE or self._report_options["Base Price"] == None):
            raise ValueError("No Price to evaluate from [Base Price = {} | Report Type = {}]".format(price, self._report_options["Base Price"]))

    def _set_base_date(self, date=None, region="us"):
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
            self._base_date = None  # Date is not relative

        #   Set the compare date as the start date (or the earlist date)
        elif date == self.R_START_DATE:
            if region == "uk":
                self._base_date = self._si.ts_date_released_uk
            else:
                self._base_date = self._si.ts_date_released_us

            if self._base_date is None or self._base_date == "":
                if self._type != self.R_NOT_RELATIVE:
                    raise ValueError("No Start Date to evaluate")
                self._base_date = max(self._original_data.keys())

        #   Set the compare date as the end date
        elif date == self.R_END_DATE:
            if region == "uk":
                self._base_date = self._si.ts_date_ended_uk
            else:
                self._base_date = self._si.ts_date_ended_us
            if self._base_date is None or self._base_date == "":
                if self._type != self.R_NOT_RELATIVE:
                    raise ValueError("No End Date to evaluate")
                self._base_date = None
        else:
            self._base_date = syt.get_timestamp(date)
            self._base_price = self._get_price_from_date(self._base_date)

    def _set_inflation_year(self, year=None):
        """
        @param year: If none provided, it is _set to None
        @return:
        """
        self._inf_year = None
        if isinstance(year, int):
            if 1950 <= year <= arrow.get().year:
                self._inf_year = year

    def _get_price_from_date(self, date=None):
        """

        @param date: in timestamp format (or number if the dates are relative)
        @return:
        """
        if date is None: return None
        compare_ts = date  # syt.get_timestamp(date)
        closest_price_date = syt.get_closest_list(compare_ts, self._working_data.keys())
        self._base_date = date
        return self._working_data[closest_price_date]

    # Filter
    def _process_filter(self):
        sql_query = None
        if isinstance(self._select_filter, list) and len(self._select_filter) >= 2:
            sql_query = self._build_report_data_sql(*self._select_filter)
        else:
            raise ValueError("Invalid Filter Formation")

        # self._sql_query = sql_query
        sql_result = self._sql(sql_query)
        # This section is broken into a while loop to take care of the stupid date duplicates in the database
        # Can probably remove this and just delete all prices from that date
        if sql_result is not None and len(sql_result):
            clean_dict = False
            base_dict = {}
            while clean_dict is False:
                base_dict = syt.list_to_dict(self._process_date_price_list(sql_result))
                sql_result = self._sql(sql_query)
                if "rerun" not in base_dict: clean_dict = True

            # Store the results of the original query so we can restore it later
            self._original_data = syt.OrderedDictV2(sorted(base_dict.items(), key=lambda t: t[0]))
            # #   Store the _sql so we can work it later, or rebuild it if needed
            # self._sql_query = sql_query
            self._clear()
        else:
            raise ValueError("Invalid SQL Statement Formation: SQL Len: {}".format(len(sql_result)))

        # Prices

    def _process_prices(self):
        """

        This updates (calculates the prices) the _working_data dict with the new parameters
        This does not modify the dates, that is done in

        STANDARD = 0
        RELATIVE = 1  - %percent change from start date
        RELATIVE_DAY = 2 - %percent change from previous day (does not take into account start price)
        DELTA = 3 - price change from start date
        DELTA_DAY = 4 - price change *day over day*  (does not take into account start price)

        Uses these variables:
        self._type - see above
        self._base_date
        self._base_price
        self._inf_year
        @return:
        """
        new_dict = collections.defaultdict()
        if self._type == self.STANDARD:
            return self._working_data  # standard _type no change, Todo, should this _clear?

        # Delta simply means the difference from the base price
        elif self._type == self.DELTA:
            for db in self._working_data:
                new_dict[db] = syt.float_zero(self._working_data[db]) - syt.float_zero(self._base_price)

        # Delta simply means the %difference from the base price
        elif self._type == self.RELATIVE:
            for db in self._working_data:
                try:
                    new_dict[db] = (syt.float_zero(self._working_data[db]) / syt.float_zero(self._base_price)) - 1
                except ZeroDivisionError:
                    new_dict[db] = 0

        #   Delta day simply means the difference from the day before, base price doesn't matter
        elif self._type == self.DELTA_DAY:
            for idx, db in enumerate(self._working_data.keys()):
                if idx == 0:
                    new_dict[db] = 0
                    continue
                else:
                    previous_value = self._working_data.previous_key(db)
                    new_dict[db] = syt.float_zero(self._working_data[db]) - syt.float_zero(
                        self._working_data[previous_value])

        #   Delta day simply means the %difference from the day before, base price doesn't matter
        elif self._type == self.RELATIVE_DAY:
            for idx, db in enumerate(self._working_data.keys()):
                if idx == 0:
                    new_dict[db] = 0
                    continue
                else:
                    previous_value = self._working_data.previous_key(db)
                    try:
                        new_dict[db] = round(
                            (syt.float_zero(self._working_data[db]) / self._working_data[previous_value]) - 1, 6)
                    except ZeroDivisionError:
                        new_dict[db] = None
                    except TypeError:
                        new_dict[db] = None
        self._working_data = syt.OrderedDictV2(sorted(new_dict.items(), key=lambda t: t[0]))

        if self._inf_year is not None:
            self._working_data = syt.adj_dict_for_inf(self._working_data, self._inf_year)

        return self._working_data

    def _process_dates(self):
        """
            Take self._base_date and return the _working_data with the adjusted dates
        @return:
        """
        if self._base_date is not None:
            # For relative dates, get the days count
            self._working_data = syt.OrderedDictV2(
                sorted({syt.get_days_between(d, self._base_date): self._working_data[d]
                        for d in self._working_data}.items()))

        else:
            # Else return the date as a string
            self._working_data = syt.OrderedDictV2(sorted({arrow.get(d).format("YYYY-MM-DD"): self._working_data[d]
                                                           for d in self._working_data}.items()))

        return self

    def get_set_info(self, type="list"):
        """
        Gets basic information for the _set in the HPA, basically a nice to have
        @param type:
        @return:
        """
        if type == "list":
            return [self._si.set_num, self._si.name, self._si.theme, self._si.year_released, self._si.original_price_us,
                    self._si.date_released_us, self._si.date_ended_us]
        else:
            return {"set_num": self._si.set_num, "name": self._si.name, "theme": self._si.theme,
                    "date_release": self._si.date_released_us,
                    "original_price": self._si.original_price_us, "_base_date": syt.get_date(self._base_date),
                    "base_date_ts": self._base_date, "inflation_year": self._inf_year, "_base_price": self._base_price,
                    "report_type": self._type, "records": len(self._working_data)}

    def _validate(self, si=True, filter=True):
        """
            All in one package to make sure that everything that is needed for running reports is included
        @param si:
        @param filter:
        @return:
        """
        if si:
            if self.si is None:
                raise ValueError("No Set to evaluate")
        if filter:
            if self._select_filter is None:
                raise ValueError("No Select Filter")


    def run_all_test(self):
        self.get_set()  # Prompt for a new set every time, since this is a test

        in_progress = []

        range_types = (self.STANDARD, self.RELATIVE, self.RELATIVE_DAY, self.DELTA, self.DELTA_DAY)

        self._working_data = copy.deepcopy(self._original_data)

        try:
            for n in range_types:
                self.set_options(report_type=n, base_price=self.R_RETAIL_PRICE, base_date=None, inf_year=2015)
                self.prepare_report()
                in_progress.append(self.run_report())

            HistoricPriceAnalyser.csv_write(in_progress, name="{}-{}".format(self._si.set_num, self.name))
        except ValueError:
            syt.log_error("HPA is missing information")

        return self

    def save(self):
        if self.name is None:
            self.name = input("What would you like to call this report? ")
        if self.desc is None:
            self.desc = input("What is this report for? ")
        self.si = None
        file_path = syt.make_dir('resources/HistoricPriceAnalysers/{}_{}.hpa'.format(self.name, syt.get_timestamp()))
        pickle.dump(self, open(file_path, "wb"))
        print("HPA Saved")

    @staticmethod
    def load():
        """
        Static method because it can be used before the class is created
        @return: The loaded class
        """

        saves_dir = syt.make_dir('resources/HistoricPriceAnalysers/')

        def find_savefiles():
            filenames = os.listdir(saves_dir)
            setcollections = []
            for file in filenames:
                if file.endswith(".hpa"):
                    setcollections.append(file)
            return setcollections

        def _load(file_name):
            return pickle.load(open(saves_dir+file_name, "rb"))

        hpa = syt.Load_Menu(name="- Load HPA -", choices=find_savefiles(), function=_load).run()
        return hpa

    def _make_filter(self, filter_dict=None):
        """
            #For making _sql from a dictionary in this format:
            # {'price_types':[], 'fields':[], 'group_function':"", 'aggregate_function':""}
        @param dic:
        @return: a list in the standard format to build a filter _sql string
        """

        if isinstance(filter_dict, list) and len(filter_dict) == 3:
            return filter_dict

        if filter_dict is None:
            filter_dict = self._select_filter

        if len(filter_dict['field']) == 0 and len(filter_dict['price_type']) == 0:
            raise SyntaxError("Filter is not in the right format")

        sql_string = []

        # _validate dict
        if len(filter_dict['field']) > 1 and filter_dict['aggregate_function'] == None:
            raise SyntaxError("Missing aggregate function")
        elif len(filter_dict['price_type']) > 1 and filter_dict['group_function'] == None:
            raise SyntaxError("Missing group function")

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

    @staticmethod
    def csv_write(report_list, name=""):
        """
        @param report_list: A list in this format:
            [
            ({(date,price),(date,price),(date,price)},[set info]),
            ({(date,price),(date,price),(date,price)},[set info])
            ]
        @return: None, but it creates the reports using the 'name' param and a date string
        """
        date_min = None
        date_max = None
        date_set = set()  # a set has unique values so there won't be any overlap

        set_defs = []
        set_prices = []

        def_csv = ""
        price_csv = ""

        # Get date range
        syt.log_info("### Finding date range")
        for report_line in report_list:
            # Go through each element in the list. And find the lowest date.
            # This will throw a type error if they are of different types
            for date_price in report_line[0]:

                if date_min is None: date_min = date_price
                if date_max is None: date_max = date_price

                if date_price < date_min:
                    date_min = date_price
                elif date_price > date_max:
                    date_max = date_price
                date_set.add(date_price)  # add the date the the set

            # Build set def list here so we save for loops which cause stupid overhead
            set_defs.append(report_line[1])

        syt.log_info("... Date range found: {} - {} for ({}) sets".format(date_min, date_max, len(set_defs)))

        syt.log_info("### Building price csv string")
        date_list = sorted(date_set)  # Put the date list in order
        price_csv = "SET_NUM"
        for dte in date_list:
            price_csv += ",{}".format(dte)
        price_csv += "\n"

        # Get set line by line
        for report_line in report_list:
            price_csv += "{}".format(report_line[1][0])  # This is the location of the set number
            for date in date_list:
                try:
                    price_csv += ",{}".format(report_line[0][date])
                except:
                    price_csv += ","
            price_csv += "\n"
        syt.log_info("... all lines built")

        syt.log_info("### Building set definitions csv string")
        set_csv = "SET_NUM, NAME, THEME, YEAR_RELEASED, ORIGINAL_PRICE, START_DATE, END_DATE\n"
        for st in set_defs:
            set_csv += syt.list2string(st)
            set_csv += "\n"

        file_path = syt.make_dir('resources/Reports/')
        syt.log_info("### Building CSV files from strings")
        with open(file_path+'{}_{}-price-data.csv'.format(name, syt.get_timestamp()), "w") as f:
            f.write(price_csv)

        with open(file_path+'{}_{}-price-_set-data.csv'.format(name, syt.get_timestamp()), "w") as f:
            f.write(set_csv)
        syt.log_info("### Building CSV files built successfully")