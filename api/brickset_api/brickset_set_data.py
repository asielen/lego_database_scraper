__author__ = 'andrew.sielen'

import pprint

from LBEF import *


# http://brickset.com/inventories/[set-num]-[set-seq] <- THe set inventory
# http://brickset.com/parts/[piece number] <-Gives you element number, element name, design number, color,


pp = pprint.PrettyPrinter(indent=4)


def get_basestats(set_num_primary, set_num_secondary=1):
    """
        Return a dictionary of base stats pulled from brickset.com
            Set type
            Theme group
            Theme
            SubTheme
            Year Released
            Pieces
            Minifigs
            RRP
            Price Per Piece
            Packaging
            Availability
            Notes
            Change Log
    """

    url = "http://brickset.com/sets/{0}-{1}".format(set_num_primary, set_num_secondary)

    soup = soupify(url)

    if soup is None: return {}

    dic = {}
    dic = _parse_sidebar(soup)
    dic = dict(dic, **_parse_avaiable_dates(soup))

    return scrub_data(dic)


# ### Get Daily Data #####
def get_daily_data(set_num_primary, set_num_secondary=1):
    """
        Returns a dictionary with the following data
            avilability dates
            rating
            want/own dates

        This is needed daily
    """
    url = "http://brickset.com/sets/{0}-{1}".format(set_num_primary, set_num_secondary)

    soup = soupify(url)

    dic = {}
    # #These three should be updated every day
    dic = dict(dic, **_parse_want_own(soup))
    dic = dict(dic, **_parse_avaiable_dates(soup))
    dic = dict(dic, **_parse_rating(soup))

    return scrub_daily_data(dic)


def _parse_sidebar(soup):
    if soup is None:
        return None
    parent_tags0 = soup.find("section", {"class": "featurebox"})
    if parent_tags0 is None:
        return {}

    children_tags0 = parent_tags0.findAll("dt")

    dic = {}
    for i in children_tags0:
        # print(i.string.strip())
        # print(i.next_sibling.next_sibling.string.strip())
        if i.text is not None and i.next_sibling.next_sibling.text is not None:
            if i.text.strip() == "Dimensions":
                dic[i.text.strip()] = _parse_set_dimensions(i.next_sibling.next_sibling.text)
            else:
                dic[i.text.strip()] = i.next_sibling.next_sibling.text.strip()
                # i.contents[0] is the title tagDATEVALUE("6/1/2013"), / i.contents[-1] is the innermost tag

    return dic


def _parse_set_dimensions(d_string):
    """
        Takes a beautiul soup object contents and returns the dimensions in the (,,) format
        example input:
             35.4 x 19.1 x 5.9 cm (13.9 x 7.5 x 2.3 in)
        example output:
            (35.4,19.1,5.9)
    """
    if 'cm' in d_string:
        # if 'cm' is in the second element of the list, use those numbers
        cm = str.split(d_string, "cm")[0]
        return tuple([zero_2_null(only_numerics_float(s)) for s in str.split(cm, ' x ')])
    else:
        # if no cm dims in the string
        return (None, None, None)


# def _parse_set_name(soup):
# """
#         Finds the set name in the soup
#     """
#     parent_tags0 = soup.find("h1")
#     if not parent_tags0:
#         return ""
#     return parent_tags0.string.strip()

def get_bs_want_own(set_num_primary, set_num_secondary=1):
    url = "http://brickset.com/sets/{0}-{1}".format(set_num_primary, set_num_secondary)

    soup = soupify(url)

    return _parse_want_own(soup)


def _parse_want_own(soup):
    """
        Returns the want and own values as a dictionary
    """
    parent_tags0 = soup.findAll("h2")

    parent_tags1 = 0
    for i in parent_tags0:
        if i.string == "Collections":
            parent_tags1 = i.parent
            break
    if parent_tags1 == 0: return {}

    children_tags1 = parent_tags1.findAll("li")

    dic = {}
    for i in children_tags1:
        dic[i.contents[1].strip()] = i.contents[0].get_text().strip()

    return dic


