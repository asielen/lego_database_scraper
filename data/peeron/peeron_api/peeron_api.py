__author__ = 'andrew.sielen'

# Master part list: http://www.peeron.com/inv/master.txt
# lego color guide: http://www.peeron.com/cgi-bin/invcgis/colorguide.cgi
# peeron colors: http://www.peeron.com/inv/colors


from system import base


def pull_colors():
    """
    @return: [peeron_name, parts, bl_name, bl_id, ldraw_id, ldraw_hex, lego_id, lego_name, rgb, cmyk, pantone, notes]
    note rebrickable ID is essentially the same as the ldraw id
    """
    url = 'http://www.peeron.com/inv/colors'
    soup = base.soupify(url)
    table_tags = soup.findAll('table')
    table = table_tags[1]
    return base.parse_html_table(table)
