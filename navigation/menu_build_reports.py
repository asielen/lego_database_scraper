# Internal
from data.data_classes import SetInfo
import system as syt
from data import data_classes as dc

# todo

def report_menu():
    options = (
        ("Quick Info", quick_info),  # Working 2014-10-5
        ("Make single set report", make_setReport),
        ("Make price report", make_priceReport),  # Todo: See DM report for example
        ("Make Collection Evaluator", make_collectionReport)
    )

    syt.Menu("- Build Set Report -", choices=options).run()


def quick_info():
    set_num = SetInfo.input_set_num()
    set = dc.SetInfo(set_num)
    print(set.debug_dump_all())


def make_setReport():
    set_num = SetInfo.input_set_num()
    test_set = dc.SetInfo(set_num)
    test_set.make_set_report()

def make_priceReport():
    pass


def make_collectionReport():

    sec_collection_menu()


def sec_collection_menu():
    # Todo 201502 - SET COLLECTIONS CLASS
    """
    TODO All of this
    Need to be able to build reports by
    Filters
        date range min / max -  SQL where
        piece count min / max - SQL where
        original price min/max - SQL where
        year released in date range - True False
        set_name = True
        theme
        set size buckets
        price buckets

    Broken out by: Buckets - these are not filters but rather aggregatetors
        Theme buckets
        Set size buckets (0-20, 21-40, 41-60, 100-150, 151 and up) ^ maybe just use the above filter and not do it auto
        Price buckets

    Price Type
        Historic New
            qty_avg
            piece_avg
        Historic Used
        Current New
        Current Used

    Report Type
        Standard (no price adj)
        relative to
            start price of eval - relative to the first historic price in the database
            original price - relative to the retail price
            end price - relative to the price on the day it was discontinued

        relative day
        delta
        delta day

    Other filter
        x number of historic get_prices - exclude sets that don't have many data points



    @return:
    """
    test_SC = None

    def menu_createSC():
        nonlocal test_SC
        filter_text = "(year_released BETWEEN 2008 AND 2015)"
        test_SC = dc.SetCollection(filter_text=filter_text)

    def menu_test_setcollection():
        nonlocal test_SC
        if test_SC is None: menu_createSC()
        test_SC.build_report()
        # syt.print4(historic_data_sets.items(), 20)


    def menu_data_dump():
        nonlocal test_SC
        filter_text = "(year_released BETWEEN 1980 AND 2015) AND ((get_piece_count >=25) OR (original_price_us >=4)) AND year_released IS NOT NULL AND set_name IS NOT NULL"
        test_SC = dc.SetCollection(filter_text=filter_text)
        csv_dump_text = test_SC.csv_dump()
        with open('{}-set-dump.csv'.format(syt.get_timestamp()), "w") as f:
            f.write(csv_dump_text)

    options = (
        ("Test Set Collection", menu_test_setcollection),
        ("Get all Set Data", menu_data_dump)
    )
    syt.Menu("- Set Collections -", choices=options, drop_down=True).run()





if __name__ == "__main__":
    report_menu()
