import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash import callback_context
from dash.dependencies import Input, Output, State

from ui.css_rules import rules
from ui.filters_team.by_team import by_team
from ui.filters_team.by_player import by_player
from ui.filters_team.by_opposition import by_opposition
from ui.filters_team.by_date import by_date
from ui.filters_team.by_system import by_system

from ui.filters_team.team_filters_tabs import tabs

labels = {
    'By Team': by_team,
    'By Players': by_player,
    'By Opposition': by_opposition,
    'By Date': by_date,
    'By System': by_system
}

def team_filters(app, db, team_id, grid_coords):
    return tabs(app, db, team_id, grid_coords)