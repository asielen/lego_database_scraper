# 20140603 This is still needed, no easy API for this data
# http://www.bricklink.com/catalogPG.asp?S=[piece number] <- gives you weight

import system as syt

def get_all_prices(set_num_primary, set_num_secondary=1):
    price_dict = {}
    piece_dict = {}
    piece_dict.update(get_pieceout_new(set_num_primary, set_num_secondary))
    piece_dict.update(get_pieceout_used(set_num_primary, set_num_secondary))
    piece_dict = _scrub_pieced_info(piece_dict)

    price_dict.update(_scrub_price_data(get_set_prices(set_num_primary, set_num_secondary)))

    price_dict = add_pieceInfo2PriceInfo(piece_dict, price_dict)

    return price_dict


def add_pieceInfo2PriceInfo(piece_dict, price_dict):
    if 'pieced_new' in piece_dict:
        if 'avg_historic_sales' in piece_dict['pieced_new']:
            price_dict['historic_new']['piece_avg'] = piece_dict['pieced_new']['avg_historic_sales']
        else:
            price_dict['historic_new']['piece_avg'] = None
        if 'current_sales' in piece_dict['pieced_new']:
            price_dict['current_new']['piece_avg'] = piece_dict['pieced_new']['current_sales']
        else:
            price_dict['current_new']['piece_avg'] = None
    if 'pieced_used' in piece_dict:
        if 'avg_historic_sales' in piece_dict['pieced_used']:
            price_dict['historic_used']['piece_avg'] = piece_dict['pieced_used']['avg_historic_sales']
        else:
            price_dict['historic_used']['piece_avg'] = None
        if 'current_sales' in piece_dict['pieced_used']:
            price_dict['current_used']['piece_avg'] = piece_dict['pieced_used']['current_sales']
        else:
            price_dict['current_used']['piece_avg'] = None

    return price_dict


def get_pieceout_new(set_num_primary, set_num_secondary=1):
    """
        Return a dictionary of the price of a pieced out new _set at the time this is run
    """
    url = "http://www.bricklink.com/catalogPOV.asp?itemType=S&itemNo={0}&itemSeq={1}&itemQty=1&breakType=M&itemCondition=N&incInstr=Y&incBox=Y&incParts=Y&breakSets=Y".format(
        set_num_primary, set_num_secondary)

    soup = syt.soupify(url)
    dic = _parse_priceout(soup)
    return {'pieced_new': dic}


def get_pieceout_used(set_num_primary, set_num_secondary=1):
    """
        Return a dictionary of the price of a pieced out new _set at the time this is run
    """
    url = "http://www.bricklink.com/catalogPOV.asp?itemType=S&itemNo={0}&itemSeq={1}&itemQty=1&breakType=M&itemCondition=U&incInstr=Y&incBox=Y&incParts=Y&breakSets=Y".format(
        set_num_primary, set_num_secondary)
    soup = syt.soupify(url)
    dic = _parse_priceout(soup)
    return {'pieced_used': dic}


# Get current market get_prices
def get_set_prices(set_num_primary, set_num_secondary=1):
    """
        From _set number, open the bricklink page and split it into current and _parse_historic_prices
        Return: Dictionary {Historic:{},Current:{}}
    """
    url = "http://www.bricklink.com/catalogPG.asp?S={0}-{1}&colorID=0&viewExclude=Y&v=D&cID=Y".format(set_num_primary,
                                                                                                      set_num_secondary)
    soup = syt.soupify(url)

    parent_tags = soup.find("tr", {"bgcolor": "#C0C0C0"})  # Relies on only that secion having that color

    if not parent_tags:
        return {"historic_new": {}, "historic_used": {}, "current_new": {}, "current_used": {}}

    historic_prices = {}
    historic_prices = _parse_historic_prices(parent_tags.contents[:2])

    current_prices = {}
    current_prices = _parse_current_prices(parent_tags.contents[2:])

    return {"historic_new": historic_prices["new"], "historic_used": historic_prices["used"],
            "current_new": current_prices["new"], "current_used": current_prices["used"]}


