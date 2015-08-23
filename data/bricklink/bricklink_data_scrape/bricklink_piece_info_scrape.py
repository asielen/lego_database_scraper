__author__ = 'andrew.sielen'

# 20140603 It looks like this will still be needed, there doesn't seem to be an easy way to get this data as a one off,
# all of this should be included in the master piece file (except the alternative models)

# http://www.bricklink.com/catalogItem.asp?P=4733
# http://www.bricklink.com/cataloglist.asp?&searchNo=Y&q=30063&catLike=W&catType=P <- Piece lookup
# New Site
# http://alpha.bricklink.com/pages/clone/catalogitem.page?P=30103

# external
import re

# internal
from database import info
import database as db
import system as syt
if __name__ == "__main__": syt.setup_logger()

def get_bl_piece_info(design_num, design_name=None, default='dict'):
    """
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
    if bl_piece_info is None and default is None: return None  # Todo what does default do?
    design_alts = None
    if bl_piece_info is not None and bl_piece_info != {}:
        piece_info["design_num"] = bl_piece_info['design_num'][0]
        piece_info["weight"] = bl_piece_info['weight']
        if design_name is None or design_name is '':
            piece_info["design_name"] = bl_piece_info['name']
        else:
            piece_info["design_name"] = design_name
        piece_info["piece_type"] = bl_piece_info['piece_type']
        piece_info["piece_category"] = bl_piece_info['category']
        if len(bl_piece_info['design_num']) == 2:
            design_alts = bl_piece_info['design_num'][1]
    else:
        piece_info = {'design_num': design_num, 'weight': None, 'design_name': design_name, 'piece_type': None,
                      'piece_category': None}  # ,'design_alts': None}
    if design_alts is not None:
        add_part_design_alt(design_num, design_alts)
    return piece_info

# Todo: This should probably not here here, should be where the rest of the database stuff is
def add_part_design_alt(primary, alts):
    """
    Add the design alt to the database
    @param alts:
    @return:
    """
    primary_id = info.get_bl_piece_ids(primary)
    alts = alts.split(',')
    if primary_id is not None:
        for n in alts:
            n = n.strip()
            db.run_sql("INSERT OR IGNORE INTO part_alternates(part_id, alternate_id) VALUES (?,?)", (primary_id, n))


def get_blPieceInfo(design_num):
    """
        Actually pulls the piece info
    """

    soup = _search_piece(design_num)
    if soup is None:
        return None


    # Get Name
    name =  ""
    parent_tags0 = soup.find(id="item-name-title")
    if parent_tags0 == None: return {}
    name = parent_tags0.string.strip()

    # Get weight
    weight = 0
    parent_tags1 = soup.find("td", {"width": "38%", "valign": "TOP"})
    if not parent_tags1: return {}
    children_tags_text = parent_tags1.get_text()
    if "Weight" in children_tags_text:
        start = children_tags_text.index("Weight") + len("Weight: ")
        end = children_tags_text.index("\n", start) - 1 # less 1 because of the g for grams
        weight = syt.float_null(children_tags_text[start:end])
        children_tags_text = children_tags_text[end+len("g\n"):]



    # Find Type and Categories
    piece_type = "P"
    category = None
    types_tag = soup.find("td", {"style": "background-color: #eeeeee; padding: 5px 5px 8px 5px; font-weight: bold;"})
    if types_tag is not None:
        types_links = types_tag.findAll("a")
        if len(types_links) >= 3:
            piece_type = _parse_type_category(str(types_links[1]))

            category = _parse_type_category(str(types_links[2]))

    if types_tag is None:
        return None


    # if piece_type == "M":
    #     return _check_minifig(soup, design_num)


    # if piece_type == "G" or piece_type == "B":
    #     parent_tags0 = soup.find("td", {"colspan": "3", "align": "CENTER"})
    # else:
    #     parent_tags0 = soup.find("td", {"colspan": "4", "align": "CENTER"})
    # if parent_tags0 is None:
    #     return None
    #
    # parent_tags1 = parent_tags0.find("tr", {"align": "CENTER", "valign": "TOP"})
    # if parent_tags1 is None:
    #     return None
    # child_tags0 = parent_tags1.findAll("td")
    #
    # weight_tag = child_tags0[3].get_text().split(":")[1]
    # # Pull the weight from the tag that contains the weight.
    # # EX: <td width="20%"><font color="#666666">Weight (in grams):</font><br>0.45</td>
    # weight = syt.float_zero(weight_tag)
    #
    # # Find Name
    # name_tag = soup.find("font", {"face": "Geneva,Arial,Helvetica"})
    # name = name_tag.get_text()



    # Find Alternate Design IDs
    design_ids = []
    parent_tags2 = soup.find("span", {"style": "display: inline-block; margin-top: 8px; font-family: Tahoma,Arial; font-size:13px;"})
    if parent_tags2 is None:
        return {'weight': weight, 'design_num': [design_num], 'name': name, 'piece_type': piece_type,
                'category': category}
    else:
        design_ids = []

        design_id_string = parent_tags2.get_text().replace("Item No:"," ").replace("Alternate"," ").replace(","," ")
        design_id_list = design_id_string.split(" ")
        design_ids = [x.strip() for x in design_id_list if x.strip() != '']
        if design_id_list is None:
            return None  # No proper design ID

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
        return 0  # unknown category

# # I don't think this is needed anymore
# def _check_minifig(soup, design_num):
#     parent_tags0 = soup.find("td", {"colspan": "3", "align": "CENTER"})
#     if parent_tags0 is None:
#         return None
#
#     parent_tags1 = parent_tags0.find("tr", {"align": "CENTER", "valign": "TOP"})
#     if parent_tags1 is None:
#         return None
#
#     child_tags0 = parent_tags1.findAll("td")
#     weight_tag = child_tags0[2].get_text().split(":")[1]
#     # Pull the weight from the tag that contains the weight.
#     # EX: <td width="20%"><font color="#666666">Weight (in grams):</font><br>0.45</td>
#     weight = syt.float_zero(weight_tag)
#
#     # Find Type and Categories
#     type = "M"
#     category = None
#     types_tag = soup.find("font", {"face": "Arial"})
#     if types_tag is not None:
#         types_links = types_tag.findAll("a")
#         if len(types_links) >= 3:
#             type = _parse_type_category(str(types_links[1]))
#             category = _parse_type_category(str(types_links[2]))
#
#     # Find Name
#     name = None
#     name_tag = soup.find("font", {"face": "Geneva,Arial,Helvetica"})
#     if name_tag is not None:
#         name = name_tag.get_text()
#     return {'weight': weight, 'design_num': [design_num], 'name': name, 'piece_type': type, 'category': category}


def _search_piece(design_num, verbose=0):
    soup = None
    url = "http://alpha.bricklink.com/pages/clone/catalogitem.page?P={0}".format(design_num)
    soup = _verify_valid_url(url, verbose)
    if soup is not None:
        return soup
    # alt search
    url = "http://www.bricklink.com/cataloglist.asp?&searchNo=Y&q={0}&catLike=W&catType=P".format(design_num)
    soup = _verify_valid_url(url, verbose)
    if soup is not None:
        return soup

    # minifigs
    url = "hhttp://alpha.bricklink.com/pages/clone/catalogitem.page?M={0}".format(design_num)
    soup = _verify_valid_url(url, verbose)
    if soup is not None:
        return soup
    # gear
    url = "http://alpha.bricklink.com/pages/clone/catalogitem.page?G={0}".format(design_num)
    soup = _verify_valid_url(url, verbose)
    if soup is not None:
        return soup
    # books
    url = "http://alpha.bricklink.com/pages/clone/catalogitem.page?B={0}".format(design_num)
    soup = _verify_valid_url(url, verbose)

    return soup


def _verify_valid_url(url, verbose=0):
    if verbose == 1: syt.log_debug(url)
    soup = syt.soupify(url)
    if soup is not None:
        parent_tags0 = soup.find("div", {"class",  "error-section"})
        parent_tags1 = soup.find("div", {"id",  "idNoResults"})
        if parent_tags0 is None and parent_tags1 is None:
            return soup
        else:
            return None
    return None


if __name__ == "__main__":
    part = input("part num? ")
    print(get_blPieceInfo(part))