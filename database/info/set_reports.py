__author__ = 'andrew.sielen'


def get_single_set_report(set_num):
    """
    create a csv file report of the set number
    @param set_num:
    @return:
    """
    if set_num is None:
        return None

    print("{0}-###################-{0}".format(set_id))
    print("Set: {} | {}".format(set_num, set_name))
    print("Theme: {} - {}".format(set_theme, set_sub_theme))
    print("Ages: {} to {}".format(set_age_low, set_age_high))
    print("Released US: {} - From {} to {}".format(set_year_released, set_date_released_us, set_date_ended_us))
    print("Released UK: {} - From {} to {}".format(set_year_released, set_date_released_uk, set_date_ended_uk))
    print("Pieces/Figures: {} / {} - Calc: [{}] / Uni: [{}]".format(set_piece_count, set_figures, set_calc_pieces,
                                                                    set_calc_unique_pieces))
    print("Weight: {} - Calc: [{}]".format(set_weight, set_calc_weight))
    print("Price: {} USD / {} GBP - Adj: [{}] USD".format(set_original_price_us, set_original_price_uk, set_calc_price))
    if set_piece_count is not None and set_calc_price is not None and set_piece_count > 0:
        print("PPP: Original {} - Adjusted: {}".format(set_original_price_us / set_piece_count,
                                                       set_calc_price / set_piece_count))
    if set_weight is not None and set_calc_price is not None and set_weight > 0:
        print("PPG: Original {} - Adjusted: {}".format(set_original_price_us / set_weight, set_calc_price / set_weight))
    print("Box Size: {} - Box Volume {}".format(set_box_size, set_box_volume))
    print("Last Updated: {}".format(set_last_updated))
    print("Inventory Last Updated: BL {} / RE {}".format(set_last_inv_updated_bl, set_last_inv_updated_re))
    print("Daily Pricing Last Updated: {}".format(set_last_price_updated))
    print("{0}-###################-{0}".format(set_id))