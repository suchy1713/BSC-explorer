from dash.dependencies import Input, Output

from assets.css_rules import rules
from metadata.id_types import *
from metadata.keys import *
from ui.sections.team_filters import team_filters


def sidebar(app, seasons):
    @app.callback(
        [Output('tab-1', children_prop),
         Output('tab-2', children_prop),
         Output('tab-3', children_prop),
         Output('tab-4', children_prop),
         Output('tab-1', tab_style_prop),
         Output('tab-2', tab_style_prop),
         Output('tab-3', tab_style_prop),
         Output('tab-4', tab_style_prop)],
        Input(coords_lookup_storage, data_prop)
    )
    def generate_tabs(lookup_data):
        lookup = lookup_data[inverted_lookup_key]
        n_teams = lookup_data[n_teams_key]

        display = {'color': rules['color']}
        hide = {'color': rules['color'], 'display': 'none'}

        if n_teams == 1:
            return team_filters(app, team1_id, lookup[team1_id], seasons),\
                   None,\
                   None,\
                   None,\
                   display,\
                   hide,\
                   hide,\
                   hide
        elif n_teams == 2:
            return team_filters(app, team1_id, lookup[team1_id], seasons), \
                   team_filters(app, team2_id, lookup[team2_id], seasons), \
                   None, \
                   None, \
                   display,\
                   display,\
                   hide,\
                   hide
        elif n_teams == 4:
            return team_filters(app, team1_id, lookup[team1_id], seasons),\
                   team_filters(app, team2_id, lookup[team2_id], seasons),\
                   team_filters(app, team3_id, lookup[team3_id], seasons),\
                   team_filters(app, team4_id, lookup[team4_id], seasons),\
                   display,\
                   display,\
                   display,\
                   display