# Get new and used piece out data
def _parse_priceout(soup):
    """
        Shared parsing of New and Used Piece out parsing since the pages use the same format
    """
    parent_tags = soup.find("tr", {"bgcolor": "#EEEEEE", "valign": "TOP", "align": "CENTER"})
    # items.contents = items.contents[1:-1] #Remove the first and last elements because they are strings
    if parent_tags == None: return {}
    children_tags0 = parent_tags.findAll("td")

    historic_price = _parse_pieceout_price_block(children_tags0[0])
    current_price = _parse_pieceout_price_block(children_tags0[1])

    return dict(historic_price, **current_price)  # this combines two dictionaries into one


def _parse_pieceout_price_block(parent_tags):
    """
        Parse a single price box on the price piece out page
        Takes a {Tag} object returns a dictionary
    """
    children_tags0 = parent_tags.find("p")
    children_tags1 = children_tags0.findAll("font")

    return {
        children_tags1[0].string.strip(): syt.zero_2_null(syt.only_numerics_float(children_tags1[1].string.strip()))}


def _parse_current_prices(parent_tags_list):
    new_prices = _parse_price_block(parent_tags_list[0])
    used_prices = _parse_price_block(parent_tags_list[1])

    return {"new": new_prices, "used": used_prices}


def _parse_historic_prices(parent_tags_list):
    new_prices = _parse_price_block(parent_tags_list[0])
    used_prices = _parse_price_block(parent_tags_list[1])

    return {"new": new_prices, "used": used_prices}


def _parse_price_block(parent_tags):
    """
        Parses a single block in this form:
            Total Lots
            Total Qty
            Min Price
            Avg Price
            QTY Avg Price
            Max Price
    """

    children_tags0 = parent_tags.findAll("tr", {"align": "RIGHT"})

    prices = {}
    for i in children_tags0:
        prices[i.contents[0].string.strip()] = syt.zero_2_null(syt.only_numerics_float(i.contents[-1].string.strip()))

    return prices


def _scrub_price_data(dic):
    """
        Takes data scraped from Bricklink in this format:
            {   'pieced_new': {   'Average of last 6 months Sales:': 34.72,
                                  'Current Items For Sale Average:': 42.96},
               'pieced_used': {   'Average of last 6 months Sales:': 25.77,
                                   'Current Items For Sale Average:': 31.24},
               'current_new': {   'Avg Price:': 29.25,
                                   'Max Price:': 60.0,
                                   'Min Price:': 19.84,
                                   'Qty Avg Price:': 28.47,
                                   'Total Lots:': 62.0,
                                   'Total Qty:': 174.0},
                'current_used': {   'Avg Price:': 22.5,
                                    'Max Price:': 24.99,
                                    'Min Price:': 20.0,
                                    'Qty Avg Price:': 22.5,
                                    'Total Lots:': 2.0,
                                    'Total Qty:': 2.0},
                'historic_new': {   'Avg Price:': 21.41,
                                    'Max Price:': 28.03,
                                    'Min Price:': 12.78,
                                    'Qty Avg Price:': 20.52,
                                    'Times Sold:': 32.0,
                                    'Total Qty:': 202.0},
                'historic_used': {   'Avg Price:': 14.68,
                                     'Max Price:': 17.5,
                                     'Min Price:': 10.0,
                                     'Qty Avg Price:': 14.68,
                                     'Times Sold:': 5.0,
                                     'Total Qty:': 5.0}}
        And returns it in this format:
            {   'pieced_new': {   'avg_historic_sales': 34.72,
                                  'current_sales': 42.96},
               'pieced_used': {   'avg_historic_sales': 25.77,
                                   'current_sales': 31.24},
               'current_new': {   'avg': 29.25,
                                   'max': 60.0,
                                   'min': 19.84,
                                   'qty_avg': 28.47,
                                   'lots': 62.0,
                                   'qty': 174.0},
                'current_used': {   'avg': 22.5,
                                    'max': 24.99,
                                    'min': 20.0,
                                    'qty_avg': 22.5,
                                    'lots': 2.0,
                                    'qty': 2.0},
                'historic_new': {   'avg': 21.41,
                                    'max': 28.03,
                                    'min': 12.78,
                                    'qty_avg': 20.52,
                                    'sales': 32.0,
                                    'qty': 202.0},
                'historic_used': {  'avg': 14.68,
                                    'max': 17.5,
                                    'min': 10.0,
                                    'qty_avg': 14.68,
                                    'sales': 5.0,
                                    'qty': 5.0},
                'aggregate':    {   'total_sold_new' : ,
                                    'total_sold_used': ,
                                    'current_total_for_sale_new' : ,
                                    'current_total_for_sale_used' : }}

    """
    scrubbed_dic = {}



    # aggregate_dic = {'total_sold_new':0,'total_sold_used':0,
    # 'current_total_for_sale_new':0,'current_total_for_sale_used':0}
    # Not sure I actually need this
    if 'current_new' in dic:
        scrubbed_dic['current_new'] = _scrub_price(dic['current_new'])
    if 'current_used' in dic:
        scrubbed_dic['current_used'] = _scrub_price(dic['current_used'])
    if 'historic_new' in dic:
        scrubbed_dic['historic_new'] = _scrub_price(dic['historic_new'])
    if 'historic_used' in dic:
        scrubbed_dic['historic_used'] = _scrub_price(dic['historic_used'])

    if 'aggregate' in dic:
        scrubbed_dic['aggregate'] = dic['aggregate']

    return scrubbed_dic


