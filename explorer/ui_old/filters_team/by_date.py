import dash_core_components as dcc
import dash_html_components as html

from ui.filters_team.date.by_date_filter import by_date_filter
from ui.filters_team.filter_group_title import filter_group_title

def by_date(app, db, team_id, grid_coords):
    return [
        *filter_group_title('Filter by Date'),
        *by_date_filter(app, db, team_id)
    ]