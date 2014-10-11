__author__ = 'andrew.sielen'

from database import info
from system.base_methods import LBEF


class set_info(object):
    def __init__(self, set_num=None):
        set_info_list = info.get_set_info(set_num)
        if set_info_list is None:
            self.set_info_list = [None] * 26  # New Set
        else:
            self.set_info_list = set_info_list[0]

    # ###
    ##Basic Properties
    ###
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
        self.set_info_list[3], self.set_info_list[4], self.set_info_list[1] = LBEF.expand_set_num(set_id)

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
        return LBEF.get_date(self.set_info_list[12])

    @date_released_us.setter
    def date_released_us(self, value):
        """ @param value: In the format YYYY-MM-DD"""
        assert isinstance(value, str) or value is None
        self.set_info_list[12] = LBEF.get_timestamp(value)

    @property
    def ts_date_ended_us(self):
        return self.set_info_list[13]

    @ts_date_ended_us.setter
    def ts_date_ended_us(self, value):
        assert isinstance(value, int) or value is None
        self.set_info_list[13] = value

    @property
    def date_ended_us(self):
        return LBEF.get_date(self.set_info_list[13])

    @date_ended_us.setter
    def date_ended_us(self, value):
        """ @param value: In the format YYYY-MM-DD"""
        assert isinstance(value, str) or value is None
        self.set_info_list[13] = LBEF.get_timestamp(value)

    @property
    def ts_date_released_uk(self):
        return self.set_info_list[14]

    @ts_date_released_uk.setter
    def ts_date_released_uk(self, value):
        assert isinstance(value, int) or value is None
        self.set_info_list[14] = value

    @property
    def date_released_uk(self):
        return LBEF.get_date(self.set_info_list[14])

    @date_released_uk.setter
    def date_released_uk(self, value):
        """ @param value: In the format YYYY-MM-DD"""
        assert isinstance(value, str) or value is None
        self.set_info_list[14] = LBEF.get_timestamp(value)

    @property
    def ts_date_ended_uk(self):
        return self.set_info_list[15]

    @ts_date_ended_uk.setter
    def ts_date_ended_uk(self, value):
        assert isinstance(value, int) or value is None
        self.set_info_list[15] = value

    @property
    def date_ended_uk(self):
        return LBEF.get_date(self.set_info_list[15])

    @date_ended_uk.setter
    def date_ended_uk(self, value):
        """ @param value: In the format YYYY-MM-DD"""
        assert isinstance(value, str) or value is None
        self.set_info_list[15] = LBEF.get_timestamp(value)

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
        return LBEF.get_date(self.set_info_list[22])

    @last_updated.setter
    def last_updated(self, value):
        """ @param value: In the format YYYY-MM-DD"""
        assert isinstance(value, str) or value is None
        self.set_info_list[22] = LBEF.get_timestamp(value)

    @property
    def ts_last_inv_updated_bo(self):
        return self.set_info_list[23]

    @ts_last_inv_updated_bo.setter
    def ts_last_inv_updated_bo(self, value):
        assert isinstance(value, int) or value is None
        self.set_info_list[23] = value

    @property
    def last_inv_updated_bo(self):
        return LBEF.get_date(self.set_info_list[23])

    @last_inv_updated_bo.setter
    def last_inv_updated_bo(self, value):
        """ @param value: In the format YYYY-MM-DD"""
        assert isinstance(value, str) or value is None
        self.set_info_list[23] = LBEF.get_timestamp(value)

    @property
    def ts_last_inv_updated_bl(self):
        return self.set_info_list[24]

    @ts_last_inv_updated_bl.setter
    def ts_last_inv_updated_bl(self, value):
        assert isinstance(value, int) or value is None
        self.set_info_list[24] = value

    @property
    def last_inv_updated_bl(self):
        return LBEF.get_date(self.set_info_list[24])

    @last_inv_updated_bl.setter
    def last_inv_updated_bl(self, value):
        """ @param value: In the format YYYY-MM-DD"""
        assert isinstance(value, str) or value is None
        self.set_info_list[24] = LBEF.get_timestamp(value)

    @property
    def ts_last_inv_updated_re(self):
        return self.set_info_list[25]

    @ts_last_inv_updated_re.setter
    def ts_last_inv_updated_re(self, value):
        assert isinstance(value, int) or value is None
        self.set_info_list[25] = value

    @property
    def last_inv_updated_re(self):
        return LBEF.get_date(self.set_info_list[25])

    @last_inv_updated_re.setter
    def last_inv_updated_re(self, value):
        """ @param value: In the format YYYY-MM-DD"""
        assert isinstance(value, str) or value is None
        self.set_info_list[25] = LBEF.get_timestamp(value)

    @property
    def ts_last_daily_update(self):
        return self.set_info_list[26]

    @ts_last_daily_update.setter
    def ts_last_daily_update(self, value):
        assert isinstance(value, int) or value is None
        self.set_info_list[26] = value

    @property
    def last_daily_update(self):
        return LBEF.get_date(self.set_info_list[26])

    @last_daily_update.setter
    def last_daily_update(self, value):
        """ @param value: In the format YYYY-MM-DD"""
        assert isinstance(value, str) or value is None
        self.set_info_list[26] = LBEF.get_timestamp(value)

    ####
    ## Calculated Properties
    ####

    ##Price per Piece
    @property
    def ppp(self):
        if self.piece_count is not None and self.piece_count > 0:
            return self.original_price_us / self.piece_count

    @property
    def ppp_uk(self):
        if self.piece_count is not None and self.piece_count > 0:
            return self.original_price_uk / self.piece_count

    ##Price per Gram
    @property
    def ppg(self):
        if self.weight is not None and self.weight > 0:
            return self.original_price_us / self.weight

    @property
    def ppg_uk(self):
        if self.weight is not None and self.weight > 0:
            return self.original_price_uk / self.weight

    ####
    ##Calculated data
    ###
    def get_price(self, year=None):
        """Only works for US right now, only have US inflation rates"""
        if year is None or year == self.year_released:
            return self.original_price_us
        else:
            return info.get_set_price(self.set_num, year)

    def get_calc_piece_count(self):
        return info.get_piece_count(self.set_num, 'bricklink')

    def get_calc_unique_pieces(self):
        return info.get_unique_piece_count(self.set_num)

    def get_calc_weight(self):
        return info.get_set_weight(self.set_num, 'bricklink')

    def get_ppp_inf_adj(self, year=None, calc=False):
        piece_count = self.piece_count
        if calc == True:
            piece_count = self.get_calc_piece_count()
        return self.get_price(year) / piece_count

    def get_ppg_adj(self, year=None, calc=False):
        weight = self.weight
        if calc == True:
            weight = self.get_calc_weight()
        return self.get_price(year) / weight

    def get_price_history(self):
        """Get price history"""
        pass


    ####
    ##House keeping
    ###
    def push_updates_to_db(self):
        """Push Updates to the database"""
        pass


    def update_from_db(self):
        pass

    def __repr__(self):
        """The representation of the class"""
        pass

    def __str__(self):
        pass

    def __len__(self):
        return len(self.set_info_list)

    def __getitem__(self, item):
        if item < self.__len__():
            return self.set_info_list[item]