def _scrub_pieced_price(dic):
    scrubbed_dic = {}
    if 'Average of last 6 months Sales:' in dic:
        scrubbed_dic['avg_historic_sales'] = dic['Average of last 6 months Sales:']
    if 'Current Items For Sale Average:' in dic:
        scrubbed_dic['current_sales'] = dic['Current Items For Sale Average:']
    return scrubbed_dic


def _scrub_pieced_info(dic):
    scrubbed_dic = {}
    if 'pieced_new' in dic:
        scrubbed_dic['pieced_new'] = _scrub_pieced_price(dic['pieced_new'])
    else:
        scrubbed_dic['pieced_new'] = None
    if 'pieced_used' in dic:
        scrubbed_dic['pieced_used'] = _scrub_pieced_price(dic['pieced_used'])
    else:
        scrubbed_dic['pieced_used'] = None
    return scrubbed_dic


def _scrub_price(dic):
    """
     Converts:                'current_new': {   'Avg Price:': 29.25,
                                   'Max Price:': 60.0,
                                   'Min Price:': 19.84,
                                   'Qty Avg Price:': 28.47,
                                   'Total Lots:': 62.0,
                                   'Total Qty:': 174.0},

    To :
                  'current_new': {   'avg': 29.25,
                                   'max': 60.0,
                                   'min': 19.84,
                                   'qty_avg': 28.47,
                                   'lots': 62.0,
                                   'qty': 174.0},
    """
    scrubbed_dic = {}
    if 'Avg Price:' in dic:
        scrubbed_dic['avg'] = dic['Avg Price:']
    else:
        scrubbed_dic['avg'] = None
    if 'Max Price:' in dic:
        scrubbed_dic['max'] = dic['Max Price:']
    else:
        scrubbed_dic['max'] = None
    if 'Min Price:' in dic:
        scrubbed_dic['min'] = dic['Min Price:']
    else:
        scrubbed_dic['min'] = None
    if 'Qty Avg Price:' in dic:
        scrubbed_dic['qty_avg'] = dic['Qty Avg Price:']
    else:
        scrubbed_dic['qty_avg'] = None
    if 'Total Lots:' in dic or 'Times Sold:' in dic:
        if 'Total Lots:' in dic:
            scrubbed_dic['lots'] = dic['Total Lots:']
        else:
            scrubbed_dic['lots'] = dic['Times Sold:']
    else:
        scrubbed_dic['lots'] = None
    if 'Total Qty:' in dic:
        scrubbed_dic['qty'] = dic['Total Qty:']
    else:
        scrubbed_dic['qty'] = None

    return scrubbed_dic


if __name__ == "__main__":
    import pprint as pp

    def main():
        SET = input("What is the _set number?: ")
        pp.pprint(get_all_prices(SET))
        main()


    main()