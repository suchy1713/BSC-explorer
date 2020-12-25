import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from ui.filters_team.utils import get_dropdown_input

def retrieve_seasons(db):
        df = db.get_seasons()
        return get_dropdown_input(df, 'season', 'season')
        
def by_season(app, db, team_id):
    seasons = retrieve_seasons(db)

    return [
        html.Label('Season', className='form-label'),
        dcc.Dropdown(
            options=seasons,
            id={'type': 'season', 'index-team': team_id},
            clearable=False,
            searchable=False,
            value=seasons[0]['value']
        )
    ]