from ui.components.multi_dropdown import multi_dropdown
from ui.components.filter_group_title import filter_group_title
from metadata.strings import *
from metadata.id_types import *
from metadata.keys import *


def by_players(team_id):
    id_index = (id_index_team, team_id)

    return [
        *filter_group_title(players_filter_group_title),
        *multi_dropdown(include_players_filter_label, include_players_dropdown, id_index),
        *multi_dropdown(exclude_players_filter_label, exclude_players_dropdown, id_index)
    ]