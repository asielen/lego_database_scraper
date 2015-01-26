# Internal
import navigation.menu
import database.info as info
import system as syt
from data import data_classes as dc

# todo

def main():
    options = {}
    options['1'] = "Quick Info", quick_info  # Working 2014-10-5
    options['2'] = "Make single set report", make_setReport
    options['3'] = "Make price report", make_priceReport  # Todo: See DM report for example
    options['4'] = "Make Collection Eval", make_collectionReport
    options['9'] = "Back", navigation.menu.back

    while True:
        result = navigation.menu.options_menu(options)
        if result is 'back':
            break
    print("Run Get Info")


def quick_info():
    set_num = syt.input_set_num()
    info.get_set_dump(set_num)


def make_setReport():
    set_num = syt.input_set_num()
    test_set = dc.SetInfo(set_num)
    test_set.set_report()


def make_priceReport():
    pass


def make_collectionReport():
    sec_collection_menu()


def sec_collection_menu():
    """
    TODO All of this
    Need to be able to build reports by
    Filters
        date range min / max
        piece count min / max
        original price min/max
        year released in date range - True False
        set_name = True
        theme
        set size buckets
        price buckets

    Broken out by: Buckets - these are not filters but rather agregators
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
        x number of historic prices - exclude sets that don't have many data points



    @return:
    """
    test_SC = None

    def menu_createSC():
        global test_SC
        filter_text = "(year_released BETWEEN 2008 AND 2015)"
        test_SC = dc.SetCollection(filter_text=filter_text)

    def menu_test_historic():
        global test_SC

        historic_data_sets = test_SC.historic_price_report()
        # syt.print4(historic_data_sets.items(), 20)


    def menu_data_dump():
        global test_SC
        filter_text = "(year_released BETWEEN 1980 AND 2015) AND ((piece_count >=25) OR (original_price_us >=4)) AND year_released IS NOT NULL AND set_name IS NOT NULL"
        test_SC = dc.SetCollection(filter_text=filter_text)
        csv_dump_text = test_SC.csv_dump()
        with open('{}-set-dump.csv'.format(syt.get_timestamp()), "w") as f:
            f.write(csv_dump_text)

    options = {}

    options['1'] = "Create Set Collection", menu_createSC
    options['2'] = "Get Historic", menu_test_historic
    options['3'] = "Get all Set Data", menu_data_dump
    options['9'] = "Back", navigation.menu.back

    while True:
        result = menu.options_menu(options)
        if result is 'back':
            break




if __name__ == "__main__":
    main()
