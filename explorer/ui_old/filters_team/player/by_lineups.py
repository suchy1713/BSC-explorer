import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from ui.filters_team.utils import get_dropdown_input

def by_lineups(app, db, team_id, type):
    label = 'Include Line-ups With' if type == 'include' else 'Exclude Line-ups With'

    return [
        html.Label(label, className='form-label'),
        dcc.Dropdown(
            id={'type': f'players-{type}', 'index-team': team_id},
            searchable=False,
            multi=True
        )
    ]