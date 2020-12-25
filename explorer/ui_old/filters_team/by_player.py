import dash_core_components as dcc
import dash_html_components as html

from ui.filters_team.player.by_lineups import by_lineups
from ui.filters_team.filter_group_title import filter_group_title

def by_player(app, db, team_id, grid_coords):
    return [
        *filter_group_title('Filter by Players'),
        *by_lineups(app, db, team_id, 'include'),
        *by_lineups(app, db, team_id, 'exclude'),
    ]