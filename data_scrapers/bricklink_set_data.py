__author__ = 'andrew.sielen'

from LBEF import *
import pprint

# http://www.bricklink.com/catalogItem.asp?P=[piece number] <- gives you weight


pp = pprint.PrettyPrinter(indent = 4)


#Get base stats
def get_basestats(set_num_primary, set_num_secondary = 1):
    """
        Return a dictionary of base stats pulled from bricklink.com
            Set name
            Item No
            Year Released
            Weight
            Box Size
            Instruction Specs (number of booklets)
            Pieces
            Figures
    """
    url = "http://www.bricklink.com/catalogItem.asp?S={0}-{1}".format(set_num_primary, set_num_secondary)

    soup = soupify(url)
    if soup is None: return {}

    #Get the set name
    parent_tags0 = soup.find("font", {"size": "+0"})
    if parent_tags0 == None: return {}
    set_name = parent_tags0.string.strip()

    #Get figures and parts
    parent_tags1 = soup.find("td", {"width": "25%", "valign": "TOP", "class": "fv"})
    if not parent_tags1: return {}
    children_tags_text = parent_tags1.get_text()
    # print(children_tags_text)
    piece_count = 0
    figures_count = 0
    children_tags_text = children_tags_text[17:]
    children_tags_text = children_tags_text.split("(")[0]
    if "Part" in children_tags_text:
        end = children_tags_text.index("Part") - 1
        if "Set" in children_tags_text:
            start = children_tags_text.index("Set", 0, end) + 4
        else:
            start = children_tags_text.index("Of:", 0, end) + 3
        piece_count = scrub_text2int(children_tags_text[start:end])
        children_tags_text = children_tags_text[end:]
        #This line makes finding the minifigure count easier by removing the data for pieces
    if "Minifig" in children_tags_text:
        end = children_tags_text.index("Minifig") - 1
        try:
            start = children_tags_text.index("Parts", 0, end) + 6
        except:
            try:
                start = children_tags_text.index("Part", 0, end) + 5
            except:
                start = 0
        if start is None:
            figures_count = 0
        else:
            figures_count = scrub_text2int(children_tags_text[start:end])




    #Get the base stats
    parent_tags2 = soup.find("tr", {"align": "CENTER", "valign": "TOP"})
    parent_tags2.contents = parent_tags2.contents[1:-1] #Remove the first and last elements because they are strings

    dic = {"set_name": set_name, "pieces": piece_count, "figures": figures_count}
    for i in parent_tags2:
        if "Box" in i.contents[0].string.strip():
            #Converts the dimension string to a tuple
            dic[i.contents[0].string.strip()] = _parse_dimensions(i.contents[-1].string.strip())
        elif "Weight" in i.contents[0].string.strip():
            #Makes the weight a float instead of a string
            dic[i.contents[0].string.strip()] = float_null(i.contents[-1].string.strip())
        else:
            dic[i.contents[0].string.strip()] = i.contents[-1].string.strip()
            #i.contents[0] is the title tag / i.contents[-1] is the innermost tag

    return _scrub_base_data(dic)


def _parse_dimensions(s):
    """
        Takes a string like: 38\xa0x\xa028.5\xa0x\xa05.8 and returns (38,28.5,5.8)
    """
    if s == '?':
        return None
    return tuple([float_null(s) for s in str.split(s, u'\xa0x\xa0')])

def _scrub_base_data(dic):
    """
        Takes data scraped from Bricklink in this format:
        {   'Box Size (in cm):': (35.4, 19.0, 5.7),
            'figures': 0,
            'Instructions:': 'Yes',
            'Item No:': '4431-1',
            'pieces': 0,
            'set_name': 'Ambulance',
            'Weight (in grams):': 404.0,
            'Year Released:': '2012'}
        And returns it in this format:
        {   'dimensions': (35.4, 19.0, 5.7),             #tuple of float Box Size (in cm): -> dimensions
            'volume' : 3833.82,                          #float
            'figures': 0,                                #int
            'set_num': '4431-1',                         #text           Item No: -> set_num
            'pieces': 0,                                 #int
            'set_name': 'Ambulance',                     #text
            'weight' : 404.0,                            #float          Weight (in grams): -> weight
            'year_released': '2012'}                 #text           Year released: -> year_released (sqlite format)

    """
    scrubbed_dic = {}
    if 'set_name' in dic:
        if dic['set_name']=='': return {}
        scrubbed_dic['set_name'] = dic['set_name']
    if 'Item No:' in dic:
        if dic['Item No:']=='': return {}
        scrubbed_dic['set_num'] = dic['Item No:']
    if 'pieces' in dic:
        scrubbed_dic['pieces'] = dic['pieces']
    if 'Box Size (in cm):' in dic:
        temp_dim_tup = _scrub_dimensions(dic['Box Size (in cm):'])
        if temp_dim_tup[0] or temp_dim_tup[1]:
            scrubbed_dic['dimensions'],scrubbed_dic['volume'] = temp_dim_tup
    if "figures" in dic:
        scrubbed_dic['figures'] = dic['figures']
    if 'Weight (in grams):' in dic:
        scrubbed_dic['weight'] = dic['Weight (in grams):']
    if 'Year Released:' in dic:
        scrubbed_dic['year_released'] = int_null(dic['Year Released:'])

    return scrubbed_dic

def _scrub_dimensions(tup):
    """
        Takes a tuple in the form (35.4, 19.0, 5.7) and returns the tuple and the volume
    """
    if tup == (None,) or not tup:
        return (None,None)
    elif len(tup) == 2:
       return tup, tup[0]*tup[1]
    else:
        return tup, tup[0]*tup[1]*tup[2]



def main():
    SET = input("What is the set number?: ")
    pp.pprint(get_basestats(SET))
    main()

if __name__ == "__main__":
    main()