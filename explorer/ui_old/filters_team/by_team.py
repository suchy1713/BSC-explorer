import dash_core_components as dcc
import dash_html_components as html

from ui.filters_team.team.by_season import by_season
from ui.filters_team.team.by_league import by_league
from ui.filters_team.team.by_club import by_club
from ui.filters_team.team.by_coach import by_coach
from ui.filters_team.filter_group_title import filter_group_title

def by_team(app, db, team_id, grid_coords):
    return [
        *filter_group_title(f'Select Team {team_id}'),
        *by_season(app, db, team_id),
        *by_league(app, db, team_id),
        *by_club(app, db, team_id),
        *by_coach(app, db, team_id),
    ]