##### Get Dates #####
def get_bs_avaiable_dates(set_num_primary, set_num_secondary=1):
    url = "http://brickset.com/sets/{0}-{1}".format(set_num_primary, set_num_secondary)

    soup = soupify(url)

    return _parse_avaiable_dates(soup)


def _parse_avaiable_dates(soup):
    """
        Finds the "Availability at LEGO.com:" section and gets the data for US/UK
    """
    dates_dic = {}
    if soup is None:
        return {}
    parent_tags0 = soup.findAll("section", {"class": "featurebox"})
    if len(parent_tags0) < 2: return {}

    parent_tags1 = parent_tags0[1]
    if parent_tags1.contents == ['\n']:
        return {}
    children_tagsA = parent_tags1.findAll("dt")  #locations
    children_tagsB = parent_tags1.findAll("dd")  #prices
    for i in range(0, len(children_tagsA)):
        if len(children_tagsB[i].contents):
            dates_dic[children_tagsA[i].get_text()] = _parse_available_dates_string(children_tagsB[i].contents[0])
    return dates_dic


def _parse_available_dates_string(s):
    """
        Takes a string in this format: \r\n    11 Nov 11 - 18 Nov 12
            and returns ('2011-11-11','2012-11-18')
    """
    dates_list = [s.strip().split(' ') for s in s.split("-")]
    if len(dates_list) < 2: return ("", "")
    if dates_list == [[""], [""]]: return ("", "")
    dates_list_strings = (_parse_available_dates_make_string(dates_list[0]),
                          _parse_available_dates_make_string(dates_list[1]))

    return dates_list_strings


def _parse_available_dates_make_string(l):
    """
        Takes a string in this format: ('10','Nov','12')
            #and returns 2012-11-10'
            and returns the unix timestamp
    """
    months = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
              'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
    if len(l) < 2: return ""
    if l[1] not in months: return ""
    date_string = "20" + l[2] + "-" + months[l[1]] + "-" + l[0]
    return date_string


##### Get Dates #####

##### Get Rating #####
def get_bs_rating(set_num_primary, set_num_secondary=1):
    url = "http://brickset.com/sets/{0}-{1}".format(set_num_primary, set_num_secondary)

    soup = soupify(url)

    return _parse_rating(soup)


def _parse_rating(soup):
    """
        Finds the rating on the site and returns it in the format {'bs_rating':n}
    """
    parent_tag = soup.find("div", {"class": "rating"})
    if parent_tag is None: return {'bs_score': None}
    return {'bs_score': float(parent_tag.attrs['title'])}


