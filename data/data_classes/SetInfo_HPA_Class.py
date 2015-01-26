# External
import collections
import copy

import arrow



# Internal
from data import update_secondary
import database as db
from database import info
import system as syt

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

def replace_comma(text):
    return str(text).replace(',', "/")

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
                # If setup with a list
                if len(set_info) == 27:
                    set_info_list = list(set_info)
                elif len(set_info) > 2 and isinstance(set_info[1], str):
                    # If the list is the wrong size, it still trys to find a set_num
                    s_num = syt.expand_set_num(set_info[1])[2]
            else:
                if isinstance(set_info, str):
                    # If setup with a string
                    s_num = syt.expand_set_num(set_info)[2]

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
        self.set_info_list[3], self.set_info_list[4], self.set_info_list[1] = syt.expand_set_num(set_id)

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
            price_inflated = (syt.get_inflation_rate(self.year_released,
                                                     year) * self.original_price_us) + self.original_price_us
            return price_inflated


    def get_calc_piece_count(self):
        return info.get_piece_count(self.set_num, 'bricklink')

    def get_calc_unique_pieces(self):
        return info.get_unique_piece_count(self.set_num)

    def get_calc_weight(self):
        return info.get_set_weight(self.set_num, 'bricklink')

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

    def get_date_min(self, type="end"):
        """

        @param type: start or end
        @return: The number of values it has before the [type] date
        6/30/14 = 1372550400 # The first possible date in the db
        """
        comp_date = self.date_ended_us
        if type == "start":
            comp_date = self.date_ended_us
        if comp_date is None: return None
        date_min = arrow.get(comp_date) - arrow.get(1372550400)
        return date_min.days

    def get_date_max(self, type="end"):
        """

        @param type: start or end
        @return: The number of values it has before the [type] date
        6/30/14 = 1372550400 # The first possible date in the db
        """
        comp_date = self.date_ended_us
        if type == "start":
            comp_date = self.date_ended_us
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

    def set_dump(self):
        """
        "id, set_num, set_name, set_theme, piece_count, figures, set_weight, year_released, date_released_us, date_ended_us,
        date_released_uk, date_ended_uk, original_price_us, original_price_uk, age_low, age_high, box_size, box_volume,
        last_updated, last_inv_updated_bl, last_inv_updated_re, last_daily_update, BASE CALC, ppp, ppp_uk, ppg, ppg_uk,
        avg_piece_weight,INFLATION, price_inf, ppp_inf, ppg_inf, CALC PIECE/WEIGHT, calc_piece_count, calc_unique_piece_count,
        calc_unique_to_total_piece_count, calc_weight, calc_avg_piece_weight, CALC INFLATION, calc_ppp_inf, calc_ppg_inf\n"
        """
        test_string = ""
        test_string += "{},".format(self.db_id)
        test_string += "{},".format(replace_comma(self.set_num))
        test_string += "{},".format(replace_comma(self.name))
        test_string += "{},".format(replace_comma(self.theme))
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
        test_string += "{},".format(replace_comma(self.box_size))
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
        "id, set_num, set_name, set_theme, piece_count, figures, set_weight, year_released, date_released_us, date_ended_us,
        date_released_uk, date_ended_uk, original_price_us, original_price_uk, age_low, age_high, box_size, box_volume,
        last_updated, last_inv_updated_bl, last_inv_updated_re, last_daily_update, BASE CALC, ppp, ppp_uk, ppg, ppg_uk,
        avg_piece_weight,INFLATION, price_inf, ppp_inf, ppg_inf, CALC PIECE/WEIGHT, calc_piece_count, calc_unique_piece_count,
        calc_unique_to_total_piece_count, calc_weight, calc_avg_piece_weight, CALC INFLATION, calc_ppp_inf, calc_ppg_inf\n"
        """
        syt.log_info("Building CSV")
        csv_string = ""
        csv_string += "Set Report, {}, {},\n".format(replace_comma(self.set_num),replace_comma(self.name))
        csv_string += "Database ID, {},\n".format(self.db_id)
        csv_string += "\n"
        csv_string += "Basic Info,\n"
        csv_string += "Set Num, {},\n".format(replace_comma(self.set_num))
        csv_string += "Set Name, {},\n".format(replace_comma(self.name))
        csv_string += "Theme, {},\n".format(replace_comma(self.theme))
        csv_string += "Piece Count, {},\n".format(self.piece_count)
        csv_string += "Figures, {},\n".format(self.figures)
        csv_string += "Set Weight, {},\n".format(self.weight)
        csv_string += "Year Released, {},\n".format(self.year_released)
        csv_string += "US Availability, {}, {},\n".format(self.date_released_us, self.date_ended_us)
        csv_string += "US Price, {},\n".format(self.original_price_us)
        csv_string += "UK Availability, {}, {},\n".format(self.date_released_uk, self.date_ended_uk)
        csv_string += "UK Price, {},\n".format(self.original_price_uk)
        csv_string += "Age Range, {}, {},\n".format(self.age_low, self.age_high)
        csv_string += "Box Dimensions, {},\n".format(replace_comma(self.box_size))
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
        date_list = sorted(date_list)

        for date in date_list:
            # Ratings
            csv_string += ",{},,,,,".format(syt.get_date(date))
            # Historic New
            csv_string += "{},{},{},{},{},{},{},,".format(hpd["historic_new.lots"].working_data[date],
                                                          hpd["historic_new.qty"].working_data[date],
                                                          hpd["historic_new.min"].working_data[date],
                                                          hpd["historic_new.max"].working_data[date],
                                                          hpd["historic_new.avg"].working_data[date],
                                                          hpd["historic_new.qty_avg"].working_data[date],
                                                          hpd["historic_new.piece_avg"].working_data[date])
            # HIstoric Used
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
        return self.get_price_history_all()  # , self.get_rating_history()

class HistoricPriceAnalyser(object):
    """
        This class basically acts as a pre-made sql query. In essence it just stores a sql string that is modified for
            whatever report you need.

        @NOTE: it only works on one price type at a time.@
    """
    STANDARD = 0
    RELATIVE = 1
    RELATIVE_DAY = 2
    DELTA = 3
    DELTA_DAY = 4


    def __init__(self, si=None, desc=None, select_filter=None):

        """
            @param desc: A short description of the filter
            @param select_filter: List:
                [select statement, where statement, group?] See the end of this doc for examples
                NOTE, filters have to return a list in the format [(date,price),(date,price)] (Only one price type at a time)
        """
        self.si = si  # the parent set. If none is provided, it doesn't create one until it is needed
        if desc is not None:
            self.desc = desc
        elif select_filter is not None:
            self.desc = select_filter[0]
        sql_query = None
        if isinstance(select_filter, list) and len(select_filter) >= 2:
            sql_query = self._build_historic_data_sql(*select_filter)
        else:
            sql_query = self._build_historic_data_sql()
        sql_result = self.sql(sql_query)
        if sql_result is not None and len(sql_result):
            base_dict = syt.list_to_dict(self._process_date_price_list(sql_result))
            # Store the results of the original query so we can restore it later
            self.original_data = OrderedDictV2(sorted(base_dict.items(), key=lambda t: t[0]))
            # Store the sql so we can work it later, or rebuild it if needed
            self.sql_query = sql_query
            # Same as clear - but needs to be defined in __init__ (set the working data = to the original data)
            self.working_data = copy.deepcopy(self.original_data)
            #Working_data_format:
            self.base_date = min(self.original_data.keys())  # ), key=self.original_data.get) # The first date
            self.base_price = self.original_data[self.base_date]  # The price at the first date
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
        DAY = 86400  # (60 * 60 * 24)  # Number of seconds in a day: 86400
        assert len(dp_list[
            0]) == 2  # If the list is longer than this, it returned a query with too many prices, only one at a time
        for idx, dp in enumerate(dp_list):
            if idx == 0:
                continue
            days_between = abs(syt.get_days_between(dp_list[idx][0], dp_list[idx - 1][0]))
            if days_between == 1:
                continue
            else:
                increment = round(
                    (syt.float_zero(dp_list[idx][1]) - syt.float_zero(dp_list[idx - 1][1])) / days_between, ndigits=2)
                for n in range(1, days_between):
                    # next_date = arrow.get(arrow.get(dp_list[idx-1][0]).replace(days=+n).timestamp).format("YYYY-MM-DD")
                    dp_list_to_add.append([arrow.get(dp_list[idx - 1][0]).replace(days=+n).timestamp,
                                           round((syt.float_zero(dp_list[idx - 1][1]) + (increment * n)), ndigits=2)])
        dp_list.extend(dp_list_to_add)
        return dp_list


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
        if rtype in (self.STANDARD, self.RELATIVE, self.RELATIVE_DAY, self.DELTA, self.DELTA_DAY):
            if rtype != self.type:
                self.type = rtype


    def set_base_price_date(self, price=None, date=None, region="us"):
        """
        Sets the price to do all the calculations from. if none then calculations are done against the retail price
        - This has no effect in a standard report, only has effect in relative and delta reports (not day over day reports though)

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
            self.base_date = syt.get_timestamp(date)
            self.base_price = self._get_price_from_date(self.base_date)

            # if self.base_date is None:
            # self.base_date = min(self.original_data.keys())
            # if self.base_price is None:
            #     self.base_price = max(self.original_data.keys())


    def run(self, by_date=False, clear=True):
        """

        @param by_date:
        @param clear: Default is to re-run from base. Can also set to False to rerun from existing
        @return:
        Default values:
            self.base_date = min(self.original_data, key=self.original_data.get)
            self.base_price = self.original_data[self.base_date]
            self.type = self.STANDARD
            self.inf_year = None
        """
        if clear: self.working_data = copy.deepcopy(self.original_data)
        if isinstance(self.inf_year, int):
            self.working_data = syt.adj_dict_for_inf(self.working_data, self.inf_year)
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
                results_dict[syt.get_ts_day(n)] = next_row
                # Note this returns a list not just a value, if you have one value (one price) you need to pull it out later

        return results_dict


    def _process_change_list(self):
        """

        This updates the working_data dict with the new parameters

        STANDARD = 0
        RELATIVE = 1  - percent change from start date
        RELATIVE_DAY = 2 - percent change from previous day (does not take into account start price)
        DELTA = 3 - price change from start date
        DELTA_DAY = 4 - price change *day over day*  (does not take into account start price)
        @return:
        """
        new_dict = collections.defaultdict()
        if self.type == self.STANDARD:
            return self.working_data  # standard type no change
        elif self.type == self.DELTA:
            for db in self.working_data:
                new_dict[db] = syt.float_zero(self.working_data[db]) - syt.float_zero(self.base_price)
        elif self.type == self.RELATIVE:
            for db in self.working_data:
                try:
                    new_dict[db] = (syt.float_zero(self.working_data[db]) / syt.float_zero(self.base_price)) - 1
                except ZeroDivisionError:
                    new_dict[db] = 0
        elif self.type == self.DELTA_DAY:
            for idx, db in enumerate(self.working_data.keys()):
                if idx == 0:
                    new_dict[db] = 0
                    continue
                else:
                    previous_value = self.working_data.previous_key(db)
                    new_dict[db] = syt.float_zero(self.working_data[db]) - syt.float_zero(
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
                            (syt.float_zero(self.working_data[db]) / self.working_data[previous_value]) - 1, 6)
                    except ZeroDivisionError:
                        new_dict[db] = None
        self.working_data = OrderedDictV2(sorted(new_dict.items(), key=lambda t: t[0]))
        return self.working_data


    def clear(self):
        """
        Reverts the working data back to the original state
        @return:
        """
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
                    "original_price": self.si.original_price_us, "base_date": syt.get_date(self.base_date),
                    "base_date_ts": self.base_date, "inflation_year": self.inf_year, "base_price": self.base_price,
                    "report_type": self.type, "records": len(self.working_data)}


    def get(self, by_date=False):
        """

        @param by_date: If False, return just the working data
                        If True... Todo - Explain this...
        @return: the results of the current query, or the current working data
        """
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
        compare_ts = date  # syt.get_timestamp(date)
        closest_price_date = syt.get_closest_list(compare_ts, self.working_data.keys())
        self.base_date = date
        return self.working_data[closest_price_date]

    def _build_historic_data_sql(self, select_=None, where_=None, group=True):
        """Takes what we got in the starter filter (either a complete filter string or a dict of filter options
            and returns a built out sql statement
        """
        h_select = "SELECT historic_prices.record_date"
        if select_ is not None:
            h_select += ", " + select_
        else:
            h_select = "SELECT historic_prices.record_date, price_types.price_type, historic_prices.lots, historic_prices.qty, historic_prices.min, historic_prices.max, historic_prices.avg, historic_prices.qty_avg, historic_prices.piece_avg"
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
        @return:
        """
        set_prices = []
        # set_defs = [["SET_NUM", "THEME", "YEAR_RELEASED", "ORIGINAL_PRICE", "DATE_START", "DATE_END"]]
        set_defs = self.get_def(type="list")
        self.clear()
        set_prices = self.run_all(types=[1], by_date=True)  #By date will start with the date ended

        return set_prices, set_defs




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
        #         return self._get_price_history()
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
        # @param select_filter: List: [select statement, where statement, group?]


        # @@BASE - can't be used, too many prices
    # SELECT sets.set_num, historic_prices.record_date, price_types.price_type,
    # historic_prices.lots, historic_prices.qty, historic_prices.min, historic_prices.max,
    # historic_prices.avg, historic_prices.qty_avg, historic_prices.piece_avg
    # FROM historic_prices
    # JOIN sets ON (sets.id=historic_prices.set_id)
    #   JOIN price_types ON (price_types.id=historic_prices.price_type)
    # WHERE sets.set_num='10501-1';
        #
        # @@AVERAGE 2+ fields
        # SELECT sets.set_num, historic_prices.record_date, price_types.price_type, (historic_prices.min+historic_prices.max)/2 # The 2 needs to be flexible TODO- what does this mean?
    # FROM historic_prices
    #   JOIN sets ON (sets.id=historic_prices.set_id)
    #   JOIN price_types ON (price_types.id=historic_prices.price_type)
    # WHERE sets.set_num='10501-1';
        #
        # @@SUM
    # SELECT sets.set_num, historic_prices.record_date, price_types.price_type, (historic_prices.min+historic_prices.max) # Same thing, no division
    # FROM historic_prices
    #   JOIN sets ON (sets.id=historic_prices.set_id)
    #   JOIN price_types ON (price_types.id=historic_prices.price_type)
    # WHERE sets.set_num='10501-1';
        #
        # @@COMBINE PRICE TYPES - AVERAGE THEM
    # SELECT sets.set_num, historic_prices.record_date, price_types.price_type, AVG(historic_prices.min+historic_prices.max)
    # FROM historic_prices
    #   JOIN sets ON (sets.id=historic_prices.set_id)
    #   JOIN price_types ON (price_types.id=historic_prices.price_type)
    # WHERE sets.set_num='10501-1' and (price_types.price_type='historic_used' OR price_types.price_type='historic_new')
    # GROUP BY historic_prices.record_date;
        #
        # @@COMBINE PRICE TYPES - SUM THEM (ALSO CAN DO MIN AND MAX)
    # SELECT sets.set_num, historic_prices.record_date, price_types.price_type, SUM(historic_prices.min+historic_prices.max)
    # FROM historic_prices
    #   JOIN sets ON (sets.id=historic_prices.set_id)
    #   JOIN price_types ON (price_types.id=historic_prices.price_type)
    # WHERE sets.set_num='10501-1' and (price_types.price_type='historic_used' OR price_types.price_type='historic_new')
    # GROUP BY historic_prices.record_date;




