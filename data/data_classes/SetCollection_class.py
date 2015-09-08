# External
import pickle
import os

# Internal
import database as db
from data.data_classes.SetInfo_HPA_Class import HistoricPriceAnalyser, SetInfo
import system as syt

if __name__ == "__main__": syt.setup_logger()

# TODO All of this
# Need to be able to build reports by
# Filters
# date range min / max -  SQL where
#     piece count min / max - SQL where
#     original price min/max - SQL where
#     year released in date range - True False
#     set_name = True
#     theme
# _set size buckets
#     price buckets
#
# Broken out by: Buckets - these are not filters but rather aggregatetors
#     Theme buckets
#     Set size buckets (0-20, 21-40, 41-60, 100-150, 151 and up) ^ maybe just use the above filter and not do it auto
#     Price buckets
#
# Price Type
#     Historic New
#         qty_avg
#         piece_avg
#     Historic Used
#     Current New
#     Current Used
#
# Report Type
#     Standard (no price adj)
#     relative to
#         start price of eval - relative to the first historic price in the database
#         original price - relative to the retail price
#         end price - relative to the price on the day it was discontinued
#
#     relative day
#     delta
#     delta day
#
# Other filter
#     x number of historic get_prices - exclude sets that don't have many data points
#
#
#
# @return:
# """

