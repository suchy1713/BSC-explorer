import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from ui.filters_team.utils import get_dropdown_input

def by_club(app, db, team_id):
    return [
        html.Label('Team', className='form-label'),
        dcc.Dropdown(
            id={'type': 'club', 'index-team': team_id},
            searchable=False,
            clearable=False
        ),
        html.Div(id={'type': 'intermid-colors', 'index-team': team_id}, style={'display': 'none'})
    ]