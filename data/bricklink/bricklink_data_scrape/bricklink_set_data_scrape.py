__author__ = 'andrew.sielen'

# 20150819 Updated for new bricklink new layout
# 20140603 It looks like this will still be needed, there doesn't seem to be an easy way to get this data as a one off,
# all of this should be included in the master _set file

# http://www.bricklink.com/catalogItem.asp?P=[piece number] <- gives you weight


import system as syt

# Get base stats
def get_basestats(set_num_primary, set_num_secondary=1):
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
    #url–old–total = "http://www.bricklink.com/catalogItem.asp?S={0}-{1}".format(set_num_primary, set_num_secondary)
    #url-old = 'http://alpha.bricklink.com/pages/clone/catalogitem.page?S={0}-{1}'.format(set_num_primary, set_num_secondary)
    url = 'http://alpha.bricklink.com/pages/clone/catalogitem.page?S={0}-{1}'.format(set_num_primary, set_num_secondary)

    soup = syt.soupify(url, bl_check=True)
    if soup is None: return {}

    # Get the _set name
    parent_tags0 = soup.find(id="item-name-title")
    if parent_tags0 == None: return {}
    set_name = parent_tags0.string.strip()

    parent_tags0 = soup.find('span', style="font-weight: bold; color: #2C6EA5")
    if parent_tags0 == None: return {}
    item_no = parent_tags0.string.strip()

    year_released = 0
    weight = 0
    box_size = ()
    piece_count = 0
    figures_count = 0

    # Get Years released, Weight and Size
    parent_tags1 = soup.find("td", {"width": "38%", "valign": "TOP"})
    if not parent_tags1: return {}
    children_tags_text = parent_tags1.get_text()


    # Year Released
    if "Released:" in children_tags_text:
        end = children_tags_text.index("Weight")
        start = children_tags_text.index("Released: ", 0, end) + len("Released: ")
        year_released = children_tags_text[start:end]
        children_tags_text = children_tags_text[end:]

    # Weight
    if "Weight" in children_tags_text:
        start = children_tags_text.index("Weight") + len("Weight: ")
        end = children_tags_text.index("\n", start) - 1 # less 1 because of the g for grams
        weight = syt.float_null(children_tags_text[start:end])
        children_tags_text = children_tags_text[end+len("g\n"):]

    # Box Size
    if "Size" in children_tags_text:
        start = children_tags_text.index("Size") + len("Size: ")
        end = children_tags_text.index("\n", start)
        box_size = _parse_dimensions(children_tags_text[start:end-len("cm")])


    #Get the Piece Count and Minifig Count
    parent_tags2 = soup.find("td", {"width": "31%", "valign": "TOP"}) # 2 elements match this, we want the first
    if not parent_tags2: return {}
    children_tags_text2 = parent_tags2.get_text()

    # Piece Count
    if "Part" in children_tags_text2:
        end = children_tags_text2.index("Part") - 1
        start = children_tags_text2.index("Of", 0, end) + len("Of\n\n")
        piece_count = syt.scrub_text2int(children_tags_text2[start:end])
        children_tags_text = children_tags_text2[end:]
    else:
        piece_count = 0

    if "Minifig" in children_tags_text2:
        end = children_tags_text2.index("Minifig") - 1
        start = children_tags_text2.index("\n", 0, end) + len("\n")
        figures_count = syt.scrub_text2int(children_tags_text2[start:end])
    else:
        figures_count = 0

    dic = {"set_name": set_name, "pieces": piece_count, "get_figures": figures_count,
           "year_released": year_released, 'box_size': box_size, 'set_num': item_no, 'weight': weight}

    return _scrub_base_data(dic)


def _parse_dimensions(string):
    """
        Takes a string like: 38 x 28.5 x 5.8 and returns (38,28.5,5.8)
    """
    if string == '?':
        return None
    return tuple([syt.float_null(s) for s in str.split(string, ' x ')])


def _scrub_base_data(dic):
    """
        Takes data scraped from Bricklink in this format:
        {   'box_size': (35.4, 19.0, 5.7),
            'get_figures': 0,
            'Item No:': '4431-1',
            'pieces': 0,
            'set_name': 'Ambulance',
            'weight': 404.0,
            'year_released': '2012'}
        And returns it in this format:
        {   'dimensions': (35.4, 19.0, 5.7),             #tuple of float Box Size (in cm): -> dimensions
            'volume' : 3833.82,                          #float
            'get_figures': 0,                            #int
            'set_num': '4431-1',                         #text           Item No: -> set_num
            'pieces': 0,                                 #int
            'set_name': 'Ambulance',                     #text
            'weight' : 404.0,                            #float          Weight (in grams): -> weight
            'year_released': '2012'}                     #text           Year released: -> year_released (sqlite format)

    """
    scrubbed_dic = {}
    if 'set_name' in dic:
        if dic['set_name'] == '': return {}
        scrubbed_dic['set_name'] = dic['set_name']
    if 'set_num' in dic:
        if dic['set_num'] == '': return {}
        scrubbed_dic['set_num'] = dic['set_num']
    if 'pieces' in dic:
        scrubbed_dic['pieces'] = dic['pieces']
    if 'box_size' in dic:
        temp_dim_tup = _scrub_dimensions(dic['box_size'])
        if temp_dim_tup[0] or temp_dim_tup[1]:
            scrubbed_dic['dimensions'], scrubbed_dic['volume'] = temp_dim_tup
    if "get_figures" in dic:
        scrubbed_dic['get_figures'] = dic['get_figures']
    if 'weight' in dic:
        scrubbed_dic['weight'] = dic['weight']
    if 'year_released' in dic:
        scrubbed_dic['year_released'] = syt.int_null(dic['year_released'])

    return scrubbed_dic


def _scrub_dimensions(tup):
    """
        Takes a tuple in the form (35.4, 19.0, 5.7) and returns the tuple and the volume
    """
    if tup == (None,) or not tup:
        return (None, None)
    elif len(tup) == 2:
        return tup, tup[0] * tup[1]
    else:
        return tup, tup[0] * tup[1] * tup[2]


if __name__ == "__main__":
    def main():
        from data.data_classes import SetInfo
        SET = SetInfo.input_set_num("What is the set number?: ")
        print("Getting Set: {}".format(SET))
        print(get_basestats(SET))
        main()

    if __name__ == "__main__":
        main()