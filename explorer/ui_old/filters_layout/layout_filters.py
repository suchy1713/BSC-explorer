import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

def vertical_checkbox():
    return dcc.Checklist(
        options=[
            {'label': 'Vertical', 'value': 'v'}
        ],
        value=['v'],
        id='vertical_checkbox'
    )  

def n_teams():
    return [
        html.Label('Number of Teams'),
        dcc.Dropdown(
        options=[
            {'label': '1', 'value': 1},
            {'label': '2', 'value': 2},
            {'label': '4', 'value': 4}
        ],
        value=2,
        id='n_teams',
        clearable=False,
        searchable=False
    )]

def layout_filters(app):

    return [
        dcc.Store(id='coords_lookup'),
        vertical_checkbox(),
        *n_teams()
    ]