def scrub_data(dic):
    """
        Takes code raw from the scrape and cleans it up using the rules in [BrickSet Data Scrub Specs]

        Takes data scraped from Brickset in this format:
        {   'Age range': '5 - 12',
            'Availability': 'Retail',
            'Barcodes': 'EAN: 5702014825109',
            'Change log': '',
            'LEGO item numbers': 'NA: 4648745',
            'Minifigs': '3',
            'Notes': '.',
            'Packaging': 'Box',
            'Dimensions': (13.9,7.5,2.3),
            'Pieces': '199',
            'Price per piece': '7.533p / 10.045c',
            'RRP': '14.99 / US$19.99',                     #Should have a pound sign but the debugger doesn't play well
            'Name': '4431-1: Ambulance',                with them in doc strings
            'Set type': 'Normal',
            'Subtheme': 'Medical',
            'Theme': 'City',
            'Theme group': 'Modern day',
            'Weight': '0.4Kg  (0.88 lb)',
            'Year released': '2012'}
        And returns it in this format:
        {   'age_range': (5,12),                            #tuple of ints  Age range -> age_range
            'availability': 'Retail',                       #text           Availability -> availability
            'lego_item_num': 'NA: 4648745',                 #text           LEGO item numbers -> lego_item_num
            'finifigs': 3,                                  #int            Minifigures -> figures
            'dimensions': (13.9,7.5,2.3),                   #tuple of float Packaging Dimensions -> dimensions  (cm)
            'volume' : 239.775,                             #float            -> volume (cm^3)
            'pieces': 199,                                  #int            Pieces -> pieces
            'price_per_piece': {'UK':7.533,'US':10.045},    #dic            Price per piece -> price_per_piece
            'original_price': {'UK':14.99,'US':19.99},      #dic            RRP -> original_price
            'set_name': 'Ambulance',                        #text           Set Name -> set_name (now only name)
            'set_num' : '4431-1',                           #text             -> set_num
            'subtheme': 'Medical',                          #text           Subtheme -> subtheme
            'theme': 'City',                                #text           Theme -> theme
            'weight': 400,                                  #float          Weight -> weight (grams)
            'year_released': '2012-1-1'}                #text           Year released -> year_released (sqlite format)
    """

    scrubbed_dic = {}

    if 'Name' in dic:
        if dic['Name'] == '': return {}
        scrubbed_dic['set_num'] = dic['Set number']
        scrubbed_dic['set_name'] = dic['Name']
    if 'Age range' in dic:
        scrubbed_dic['age_range'] = bs_scrub_age_range(dic['Age range'])
    if 'Availability' in dic:
        scrubbed_dic['availability'] = dic['Availability']
    if 'LEGO item numbers' in dic:
        scrubbed_dic['lego_item_num'] = dic['LEGO item numbers']
    if 'Minifigs' in dic:
        scrubbed_dic['figures'] = scrub_text2int(dic['Minifigs'])
    if 'Dimensions' in dic:
        scrubbed_dic['dimensions'], scrubbed_dic['volume'] = bs_scrub_dimensions(dic['Dimensions'])
    if 'Pieces' in dic:
        scrubbed_dic['pieces'] = scrub_text2int(dic['Pieces'])
    if 'Price per piece' in dic:
        scrubbed_dic['price_per_piece'] = bs_scrub_price(dic['Price per piece'])
    if 'RRP' in dic:
        scrubbed_dic['original_price'] = bs_scrub_price(dic['RRP'])
    if "Subtheme" in dic:
        scrubbed_dic['subtheme'] = dic['Subtheme']
    if "Theme" in dic:
        scrubbed_dic['theme'] = dic['Theme']
    if 'Weight' in dic:
        scrubbed_dic['weight'] = bs_scrub_weight(dic['Weight'])
    if 'Year released' in dic:
        scrubbed_dic['year_released'] = bs_scrub_year(dic['Year released'])

    if 'United Kingdom' in dic:
        scrubbed_dic['available_uk'] = dic['United Kingdom']
    if 'United States' in dic:
        scrubbed_dic['available_us'] = dic['United States']
    if 'people own this set' in dic:
        scrubbed_dic['bs_own'] = only_numerics_int(dic['people own this set'])
    if 'want this set' in dic:
        scrubbed_dic['bs_want'] = only_numerics_int(dic['want this set'])
    if 'bs_score' in dic:
        scrubbed_dic['bs_score'] = dic['bs_score']

    return scrubbed_dic


