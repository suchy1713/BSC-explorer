import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

from ui.filters_team.utils import get_dropdown_input
from utils.group_formations import group_formations
from utils.get_filters_label import get_filters_label
from utils.get_formation_label import get_formation_label

def by_formation(app, db, team_id, row, column):
    return [
        html.Label('Formation', className='form-label'),
        dcc.Dropdown(
            id={'type': 'formation', 'index-coords': f'{row}{column}'},
            searchable=False,
            clearable=False,
        ),
        html.Div(id={'type': 'intermid-formations', 'index-coords': f'{row}{column}'}, style={'display': 'none'}),
        html.Div(id={'type': 'intermid-events', 'index-coords': f'{row}{column}'}, style={'display': 'none'}),
        html.Div(id={'type': 'intermid-players', 'index-coords': f'{row}{column}'}, style={'display': 'none'}),
        html.Div(id={'type': 'intermid-nineties', 'index-coords': f'{row}{column}'}, style={'display': 'none'}),
        html.Div(id={'type': 'intermid-clubId', 'index-coords': f'{row}{column}'}, style={'display': 'none'}),
        html.Div(id={'type': 'intermid-formationLabel', 'index-coords': f'{row}{column}'}, style={'display': 'none'}),
        html.Div(id={'type': 'intermid-filtersLabel', 'index-coords': f'{row}{column}'}, style={'display': 'none'}),
        html.Div(id={'type': 'intermid-teamColor', 'index-coords': f'{row}{column}'}, style={'display': 'none'})
    ]