import datetime
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from ui.filters_team.utils import get_dropdown_input

def by_date_filter(app, db, team_id):
    return [
        html.Label('First Date to Include', className='form-label'),
        dcc.DatePickerSingle(
            id={'type': 'first-date', 'index-team': team_id},
            display_format='YYYY-MM-DD',
            clearable=False,
            first_day_of_week=1,
            style={'display': 'block'}
        ),
        html.Label('Last Date to Include', className='form-label'),
        dcc.DatePickerSingle(
            id={'type': 'last-date', 'index-team': team_id},
            display_format='YYYY-MM-DD',
            clearable=False,
            first_day_of_week=1,
            style={'display': 'block'}
        ),
    ]