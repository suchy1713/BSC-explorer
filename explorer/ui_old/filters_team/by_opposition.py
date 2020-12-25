import dash_core_components as dcc
import dash_html_components as html

from ui.filters_team.opposition.by_opp_team import by_opp_team
from ui.filters_team.opposition.by_opp_formation import by_opp_formation
from ui.filters_team.filter_group_title import filter_group_title

def by_opposition(app, db, team_id, grid_coords):
    return [
        *filter_group_title('Filter by Opposition'),
        *by_opp_team(app, db, team_id),
        *by_opp_formation(app, db, team_id)
    ]