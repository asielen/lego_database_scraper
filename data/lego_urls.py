__author__ = 'andrew.sielen'

from data.data_classes import SetInfo

# Bricklink
bl_piece_value_new_url = "http://www.bricklink.com/catalogPOV.asp?itemType=S&itemNo={0}&itemSeq={1}&itemQty=1&breakType=M&itemCondition=N&incInstr=Y&incBox=Y&incParts=Y&breakSets=Y"
bl_piece_value_used_url = "http://www.bricklink.com/catalogPOV.asp?itemType=S&itemNo={0}&itemSeq={1}&itemQty=1&breakType=M&itemCondition=U&incInstr=Y&incBox=Y&incParts=Y&breakSets=Y"
bl_set_price_guide_url = "http://www.bricklink.com/catalogPG.asp?S={0}-{1}&colorID=0&viewExclude=Y&v=D&cID=Y"
bl_set_info_url = "http://www.bricklink.com/catalogItem.asp?S={0}-{1}"
bl_set_inv_url = "http://www.bricklink.com/catalogItemInv.asp?S={0}-{1}"

# Brickset
bs_set_info_url = "http://brickset.com/sets/{0}-{1}"
bs_set_inv_url = "http://brickset.com/inventories/{0}-{1}"


def get_links(set_num=None):
    if set_num is None:
        set_num = SetInfo.input_set_num()
    set_num_primary, set_num_secondary, _ = SetInfo.expand_set_num(set_num)

    print("- Links for: {} -".format(set_num))
    print(" Bricklink Links")
    print("  Set Info: " + bl_set_info_url.format(set_num_primary, set_num_secondary))
    print("  Set Inv: " + bl_set_inv_url.format(set_num_primary, set_num_secondary))
    print("  Price Info: " + bl_set_price_guide_url.format(set_num_primary, set_num_secondary))
    print("  Piece Out New: " + bl_piece_value_new_url.format(set_num_primary, set_num_secondary))
    print("  Piece Out Old: " + bl_piece_value_used_url.format(set_num_primary, set_num_secondary))
    print()
    print(" Brickset Links")
    print("  Set Info: " + bs_set_info_url.format(set_num_primary, set_num_secondary))
    print("  Set Inv: " + bs_set_inv_url.format(set_num_primary, set_num_secondary))




