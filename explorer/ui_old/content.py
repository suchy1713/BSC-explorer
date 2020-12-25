import dash_bootstrap_components as dbc
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH
from dash.exceptions import PreventUpdate
import json

from ui.plot.plot import plot_container, get_graph, get_header, get_footer
from plots.codes import Passes, Phases

def content(app, cache):
    @app.callback(
        [
            Output({'type': 'plot-container', 'index-coords': '00'}, 'children'),
            Output({'type': 'plot-container', 'index-coords': '10'}, 'children'),
            Output({'type': 'plot-container', 'index-coords': '01'}, 'children'),
            Output({'type': 'plot-container', 'index-coords': '11'}, 'children')
        ],
        Input('vertical_checkbox', 'value')
    )
    def update_vertical(value):
        if len(value) > 0:
            return plot_container(app, 0, 0), plot_container(app, 1, 0), plot_container(app, 0, 1), plot_container(app, 1, 1)

        else:
            return plot_container(app, 0, 0), plot_container(app, 0, 1, True), plot_container(app, 1, 0, True), plot_container(app, 1, 1)

    @app.callback(
    Output(component_id={'type': 'plot-container-body', 'index-coords': MATCH}, component_property='children'),
    [Input(component_id={'type': 'intermid-events', 'index-coords': MATCH}, component_property='children'),
    Input(component_id={'type': 'intermid-players', 'index-coords': MATCH}, component_property='children'),
    Input(component_id={'type': 'intermid-nineties', 'index-coords': MATCH}, component_property='children'),
    Input(component_id={'type': 'intermid-clubId', 'index-coords': MATCH}, component_property='children'),
    Input(component_id={'type': 'intermid-formationLabel', 'index-coords': MATCH}, component_property='children'),
    Input(component_id={'type': 'intermid-filtersLabel', 'index-coords': MATCH}, component_property='children'),
    Input(component_id={'type': 'intermid-versionDict', 'index-coords': MATCH}, component_property='children'),
    Input(component_id={'type': 'intermid-teamColor', 'index-coords': MATCH}, component_property='children'),
    Input(component_id={'type': 'plot', 'index-coords': MATCH}, component_property='value'),
    Input(component_id={'type': 'reversed', 'index-coords': MATCH}, component_property='children')],
    State({'type': 'plot', 'index-coords': MATCH}, 'id')
    )
    @cache.memoize(timeout=20)
    def generate_plot(events, players, nineties, club, formation_text, filters_text, version_dict, color, plot_type, reversed, id):
        index = id['index-coords']
        row = int(str(id['index-coords'])[0])
        
        if reversed == 'True':
            row = 1 if row == 0 else 0

        try:
            events_df = pd.read_json(events, orient='split')
            players_df = pd.read_json(players, orient='split')
        except ValueError:
            raise PreventUpdate

        try:
            version_dict = json.loads(version_dict)
        except Exception:
            version_dict = {'passes': Passes.All, 'phase': Phases.All}

        season = club.split('_')[1]
        graph = get_graph(index, events_df, players_df, nineties, version_dict, plot_type, color)

        if row == 0:
            return [get_header(club, season, formation_text, filters_text, color, plot_type, version_dict), graph]
        else:
            return [graph, get_footer(club, season, formation_text, filters_text, color, plot_type, version_dict)]

    margin_top = '0px'
    return dbc.Row(
        dbc.CardColumns(
            [dbc.Card(
                className='shadow div-card-bg',
                id={'type': 'plot-container', 'index-coords': '00'},
                style={'height': '47vh', 'margin-top': '1.8vh', 'width': '100%'}
            ),
            dbc.Card(
                className='shadow div-card-bg',
                id={'type': 'plot-container', 'index-coords': '10'},
                style={'height': '47vh', 'margin-top': '0px', 'width': '100%'}
            ),
            dbc.Card(
                className='shadow div-card-bg',
                id={'type': 'plot-container', 'index-coords': '01'},
                style={'height': '47vh', 'margin-top': '1.8vh', 'width': '100%'}
            ),
            dbc.Card(
                className='shadow div-card-bg',
                id={'type': 'plot-container', 'index-coords': '11'},
                style={'height': '47vh', 'margin-top': '0px', 'width': '100%'}
            )],
            className='my-cards',
            style={'width': '100%'}
        ),
        className='content'
    )
