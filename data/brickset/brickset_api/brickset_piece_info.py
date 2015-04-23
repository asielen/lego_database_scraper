#Not needed anymore? Todo
import pprint

import system as syt

# http://brickset.com/parts/473326 <-Piece lookup
# http://www.bricklink.com/catalogItem.asp?P=4733
# http://www.bricklink.com/cataloglist.asp?&searchNo=Y&q=30063&catLike=W&catType=P <- Piece lookup

# Get pieces stats
def get_pieceinfo(element_number):
    """
        Return a dictionary of pieces from Brickset.com
        {
            {part_num : }
            {design_name : }
            {design_num : }
            {color_name : }
            {weight : }
            {design_alts : }
        }
    """

    url = "http://brickset.com/parts/{0}".format(element_number)
    # print(url)
    soup = syt.soupify(url)

    piece_info = {}
    piece_info = _scrub_data(_parse_sidebar(soup))

    if piece_info is None: piece_info = {'design_num': design_num, 'weight': None, 'design_name': design_name,
                                         'piece_type': None, 'design_alts': None}
    bl_piece_info = get_blPieceInfo(piece_info["design_num"], element_number)
    if bl_piece_info is not None:
        piece_info["design_num"] = bl_piece_info['design_num'][0]
        piece_info["weight"] = bl_piece_info['weight']
        piece_info["piece_type"] = bl_piece_info['piece_type']
        if bl_piece_info['name'] != "":
            piece_info["design_name"] = bl_piece_info['name']
        if len(bl_piece_info['design_num']) == 2:
            piece_info["design_alts"] = bl_piece_info['design_num'][1]
        else:
            piece_info["design_alts"] = ""
    else:
        piece_info["weight"] = 0
        piece_info["design_alts"] = ""
        piece_info["piece_type"] = None

    return piece_info


def _parse_sidebar(soup):
    if soup is None:
        return None
    parent_tags0 = soup.find("section", {"class": "featurebox"})
    if parent_tags0 is None:
        return None

    children_tags0 = parent_tags0.findAll("dt")

    dic = {}
    for i in children_tags0:
        # print(i.string.strip())
        # print(i.next_sibling.next_sibling.stri{'weight': weight, 'design_num': [design_num], 'name': name}ng.strip())
        if i.text is not None and i.next_sibling.next_sibling.text is not None:
            dic[i.text.strip()] = i.next_sibling.next_sibling.text.strip()
            # i.contents[0] is the title tagDATEVALUE("6/1/2013"), / i.contents[-1] is the innermost tag

    return dic


def _scrub_data(dic):
    """
        Takes code raw from the scrape and cleans it up using the rules in [BrickSet Data Scrub Specs]
    """

    if dic is None: return None

    scrubbed_dic = {}

    if 'Element number' in dic:
        scrubbed_dic['part_num'] = dic['Element number']
    if 'Element name' in dic:
        scrubbed_dic['design_name'] = dic['Element name']
    if 'Design' in dic:
        scrubbed_dic['design_num'] = dic['Design']
    if 'Colour' in dic:
        scrubbed_dic['color_name'] = dic['Colour']
    return scrubbed_dic


def get_blPieceInfo(design_num, element_num):
    """
        Returns the piece weight from bricklink
    """

    soup = _search_piece(design_num, element_num)
    if soup is None:
        return None

    parent_tags0 = soup.find("td", {"colspan": "4", "align": "CENTER"})
    if parent_tags0 is None:
        return None

    parent_tags1 = parent_tags0.find("tr", {"align": "CENTER", "valign": "TOP"})
    if parent_tags1 is None:
        return None
    child_tags0 = parent_tags1.findAll("td")
    weight_tag = child_tags0[3].get_text().split(":")[
        1]  # Pull the weight from the tag that contains the weight. EX: <td width="20%"><font color="#666666">Weight (in grams):</font><br>0.45</td>
    weight = syt.float_zero(weight_tag)

    # Find Name
    name_tag = soup.find("font", {"face": "Geneva,Arial,Helvetica"})
    name = name_tag.get_text()


    # Find Alternate Design IDs

    parent_tags2 = soup.find("td", {"align": "RIGHT"})
    if parent_tags2 is None:
        return {'weight': weight, 'design_num': [design_num], 'name': name, 'piece_type': 'element'}
    else:
        design_ids = []
        parent_tags3 = parent_tags2.find("td", {"align": "CENTER"})  # Find the alternative design id
        if parent_tags3 is None:
            return {'weight': weight, 'design_num': [design_num], 'name': name, 'piece_type': 'element'}
        parent_tags4 = soup.find("font", {"face": "Arial"})  # Find the _main design id
        design_id_text = parent_tags3.get_text()
        design_id_tags0 = design_id_text.split(":")[1]

        main_design_id = parent_tags4.get_text().split(":")[-1].strip()

        design_ids.append(main_design_id)  # Add the _main id
        design_ids.append(design_id_tags0)  # Add the alternative Ids

        return {'weight': weight, 'design_num': design_ids, 'name': name, 'piece_type': 'element'}


def _search_piece(design_num, element_num):
    soup = None
    url = "http://www.bricklink.com/catalogItem.asp?P={0}".format(design_num)
    soup = syt.soupify(url)
    if soup is not None:
        parent_tags0 = soup.find("font", {"size": "+2"})
        parent_tags1 = soup.find(text="Search Results")
        if parent_tags0 is None and parent_tags1 is None:
            return soup

    url = "http://www.bricklink.com/cataloglist.asp?&searchNo=Y&q={0}&catLike=W&catType=P".format(design_num)
    soup = syt.soupify(url)
    if soup is not None:
        parent_tags0 = soup.find("font", {"size": "+2"})
        parent_tags1 = soup.find(text="Search Results")
        if parent_tags0 is None and parent_tags1 is None:
            return soup

        url = "http://www.bricklink.com/cataloglist.asp?&searchNo=Y&q={0}&catLike=W&catType=P".format(element_num)
        soup = syt.soupify(url)
        if soup is not None:
            parent_tags0 = soup.find("font", {"size": "+2"})
            parent_tags1 = soup.find(text="Search Results")
            if parent_tags0 is None and parent_tags1 is None:
                return soup

        url = "http://www.bricklink.com/cataloglist.asp?&searchNo=Y&q={0}&catLike=W&catType=M".format(element_num)
        soup = syt.soupify(url)
    return soup


def main():
    set = input("What is the piece num? ")
    pprint.pprint(get_pieceinfo(set))
    # pprint.pprint(get_pieceinfo_bl(_set))
    main()


if __name__ == "__main__":
    main()