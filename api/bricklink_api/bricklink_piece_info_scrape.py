__author__ = 'andrew.sielen'

# 20140603 It looks like this will still be needed, there doesn't seem to be an easy way to get this data as a one off,
# all of this should be included in the master piece file (except the alternative models)

# http://www.bricklink.com/catalogItem.asp?P=4733
# http://www.bricklink.com/cataloglist.asp?&searchNo=Y&q=30063&catLike=W&catType=P <- Piece lookup

# external
import pprint
import re

#other module
import LBEF


def get_pieceinfo(design_num, design_name=None, type=0):
    """
        Return a dictionary of pieces from Brickset.com
        {
            {design_name : }
            {design_num : }
            {weight : }
            {design_alts : }
            {year_released : }
            {year_ended : }
        }
    """

    piece_info = {}
    bl_piece_info = get_blPieceInfo(design_num)
    if bl_piece_info is not None:
        piece_info["design_num"] = bl_piece_info['design_num'][0]
        piece_info["weight"] = bl_piece_info['weight']
        if design_name is None or design_name is '':
            piece_info["design_name"] = bl_piece_info['name']
        else:
            piece_info["design_name"] = design_name
        piece_info["piece_type"] = bl_piece_info['piece_type']
        piece_info["piece_category"] = bl_piece_info['category']
        # No longer using design alts 201406
        # if len(bl_piece_info['design_num']) == 2:
        #     piece_info["design_alts"] = bl_piece_info['design_num'][1]
        # else:
        #     piece_info["design_alts"] = ""
    else:
        piece_info = {'design_num': design_num, 'weight': None, 'design_name': design_name, 'piece_type': None,
                      'piece_category': None}  #,'design_alts': None}
    if type == 1:
        return [piece_info['design_num'],
                piece_info['design_name'],
                piece_info['weight'],
                piece_info['piece_type'],
                piece_info["piece_category"]]
    return piece_info


def get_blPieceInfo(design_num):
    """
        Actually pulls the piece info
    """

    soup = _search_piece(design_num)
    if soup is None:
        return None

    parent_tags0 = soup.find("td", {"colspan": "4", "align": "CENTER"})
    if parent_tags0 is None:
        return _check_minifig(soup, design_num)

    parent_tags1 = parent_tags0.find("tr", {"align": "CENTER", "valign": "TOP"})
    if parent_tags1 is None:
        return None
    child_tags0 = parent_tags1.findAll("td")
    weight_tag = child_tags0[3].get_text().split(":")[1]
    #Pull the weight from the tag that contains the weight.
    # EX: <td width="20%"><font color="#666666">Weight (in grams):</font><br>0.45</td>
    weight = LBEF.float_zero(weight_tag)

    #Find Name
    name_tag = soup.find("font", {"face": "Geneva,Arial,Helvetica"})
    name = name_tag.get_text()

    #Find Type and Categories
    types_tag = soup.find("font", {"face": "Arial"})
    types_links = types_tag.findAll("a")
    piece_type = None
    category = None
    if len(types_links) == 3:
        piece_type = _parse_type_category(str(types_links[1]))
        category = _parse_type_category(str(types_links[2]))

    #Find Alternate Design IDs

    parent_tags2 = soup.find("td", {"align": "RIGHT"})
    if parent_tags2 is None:
        return {'weight': weight, 'design_num': [design_num], 'name': name, 'piece_type': piece_type,
                'category': category}
    else:
        design_ids = []
        parent_tags3 = parent_tags2.find("td", {"align": "CENTER"})  #Find the alternative design id
        if parent_tags3 is None:
            return {'weight': weight, 'design_num': [design_num], 'name': name, 'piece_type': piece_type,
                    'category': category}
        parent_tags4 = soup.find("font", {"face": "Arial"})  #Find the _main design id
        design_id_text = parent_tags3.get_text()
        design_id_tags0 = design_id_text.split(":")[1]

        main_design_id = parent_tags4.get_text().split(":")[-1].strip()

        design_ids.append(main_design_id)  # Add the _main id
        design_ids.append(design_id_tags0)  # Add the alternative Ids

        return {'weight': weight, 'design_num': design_ids, 'name': name, 'piece_type': piece_type,
                'category': category}


def _parse_type_category(text):
    """
    Regular expressions, how do they work!?
    (takes a string like: catalogList.asp?catType=P&catString=85" and returns 85)
        Must have the = and the "
    @param text:
    @return:
    """
    prog = re.compile(r'[eg]=([A-Z0-9]*)">')
    result = prog.search(text)
    try:
        result = prog.search(text)
        result = result.group()
        return result[2:-2]
    except:
        return None


def _check_minifig(soup, design_num):
    parent_tags0 = soup.find("td", {"colspan": "3", "align": "CENTER"})
    if parent_tags0 is None:
        return None

    parent_tags1 = parent_tags0.find("tr", {"align": "CENTER", "valign": "TOP"})
    if parent_tags1 is None:
        return None

    child_tags0 = parent_tags1.findAll("td")
    weight_tag = child_tags0[2].get_text().split(":")[1]
    #Pull the weight from the tag that contains the weight.
    # EX: <td width="20%"><font color="#666666">Weight (in grams):</font><br>0.45</td>
    weight = LBEF.float_zero(weight_tag)

    #Find Type and Categories
    types_tag = soup.find("font", {"face": "Arial"})
    types_links = types_tag.findall("a")
    if len(types_links) == 3:
        type = _parse_type_category(types_links[1])
        category = _parse_type_category(types_links[2])

    #Find Name
    name_tag = soup.find("font", {"face": "Geneva,Arial,Helvetica"})
    name = name_tag.get_text()
    return {'weight': weight, 'design_num': [design_num], 'name': name, 'piece_type': type, 'category': category}


def _search_piece(design_num, verbose=0):
    soup = None
    url = "http://www.bricklink.com/catalogItem.asp?P={0}".format(design_num)
    if verbose == 1: print(url)
    soup = LBEF.soupify(url)
    if soup is not None:
        parent_tags0 = soup.find("font", {"size": "+2"})
        parent_tags1 = soup.find(text="Search Results")
        if parent_tags0 is None and parent_tags1 is None:
            return soup

        url = "http://www.bricklink.com/cataloglist.asp?&searchNo=Y&q={0}&catLike=W&catType=P".format(design_num)
        if verbose == 1: print(url)
        soup = LBEF.soupify(url)
        if soup is not None:
            parent_tags0 = soup.find("font", {"size": "+2"})
            parent_tags1 = soup.find(text="Search Results")
            if parent_tags0 is None and parent_tags1 is None:
                return soup
        url = "http://www.bricklink.com/catalogItem.asp?M={0}".format(design_num)
        if verbose == 1: print(url)
        soup = LBEF.soupify(url)
    return soup


def main():
    set = input("What is the piece num? ")
    pprint.pprint(get_pieceinfo(set))
    main()


if __name__ == "__main__":
    main()