def scrub_daily_data(dic):
    """
        Takes code raw from the scrape and cleans it up using the rules in [BrickSet Data Scrub Specs]

        Takes data scraped from Brickset in this format:
        {   'Age range': '5 - 12',
            'Availability': 'Retail',
            'Barcodes': 'EAN: 5702014825109',
            'Change log': '',
            'LEGO item numbers': 'NA: 4648745',
            'Minifigs': '3',
            'Notes': '.',
            'Packaging': 'Box',
            'Dimensions': (13.9,7.5,2.3),
            'Pieces': '199',
            'Price per piece': '7.533p / 10.045c',
            'RRP': '14.99 / US$19.99',                     #Should have a pound sign but the debugger doesn't play well
            'Name': '4431-1: Ambulance',                with them in doc strings
            'Set type': 'Normal',
            'Subtheme': 'Medical',
            'Theme': 'City',
            'Theme group': 'Modern day',
            'Weight': '0.4Kg  (0.88 lb)',
            'Year released': '2012'}
        And returns it in this format:
        {   'age_range': (5,12),                            #tuple of ints  Age range -> age_range
            'availability': 'Retail',                       #text           Availability -> availability
            'lego_item_num': 'NA: 4648745',                 #text           LEGO item numbers -> lego_item_num
            'finifigs': 3,                                  #int            Minifigures -> figures
            'dimensions': (13.9,7.5,2.3),                   #tuple of float Packaging Dimensions -> dimensions  (cm)
            'volume' : 239.775,                             #float            -> volume (cm^3)
            'pieces': 199,                                  #int            Pieces -> pieces
            'price_per_piece': {'UK':7.533,'US':10.045},    #dic            Price per piece -> price_per_piece
            'original_price': {'UK':14.99,'US':19.99},      #dic            RRP -> original_price
            'set_name': 'Ambulance',                        #text           Set Name -> set_name (now only name)
            'set_num' : '4431-1',                           #text             -> set_num
            'subtheme': 'Medical',                          #text           Subtheme -> subtheme
            'theme': 'City',                                #text           Theme -> theme
            'weight': 400,                                  #float          Weight -> weight (grams)
            'year_released': '2012-1-1'}                #text           Year released -> year_released (sqlite format)
    """

    scrubbed_dic = {}

    if 'United Kingdom' in dic:
        scrubbed_dic['available_uk'] = dic['United Kingdom']
    else:
        scrubbed_dic['available_uk'] = (None, None)
    if 'United States' in dic:
        scrubbed_dic['available_us'] = dic['United States']
    else:
        scrubbed_dic['available_us'] = (None, None)
    if 'people own this set' in dic:
        scrubbed_dic['bs_own'] = only_numerics_int(dic['people own this set'])
    else:
        scrubbed_dic['bs_own'] = None
    if 'want this set' in dic:
        scrubbed_dic['bs_want'] = only_numerics_int(dic['want this set'])
    else:
        scrubbed_dic['bs_want'] = None
    if 'bs_score' in dic:
        scrubbed_dic['bs_score'] = dic['bs_score']
    else:
        scrubbed_dic['bs_score'] = None

    return scrubbed_dic


#These are functions that are unique to brickset data, they don't need to be in the generic scrub file
def bs_scrub_price(s):
    """
        Takes a string formatted like: '8.49 / US$9.99'
            and returns {'UK':8.49,'US':9.99}
    """
    price_dic = {}
    price_list = s.split('/')
    for p in price_list:
        if '\u00A3' in p or 'p' in p:
            #searches for the pound sign or pence
            price_dic['uk'] = zero_2_null(only_numerics_float(p))
        elif '$' in p or 'c' in p:
            #searches for the dollar sign or c for cents
            price_dic['us'] = zero_2_null(only_numerics_float(p))
    return price_dic


# def bs_scrub_set_name(s):
#     """
#         Takes a string in the format: 4431-1: Ambulance
#             and returns ['4431-1','Ambulance']
#     """
#     name_list = s.split(': ')
#     return name_list

def bs_scrub_age_range(s):
    """
        Takes a string in the format: '7 - 12'
            and returns (7,12)
        Could also be in the format: '7+'
            returns (7,)
    """
    ages = s.split('-')
    ages_list = tuple([zero_2_null(only_numerics_int(s)) for s in ages])
    if len(ages_list) < 2:
        ages_list = (ages_list[0], None)
    return ages_list


def bs_scrub_dimensions(t):
    """
        Needs to return tuple of dimensions + volume (l * w * h)
    """
    volume = t[0] * t[1] * t[2]
    if volume == 0: return [(None, None, None), None]
    return [t, volume]


def bs_scrub_weight(s):
    """
        Takes a string in the format: 0.4Kg  (0.88 lb)
            and returns 400.0
    """
    weight = s.split('Kg')[0]
    weight = only_numerics_float(weight) * 1000  #Kg to grams conversion
    if weight == 0: return None
    return weight


def bs_scrub_year(s):
    """
        Takes a year as '2012' and returns '2012-1-1'
    """
    return zero_2_null(only_numerics_int(s))


def main():
    set = input("What is the set num? ")
    pp.pprint(get_basestats(set))
    pp.pprint(get_daily_data(set))
    main()


if __name__ == "__main__":
    main()


