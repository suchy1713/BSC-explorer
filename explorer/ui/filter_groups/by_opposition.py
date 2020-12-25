from ui.components.multi_dropdown import multi_dropdown
from ui.components.range_slider import range_slider
from ui.components.filter_group_title import filter_group_title
from metadata.strings import *
from metadata.id_types import *
from metadata.keys import *


def by_opposition(team_id):
    id_index = (id_index_team, team_id)

    return [
        *filter_group_title(opposition_filter_group_title),
        *multi_dropdown(opposition_formation_filter_label, opposition_formation_dropdown, id_index),
        *range_slider(possession_filter_label, possession_slider, id_index)
    ]
