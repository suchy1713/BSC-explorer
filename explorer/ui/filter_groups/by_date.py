from ui.components.date_picker import date_picker
from ui.components.filter_group_title import filter_group_title
from metadata.strings import *
from metadata.id_types import *
from metadata.keys import *


def by_date(team_id):
    id_index = (id_index_team, team_id)

    return [
        *filter_group_title(date_filter_group_title),
        *date_picker(start_date_filter_date, start_date_dropdown, id_index),
        *date_picker(end_date_filter_date, end_date_dropdown, id_index)
    ]