class SetCollection(object):
    """
        This stores a list of sets, but it also stores the filter list to get that list of text
        This makes it easier to do mass things to it because we can then do it just in _sql instead
        of loops

        There is the base filter, and then there is the report creation.
    """


    def __init__(self, set_list=None, filter_text=None):
        """
        @param set_list: List of get_set_nums
        @param filter_text: Filter Text e.g. "year_released = 2014, theme = city
        @return:
        """
        self.name = None
        set_filters = ""
        if set_list is not None and isinstance(set_list, list):
            set_filters = SetCollection.build_filter_from_set_list(set_list)
        if filter_text is not None:
            set_filters = "(" + filter_text + ")" + set_filters

        # set_data = _set_info_creator(self._run_query(filter_text=set_filters))
        self.set_data_lookups = {"calc_piece_count": None, "calc_unique_piece_count": None, "calc_weight": None,
                                 "calc_inf_price": None}
        self.report_settings = {}

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

    def __str__(self):
        return self.filter_text

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

    def get_date_range(self):
        """The date range of the collection """
        # Todo: Add month and region
        max_date = None
        min_date = None
        max_date = self._run_query(base_text="SELECT MAX(year_released) FROM sets", one=True)
        min_date = self._run_query(base_text="SELECT MIN(year_released) FROM sets", one=True)
        return min_date, max_date

    def get_themes(self, subtheme=False, coverage=False):
        """List of all the get_themes in the collection, when coverage is true, it returns the num of sets that have this field"""
        # Todo: add subtheme
        theme_list = self._run_query(base_text="SELECT DISTINCT theme FROM sets")
        if coverage:
            return theme_list, len(theme_list)
        return theme_list

    def get_set_nums(self):
        """List of all _set nums"""
        nums_list = self._run_query(base_text="SELECT set_num FROM sets", filter_text=None)
        nums_list = [n[0] for n in nums_list]
        return nums_list

    def _get_num_value(self, field="", type=None):
        """

        Used for any of the fields on a _set record that could contain a value that is worth summing counting etc
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

    def get_unique_piece_count(self):
        if self.set_data_lookups["calc_unique_piece_count"] is not None:
            return self.set_data_lookups["calc_unique_piece_count"]
        query = ("SELECT set_num, unique_pieces FROM sets AS S JOIN (SELECT bl_inventories.set_id, "
                 "COUNT(bl_inventories.quantity) AS unique_pieces FROM bl_inventories "
                 "JOIN parts ON bl_inventories.piece_id = parts.id ",
                 "GROUP BY bl_inventories.set_id) AS U ON S.id = U.set_id")
        self.set_data_lookups["calc_unique_piece_count"] = self._run_query(query[0], query[1])
        return self.set_data_lookups["calc_unique_piece_count"]

    def get_piece_count(self, type=None, calc=False):
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
            return self._get_num_value(field="get_piece_count", type=type)

    def get_prices(self, type=None, year=None):
        """
        @param type; either None, average, or total
        @param year; If this is a number it will adjust all the get_prices for that years inflation
        @return:
        """
        # Todo, year
        return self._get_num_value(field="original_price_us", type=type)

    def get_weights(self, type=None, calc=False):
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

    def get_figures(self, type=None):
        return self._get_num_value(field="get_figures", type=type)

    def get_age_range(self, type=None):
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
    # Calculated Data Todo
    # #
    def get_ppp(self, type=None):
        pass

    def get_ppg(self, type=None):
        pass

    # #
    # CSV DUMP
    # #
    # @profile
    def csv_dump(self):
        csv_dump_string = ""
        csv_dump_string += "id, set_num, set_name, set_theme, get_piece_count, get_figures, set_weight, year_released, date_released_us, date_ended_us, " \
                           "date_released_uk, date_ended_uk, original_price_us, original_price_uk, age_low, age_high, box_size, box_volume, " \
                           "last_updated, last_inv_updated_bl, last_inv_updated_re, last_daily_update, BASE CALC, get_ppp, ppp_uk, get_ppg, ppg_uk, " \
                           "avg_piece_weight,INFLATION, price_inf, ppp_inf, ppg_inf, CALC PIECE/WEIGHT, calc_piece_count, calc_unique_piece_count, " \
                           "calc_unique_to_total_piece_count, calc_weight, calc_avg_piece_weight, CALC INFLATION, calc_ppp_inf, calc_ppg_inf\n"
        timer = syt.process_timer("BUILDING CSV", verbose=False)
        sets = self.get_set_nums()
        total_sets = len(sets)
        timer.log_time(1, total_sets)
        current_set_count = 0
        for snum in sets:
            tSetInfo = SetInfo(snum)
            csv_dump_string += tSetInfo.set_dump()
            current_set_count += 1
            if current_set_count >= 40:
                timer.log_time(current_set_count, total_sets - (timer.tasks_completed + current_set_count))
                current_set_count = 0
        timer.end()
        file_path = syt.make_dir('resources/Reports/')
        with open(file_path+'{}_{}-basic-report.csv'.format(self.name, syt.get_timestamp()), "w") as f:
            print(f)
            f.write(csv_dump_string)
        return self

    # #
    # Advanced Data
    # #
    # R_STANDARD = 0
    # R_RELATIVE_DAY = 1
    # R_DELTA = 2
    # R_DELTA_DAY = 3
    #
    # R_NOT_RELATIVE = 0
    # R_RETAIL_PRICE = 1
    # R_END_PRICE = 2
    #
    # def choose_report_type(self):
    # """
    # Menu to choose a report _type
    #     @return:
    #     """
    #     report_type = []
    #     return report_type

    def build_hpa_report(self, sfilter=None, report_type=None):
        """
            Take the _set collection and layer a report on top of it
        @param sfilter:
        @param report_type:
        @return:
        """

        tHPA = HistoricPriceAnalyser().create()

        report_data = []  # This holds all the report data

        # date_list = []
        # date_range = [0, 0]
        # if sfilter is None:
        # sfilter = HistoricPriceAnalyser.build_filter()
        # if sfilter is None: return None
        # if report_type is None:
        #     report_type = HistoricPriceAnalyser.build_report_type()
        set_nums = self.get_set_nums()
        timer = syt.process_timer("Building Set Collection Report", verbose=False)
        for idx, snum in enumerate(set_nums):
            syt.log_info("   Getting set info on {} ".format(snum))
            try:
                report_data.append(tHPA.run_report(si=SetInfo(snum)))
            except ValueError as v:
                syt.log_warning(" ##  Skipped {} because {}".format(snum, v))
            timer.log_time(1, len(set_nums) - idx)
            # tHPA = HistoricPriceAnalyser.create(si=SetInfo(snum), select_filter=sfilter).set_options(**report_type) #Todo this throws an error with certain report_types, when report_type is not a dict
            # tHPA = HistoricPriceAnalyser(si=SetInfo(snum), _select_filter=sfilter).set_options(**report_type)

        timer.log_time(len(set_nums))
        timer.end()
        HistoricPriceAnalyser.csv_write(report_data, self.name)


    def save(self):
        if self.name is None:
            self.name = input("What do you want to call this collection? ")
        file_path = syt.make_dir('resources/SetCollections/{}_{}.sc'.format(self.name, syt.get_timestamp()))
        pickle.dump(self, open(file_path, "wb"))
        print("Set Collection Saved")

    @staticmethod
    def load():
        """
        Static method because it can be used before the class is created
        @return: The loaded class
        """

        saves_dir = syt.make_dir('resources/SetCollections/')

        def find_savefiles():
            filenames = os.listdir(saves_dir)
            setcollections = []
            for file in filenames:
                if file.endswith(".sc"):
                    setcollections.append(file)
            return setcollections

        def _load(file_name):
            return pickle.load(open(saves_dir+file_name, "rb"))

        return syt.Load_Menu(name="- Load Set Collection -", choices=find_savefiles(), function=_load).run()

    ##
    # Static Methods
    ##
    @staticmethod
    def build_filter_from_set_list(set_lists):
        """
        Take a list of _set lists and return a filter statement:  " OR set_num=xxx-xx OR ..."
        @param set_lists:
        @return:
        """
        def _validate_set_list(set_list, allow_set_nums=False):
            if len(set_list) == 27 and isinstance(set_list[1], str):
                return set_list[1]
            elif allow_set_nums is True and isinstance(set_list, str):
                return set_list
            return False

        set_num_filter = ""
        for s in set_lists:
            cset_num = _validate_set_list(s, allow_set_nums=True)
            if cset_num:
                set_num_filter += " OR sets.set_num = {}".format(cset_num)
            cset_num = None
        return set_num_filter

    @staticmethod
    def build_filter(make=True):
        """
        menu to build a list to be used to make a filter
        # Filters
        #     date range min / max -  SQL where
        #     piece count min / max - SQL where
        #     original price min/max - SQL where
        #     year released in date range - True False
        #     set_name = True
        #     theme
        @return:
        """
        # High, Low, Required? (True/False-if true, don't allow null values), Logic (True/False = AND/OR)
        date = [None, None, True, True]
        piece = [None, None, True, False]
        price = [None, None, False, False]
        theme = [None, True, False]  # No high, low


        def change_date_range():
            nonlocal date
            date_low = syt.int_null(input("What is the starting year? "))
            date_high = syt.int_null(input("What is the ending year? "))
            date_null = input("Don't include null dates? y/n ")
            if date_null.lower() == 'y':
                date_null = True
            else:
                date_null = False
            date_req = input("Is fitting in the date range required? y/n ")
            if date_req.lower() == 'y':
                date_req = True
            else:
                date_req = False

            date = [date_low, date_high, date_null, date_req]

        def change_piece_count():
            nonlocal piece
            piece_low = syt.int_null(input("What is the lowest piece count? "))
            piece_high = syt.int_null(input("What is the highest piece count? "))
            piece_null = input("Don't include null piece count? y/n ")
            if piece_null.lower() == 'y':
                piece_null = True
            else:
                piece_null = False
            piece_req = input("Is fitting in the piece count range required? y/n ")
            if piece_req.lower() == 'y':
                piece_req = True
            else:
                piece_req = False
            piece = [piece_low, piece_high, piece_null, piece_req]

        def change_price():
            nonlocal price
            price_low = syt.int_null(input("What is the lowest price? "))
            price_high = syt.int_null(input("What is the highest price? "))
            price_null = input("Don't include null price? y/n ")
            if price_null.lower() == 'y':
                price_null = True
            else:
                price_null = False
            price_req = input("Is fitting in the price range required? y/n ")
            if price_req.lower() == 'y':
                price_req = True
            else:
                price_req = False
            price = [price_low, price_high, price_null, price_req]

        def change_theme():
            nonlocal theme
            theme_name = input("What theme would you like to report on? ")
            if theme_name is "": theme_name = None
            theme_null = input("Don't include null theme? y/n ")
            if theme_null.lower() == 'y':
                theme_null = True
            else:
                theme_null = False
            theme_req = input("Is fitting in the theme required? y/n ")
            if theme_req.lower() == 'y':
                theme_req = True
            else:
                theme_req = False
            theme = [theme_name, theme_null, theme_req]


        def current_settings():
            settings = "- Create Filter -\n"
            settings += "| Date Range: {} to {} | Allow Null: {} | Required: {}\n".format(*date)
            settings += "| Price Range: {} to {} | Allow Null: {} | Required: {}\n".format(*price)
            settings += "| Piece Count Range: {} to {} | Allow Null: {} | Required: {}\n".format(*piece)
            settings += "| Theme: {} | Allow Null: {} | Required: {}\n".format(*theme)
            settings += "# Current Filter: {}".format(
                SetCollection.make_filter({"piece": piece, "date": date, "price": price, "theme": theme}))
            return settings

        options = (
            ("Date Range", change_date_range),
            ("Piece Count", change_piece_count),
            ("Original Price", change_price),
            ("Theme", change_theme)
        )
        syt.Menu(name=current_settings, choices=options, quit_tag="Done").run()

        if make:
            return SetCollection.make_filter({"piece": piece, "date": date, "price": price, "theme": theme})
        else:
            return {"piece": piece, "date": date, "price": price, "theme": theme}

    @staticmethod
    def make_filter(filter_dict=None):
        """
        Take a filter list and turn it into a string that can be used to make a _set collection
        @param filter_list:
        @return:
        "(year_released BETWEEN 1980 AND 2015) AND ((get_piece_count >=25) OR (original_price_us >=4)) AND year_released IS NOT NULL AND set_name IS NOT NULL"
        """
        select_text = ""
        required_text = "set_name IS NOT NULL"
        and_list = []
        or_list = []
        year_text = ""
        if filter_dict['date'][0] is not None or filter_dict['date'][1] is not None:
            if filter_dict['date'][0] is None:
                year_text += "(year_released <= {})".format(filter_dict['date'][1])
            elif filter_dict['date'][1] is None:
                year_text += "(year_released >= {})".format(filter_dict['date'][0])
            else:
                year_text += "(year_released BETWEEN {} AND {})".format(filter_dict['date'][0], filter_dict['date'][1])
        if len(year_text):
            if filter_dict['date'][3]:
                and_list.append(year_text)
            else:
                or_list.append(year_text)
        if filter_dict['date'][2]:
            required_text += " AND year_released IS NOT NULL"

        price_text = ""
        if filter_dict['price'][0] is not None or filter_dict['price'][1] is not None:
            if filter_dict['price'][0] is None:
                price_text += "(original_price_us <= {})".format(filter_dict['price'][1])
            elif filter_dict['price'][1] is None:
                price_text += "(original_price_us >= {})".format(filter_dict['price'][0])
            else:
                price_text += "(original_price_us BETWEEN {} AND {})".format(filter_dict['price'][0],
                                                                             filter_dict['price'][1])
        if len(price_text):
            if filter_dict['price'][3]:
                and_list.append(price_text)
            else:
                or_list.append(price_text)
        if filter_dict['price'][2]:
            required_text += " AND original_price_us IS NOT NULL"

        piece_text = ""
        if filter_dict['piece'][0] is not None or filter_dict['piece'][1] is not None:
            if filter_dict['piece'][0] is None:
                piece_text += "(piece_count <= {})".format(filter_dict['piece'][1])
            elif filter_dict['piece'][1] is None:
                piece_text += "(piece_count >= {})".format(filter_dict['piece'][0])
            else:
                piece_text += "(piece_count BETWEEN {} AND {})".format(filter_dict['piece'][0], filter_dict['piece'][1])
        if len(piece_text):
            if filter_dict['piece'][3]:
                and_list.append(piece_text)
            else:
                or_list.append(piece_text)
        if filter_dict['piece'][2]:
            required_text += " AND piece_count IS NOT NULL"

        theme_text = ""
        if filter_dict['theme'][0] is not None:
            theme_text = "(theme = {})".format(filter_dict['theme'][0])
        if len(theme_text):
            if filter_dict['theme'][2]:
                and_list.append(theme_text)
            else:
                or_list.append(theme_text)
        if filter_dict['theme'][2]:
            required_text += " AND them IS NOT NULL"

        and_text = ""
        if len(and_list):
            and_text += "("
            for idx, t in enumerate(and_list):
                if idx != 0: and_text += " AND "
                and_text += t
            and_text += ")"

        or_text = ""
        if len(or_list):
            or_text += "("
            for idx, t in enumerate(or_list):
                if idx != 0: or_text += " OR "
                or_text += t
            or_text += ")"

        if len(and_text):
            select_text += and_text

        if len(or_text):
            if len(select_text): select_text += " AND "
            select_text += or_text

        if len(required_text):
            if len(select_text): select_text += " AND "
            select_text += required_text

        return select_text


def SetCollection_menu():
    """
    Primary menu for building and playing with _set collections

    @return:
    """
    set_collection = None

    def menu_create_sc():
        nonlocal set_collection
        set_collection = SetCollection(filter_text=SetCollection.build_filter())

    def menu_create_basic_report():
        nonlocal set_collection
        if set_collection is None: menu_create_sc()
        set_collection.csv_dump()


    def menu_build_report():
        nonlocal set_collection
        if set_collection is None: menu_create_sc()
        set_collection.build_hpa_report()


    def menu_save_collection():
        nonlocal set_collection
        if set_collection is None: menu_create_sc()
        set_collection.save()

    def menu_load_collection():
        nonlocal set_collection
        set_collection = SetCollection.load()

    def menu_title():
        text = "- Set Collections -"
        if set_collection is not None:
            text = "\n| Collection filter text: {}".format(set_collection)
        return text

    options = (
        ("Create Set Collection", menu_create_sc),
        ("Build Basic Report", menu_create_basic_report),
        ("Build HPA Report", menu_build_report),
        ("Save Collection", menu_save_collection),
        ("Load Collection", menu_load_collection))

    syt.Menu(name=menu_title, choices=options).run()


if __name__ == "__main__":
    SetCollection_menu()
