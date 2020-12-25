import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from ui.filters_team.utils import get_dropdown_input

def by_league(app, db, team_id):
    return [
        html.Label('League', className='form-label'),
        dcc.Dropdown(
            id={'type': 'league', 'index-team': team_id},
            searchable=False,
            clearable=False
        )
    ]