# internal
from data.data_classes import SetInfo
import system as syt
if __name__ == "__main__": syt.setup_logger()

KEY = 'LmtbQqIRtP'
url = 'http://rebrickable.com/api'

# These methods rely on the monthly data-dump, they are faster but less accurate
def pull_all_colors():
    """
    USE pull_colors instead. It has more detail
    This is from a datadump on http://rebrickable.com/downloads
    It pulls all colors in rebrickable terms
    @return:
    """
    # url = "http://rebrickable.com/files/colors.csv.gz"
    # return public_api.read_gzip_csv_from_url(url)
    return pull_colors()


def pull_all_pieces():
    """
    This is from a datadump on http://rebrickable.com/downloads
    It pulls all piece types in the database
    @return:
    """
    url = "http://rebrickable.com/files/pieces.csv.gz"
    return syt.read_gzip_csv_from_url(url)


def pull_all_set_parts():
    """
    This is from a datadump on http://rebrickable.com/downloads
    It pulls all the inventories in the database, need to pull all pieces first
    @return:
    """
    url = "http://rebrickable.com/files/set_pieces.csv.gz"
    return syt.read_gzip_csv_from_url(url)


def pull_set_catalog():
    """
    There is no api to get a list of sets, so i just take the list of inventories and get the sets from that
    @return:
    """
    set_pieces = pull_all_set_parts()
    sets = set()  # Ignore duplicates
    for r in set_pieces:
        if r[0] == 'set_id':
            continue
        sets.add((r[0],))
    return sets


def pull_set_info(set_num):
    """
    key - API Key
    _set - The Set num to look up (e.g. 8043-1)
    format - How to display output data. Valid values: xml, json, csv, tsv
    @param set_num:
    @return:
    """
    parameters = {'key': KEY, 'set_id': set_num, 'format': 'csv'}
    return syt.read_csv_from_url(url + '/get_set', params=parameters)


def pull_set_inventory(set_num):
    """
    key - API Key
    _set - The Set ID to look up (e.g. 8258-1)
    format - How to display output data. Valid values: xml, json, csv, tsv
    @param set_num:
    @return:
    """
    parameters = {'key': KEY, '_set': set_num, 'format': 'csv'}
    return syt.read_csv_from_url(url + '/get_set_parts', params=parameters)


def _pull_piece_info(part_id):
    """
    key - API Key
    part_id - The Part ID to look up (e.g. 3001)
    inc_rels - Optional flag (1 or 0) to include Part Relationships in return data (may be a lot of data for some parts)
    inc_ext - Optional flag (1 or 0) to include external Part IDs (may be a lot of data for some parts due to LEGO element ids)
    format - How to display output data. Valid values: xml, json
    @param part_id:
    @return: in json format for some stupid reason (a dictionary)
    xml is a little easier to deal with
    """
    # parameters = {'key': KEY, 'part_id': part_id, 'inc_ext': '1', 'format': 'json'}
    # return syt.read_json_from_url(url + '/get_part', params=parameters)
    parameters = {'key': KEY, 'part_id': part_id, 'inc_ext': '1', 'format': 'xml'}
    return syt.read_xml_from_url(url + '/get_part', params=parameters)


def pull_piece_info(part_id):
    """
    Usable form of _pull_piece_info
    @param part_id:
    @return: [re_id, bl_id, name, alt_ids, element_ids] # The last two are just to help when looking it up
    """
    piece_info = _pull_piece_info(part_id)  # in xml format
    bl_id = piece_info.find('bricklink')
    alt_ids = None
    element_ids = None
    if bl_id is not None:
        bl_id = bl_id.text
    else:
        element_ids = []
        element_id_tags = piece_info.findAll("element_id")
        for tag in element_id_tags:
            element_ids.append(tag.text)
        alt_ids = []
        alt_ids_tags = []
        alt_ids_tags.extend(piece_info.findAll("peeron"))
        alt_ids_tags.extend(piece_info.findAll("ldraw"))
        alt_ids_tags.extend(piece_info.findAll("lego_design_id"))
        for tag in alt_ids_tags:
            alt_ids.append(tag.text)
    try:
        name = piece_info.find('name').text
    except:
        syt.log_note("Missing Piece Info: re_id={} does not exist through re_id api call".format(part_id))
        return [part_id, None, None, [part_id], []]
    return [part_id, bl_id, name, alt_ids, element_ids]


def pull_colors():
    """
    This doesn't use the API because it instead pulls ALL colors from this table: http://rebrickable.com/colors
        The public_api only returns the _main id
    @return: ['',rebrickable ID, Name, rgb hex, num parts, num sets, start year, start end, lego name, ldraw color, bricklink color, peeron color]
    note rebrickable ID is essentially the same as the ldraw id
    """
    url = 'http://rebrickable.com/colors'
    soup = syt.soupify(url)
    table = soup.find('table', {'class': 'table'})
    return syt.parse_html_table(table)


if __name__ == "__main__":

    def main_menu():
        """
        Main launch menu
        @return:
        """

        options = (
            ("Pull Set Info", menu_pull_set_info),
            ("Pull Set Inventory", menu_pull_set_inventory),
            ("Pull Piece Info", menu_pull_piece_info),
            ("Pull all Pieces", menu_pull_all_pieces),
            ("Pull all _set Parts", menu_pull_all_set_parts),
            ("Pull all Sets", menu_pull_all_sets),
            ("SYS Pull Colors", menu_pull_colors)
        )

        syt.Menu(name="– Rebrickable API testing –", choices=options).run()

    def menu_pull_all_pieces():
        csvfile = pull_all_pieces()
        syt.print4(csvfile)


    def menu_pull_all_set_parts():
        csvfile = pull_all_set_parts()
        filelist = list(csvfile)
        syt.print4(csvfile)
        print(len(filelist))

    def menu_pull_all_sets():
        csvfile = pull_set_catalog()
        syt.print4(csvfile, 100)

    def menu_pull_set_info():
        set_num = SetInfo.input_set_num()
        csvfile = pull_set_info(set_num)
        syt.print4(csvfile)


    def menu_pull_set_inventory():
        set_num = SetInfo.input_set_num()
        csvfile = pull_set_inventory(set_num)
        for c in csvfile:
            print(c)


    def menu_pull_piece_info():
        piece_num = input("What piece num? ")
        csvfile = pull_piece_info(piece_num)
        print(csvfile)  # a dictionary that will need to be parsed


    def menu_pull_colors():
        csvfile = pull_colors()
        syt.print4(csvfile)


    if __name__ == "__main__":
        main_menu()