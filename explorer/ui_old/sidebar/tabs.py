import datetime
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, MATCH, ALL
from dash import callback_context
from dash.exceptions import PreventUpdate
import pandas as pd
import numpy as np
import json
from ast import literal_eval

from ui.css_rules import rules
from ui.filters_team.team_filters import team_filters
from ui.filters_team.placeholder import get_placeholder
from ui.filters_layout.layout_filters import layout_filters
from ui.filters_team.utils import get_dropdown_input
from utils.group_formations import group_formations
from utils.get_filters_label import get_filters_label
from utils.get_formation_label import get_formation_label
from utils.get_intermid_output import get_intermid_output
from ui.plot.get_color import get_color
from ui.filters_plot.features import passes_select, phase_select

def tabs(app, cache, db):
    @app.callback(
        Output({'type': 'plot-filters-content', 'index-coords': MATCH}, 'children'),
        Input({'type': 'plot', 'index-coords': MATCH}, 'value'),
        State({'type': 'plot', 'index-coords': MATCH}, 'id'))
    def generate_plot_filters(plot_type, id):
        index = id['index-coords']

        filters = [
            phase_select,
            passes_select
        ]

        if plot_type == 'Pass Network':
            hides = [False, False]
        elif plot_type == 'Territory Plot - Attack':
            hides = [False, True]
        elif plot_type == 'Territory Plot - Defence':
            hides = [True, True]

        result = []
        for filter_func, hide in zip(filters, hides):
            result.append(filter_func(index, hide))

        return result

    @app.callback(
        Output({'type': 'intermid-versionDict', 'index-coords': MATCH}, 'children'),
        [Input({'type': 'phase', 'index-coords': MATCH}, 'value'),
        Input({'type': 'passes', 'index-coords': MATCH}, 'value')])
    def save_versiondict(phase, passes):
        return json.dumps({'phase': phase, 'passes': passes})

    tabs = html.Div(
        [
            dbc.Tabs(
                [
                    dbc.Tab(layout_filters(app), label="Customize", tab_id="tab-0", style={'color': rules['color']}),
                    dbc.Tab(get_placeholder(), label="Team 1", id='tab-1', tab_id="tab-1", style={'color': rules['color']}),
                    dbc.Tab(label="Team 2", id='tab-2', tab_id="tab-2", style={'color': rules['color']}),
                    dbc.Tab(label="Team 3", id='tab-3', tab_id="tab-3", tab_style={'color': rules['color'], 'display': 'none'}),
                    dbc.Tab(label="Team 4", id='tab-4', tab_id="tab-4", tab_style={'color': rules['color'], 'display': 'none'})
                ],
                id="tabs",
                active_tab="tab-1",
                className='nav-fill shadow-sm'
            )
        ]
    )

    return tabs