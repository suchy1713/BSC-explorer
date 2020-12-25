from utils.group_formations import group_formations
from utils.get_filters_label import get_filters_label
from utils.get_dropdown_input import get_dropdown_input
from utils.get_color import get_color
from metadata.keys import *


def get_intermid_output(db, trigger_team_id, clubs,
                        coaches,
                        coaches_options,
                        players_to_include,
                        players_to_include_options,
                        players_to_exclude,
                        players_to_exclude_options,
                        possession_vals,
                        possession_min,
                        possession_max,
                        opp_formation,
                        opp_formations_options,
                        start_dates,
                        start_dates_min,
                        end_dates,
                        end_dates_max,
                        colors,
                        indexes):
    ids = [i[id_index_team] for i in indexes]
    idx = ids.index(trigger_team_id)

    formations = db.get_formations(clubs[idx], coaches[idx],
                                   players_to_include[idx], players_to_exclude[idx], possession_vals[idx], opp_formation[idx],
                                   start_dates[idx], end_dates[idx])
    grouped = group_formations(formations)
    options = get_dropdown_input(grouped, label_to_display_key, vector_key)

    filters_label = get_filters_label(coaches[idx],
                                      coaches_options[idx], players_to_include[idx], players_to_exclude[idx],
                                      players_to_include_options[idx], players_to_exclude_options[idx],
                                      possession_vals[idx], possession_min[idx], possession_max[idx],
                                      opp_formation[idx], opp_formations_options[idx], start_dates[idx], end_dates[idx],
                                      start_dates_min[idx], end_dates_max[idx])

    intermid_dict = {
        intermid_formations_key: formations[[id_key, vector_key, label_key, minutes_key]].to_json(date_format='iso',
                                                                                                  orient='split'),
        intermid_club_id_key: clubs[idx],
        intermid_filters_label_key: filters_label,
        intermid_team_color_key: get_color(colors[idx], clubs[idx])
    }

    return options, options[0]['value'], intermid_dict
