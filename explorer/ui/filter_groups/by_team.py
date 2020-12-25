from ui.components.dropdown import dropdown
from ui.components.multi_dropdown import multi_dropdown
from ui.components.filter_group_title import filter_group_title
from ui.components.storage import storage
from metadata.strings import *
from metadata.id_types import *
from metadata.keys import *


def by_team(team_id, seasons):
    id_index = (id_index_team, team_id)

    return [
        storage({'type': team_colors_storage, id_index_team: team_id}),
        *filter_group_title(team_filter_group_title(team_id)),
        *dropdown(season_filter_label, season_dropdown, id_index, seasons),
        *dropdown(league_filter_label, league_dropdown, id_index),
        *dropdown(club_filter_label, club_dropdown, id_index),
        *multi_dropdown(coach_filter_label, coach_dropdown, id_index)
    ]
